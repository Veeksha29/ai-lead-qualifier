# conversation/category_extractor.py

import json
from llm.groq_client import call_llm
from llm.prompts import CATEGORY_EXTRACTION_PROMPT


def extract_category(user_input: str) -> dict:
    """
    Extracts canonical category from raw user input.

    Returns:
    {
        "category": str | None,
        "confidence": float
    }
    """

    try:
        raw_response = call_llm(
            system_prompt=CATEGORY_EXTRACTION_PROMPT,
            user_prompt=user_input
        )

        data = json.loads(raw_response)

        # Safety defaults
        category = data.get("category")
        confidence = float(data.get("confidence", 0.0))

        # Normalize bad outputs
        if not category or confidence < 0.3:
            return {
                "category": None,
                "confidence": confidence
            }

        return {
            "category": category.strip(),
            "confidence": confidence
        }

    except Exception as e:
        # Never let category extraction crash the system
        return {
            "category": None,
            "confidence": 0.0
        }

