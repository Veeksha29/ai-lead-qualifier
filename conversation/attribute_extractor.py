# conversation/attribute_extractor.py

import json
import re
from llm.groq_client import call_llm
from llm.prompts import ATTRIBUTE_EXTRACTION_PROMPT


def _extract_json(text: str) -> dict:
    """
    Safely extract JSON from LLM output.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in LLM output")
    return json.loads(match.group())


def extract_attribute(category: str, attribute: str, user_input: str) -> dict:
    """
    Extracts a single attribute value from user input.

    Returns:
    {
        attribute_name: value | None
    }
    """

    user_prompt = f"""
Category: {category}
Attribute: {attribute}
User Input: {user_input}
"""

    raw_response = call_llm(
        system_prompt=ATTRIBUTE_EXTRACTION_PROMPT,
        user_prompt=user_prompt
    )

    try:
        data = _extract_json(raw_response)

        # Ensure only expected attribute is returned
        if attribute not in data:
            return {attribute: None}

        return {attribute: data.get(attribute)}

    except Exception:
        print("⚠️ ATTRIBUTE EXTRACTION FAILED")
        print("Attribute:", attribute)
        print("Raw output:", raw_response)

        # Safe fallback
        return {attribute: None}
