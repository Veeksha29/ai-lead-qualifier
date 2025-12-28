# conversation/state.py

class ConversationState:
    def __init__(self, category: str, schema: dict, language: str = "en"):
        self.category = category
        self.schema = schema
        self.language = language

        self.collected_attributes = {}
        self.questions_asked = 0

        for attr in (
            schema.get("mandatory", [])
            + schema.get("important", [])
            + schema.get("optional", [])
        ):
            self.collected_attributes[attr] = None

    # -----------------------------
    # Missing helpers
    # -----------------------------

    def missing_mandatory(self):
        return [
            a for a in self.schema.get("mandatory", [])
            if self.collected_attributes.get(a) is None
        ]

    def missing_important(self):
        return [
            a for a in self.schema.get("important", [])
            if self.collected_attributes.get(a) is None
        ]

    def missing_optional(self):
        return [
            a for a in self.schema.get("optional", [])
            if self.collected_attributes.get(a) is None
        ]

    # -----------------------------
    # Update
    # -----------------------------

    def update(self, extracted_data: dict):
        for k, v in extracted_data.items():
            if k in self.collected_attributes and v is not None:
                self.collected_attributes[k] = v

    # -----------------------------
    # Qualification logic
    # -----------------------------

    def min_questions_required(self) -> int:
        cat = self.category.lower()

        if any(x in cat for x in ["plumber", "electrician", "repair"]):
            return 2

        if any(x in cat for x in ["photographer", "caterer", "decorator"]):
            return 3

        if any(x in cat for x in ["supplier", "manufacturer", "industrial"]):
            return 3

        return 2

    def is_mandatory_complete(self) -> bool:
        return len(self.missing_mandatory()) == 0

    def is_lead_ready(self) -> bool:
        filled = len([v for v in self.collected_attributes.values() if v])

        return (
            self.is_mandatory_complete()
            and self.questions_asked >= self.min_questions_required()
        )

    # -----------------------------
    # Debug
    # -----------------------------

    def summary(self) -> dict:
        return {
            "category": self.category,
            "questions_asked": self.questions_asked,
            "collected_attributes": self.collected_attributes,
            "missing_mandatory": self.missing_mandatory(),
            "missing_important": self.missing_important(),
            "missing_optional": self.missing_optional(),
        }
