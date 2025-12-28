# schema/schema_generator.py

import json
import re
from llm.groq_client import call_llm
from llm.prompts import SCHEMA_PROMPT


def _extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found")
    return json.loads(match.group())


def generate_schema(category: str) -> dict:
    raw_response = call_llm(
        system_prompt=SCHEMA_PROMPT,
        user_prompt=f"Category: {category}"
    )

    try:
        schema = _extract_json(raw_response)

        mandatory = schema.get("mandatory", [])
        important = schema.get("important", [])
        optional = schema.get("optional", [])

        # 🔒 GUARDRAIL: ensure minimum 2 mandatory attributes
        if len(mandatory) < 2:
            if "service_type" not in mandatory:
                mandatory.append("service_type")

        return {
            "mandatory": mandatory,
            "important": important,
            "optional": optional
        }

    except Exception:
        # Absolute fallback
        return {
            "mandatory": ["location", "service_type"],
            "important": [],
            "optional": []
        }
