# conversation/question_generator.py

import json
import re
from llm.groq_client import call_llm
from llm.prompts import QUESTION_PROMPT


def _extract_json(text: str) -> dict:
    """
    Safely extract JSON from LLM output.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in LLM output")
    return json.loads(match.group())


def select_next_attribute(state):
    """
    Priority order:
    1. Mandatory
    2. Important
    3. Optional
    """
    missing = state.missing_mandatory()
    if missing:
        return missing[0]

    missing = state.missing_important()
    if missing:
        return missing[0]

    missing = state.missing_optional()
    if missing:
        return missing[0]

    return None


def generate_question(state):
    """
    Generates the next question + suggestions based on conversation state.
    """

    attribute = select_next_attribute(state)

    if not attribute:
        return None  # Nothing left to ask

    # Provide lightweight examples to guide LLM
    examples = attribute.replace("_", " ").split()

    user_prompt = f"""
Category: {state.category}
Missing Attribute: {attribute}
Examples: {", ".join(examples)}
"""

    language = getattr(state, "language", "en")

    system_prompt = QUESTION_PROMPT.replace("__LANGUAGE__", language)

    raw_response = call_llm(
    system_prompt=system_prompt,
    user_prompt=user_prompt
    )


    try:
        data = _extract_json(raw_response)
        state.questions_asked += 1
        return {
            "attribute": attribute,
            "question": data.get("question"),
            "suggestions": data.get("suggestions", [])
        }

    except Exception:
        print("⚠️ QUESTION GENERATION FAILED")
        print("Raw output:", raw_response)

        # Fallback safe question
        return {
            "attribute": attribute,
            "question": f"Please provide {attribute.replace('_', ' ')}",
            "suggestions": ["Other"]
        }
