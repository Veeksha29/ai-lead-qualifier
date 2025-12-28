# conversation/orchestrator.py

from conversation.category_extractor import extract_category
from schema.schema_generator import generate_schema
from conversation.state import ConversationState
from conversation.question_generator import generate_question
from conversation.attribute_extractor import extract_attribute
from conversation.language import detect_language


class LeadQualificationOrchestrator:
    """
    Central brain controlling lead qualification flow.
    """

    def __init__(self):
        self.state = None

    # -------------------------------------------------
    # USER MESSAGE HANDLER
    # -------------------------------------------------
    def handle_user_message(self, user_message: str) -> dict:

        # -----------------------------------------
        # AUTO-RESET IF USER CHANGES INTENT MID-CHAT
        # -----------------------------------------
        if self.state is not None:
            category_data = extract_category(user_message)

            if (
                category_data.get("category")
                and category_data.get("confidence", 0) > 0.7
                and category_data["category"] != self.state.category
            ):
                # New intent detected → reset conversation
                self.state = None

        # -----------------------------------------
        # INITIALIZE CONVERSATION (IF NEEDED)
        # -----------------------------------------
        if self.state is None:
            category_data = extract_category(user_message)

            if (
                not category_data.get("category")
                or category_data.get("confidence", 0) < 0.6
            ):
                return {
                    "type": "clarification",
                    "question": "Can you tell me what service or product you are looking for?",
                    "suggestions": ["Service", "Product", "Not sure"]
                }

            category = category_data["category"]

            # Detect language once per conversation
            language = detect_language(user_message)

            # Generate schema dynamically
            schema = generate_schema(category)

            # Create new state
            self.state = ConversationState(
                category=category,
                schema=schema,
                language=language
            )

            # Try extracting attributes from first message
            for attr in self.state.collected_attributes.keys():
                extracted = extract_attribute(category, attr, user_message)
                self.state.update(extracted)

        # -----------------------------------------
        # CHECK IF LEAD IS READY
        # -----------------------------------------
        if self.state.is_lead_ready():
            return {
                "type": "lead_ready",
                "category": self.state.category,
                "data": self.state.collected_attributes
            }

        # -----------------------------------------
        # ASK NEXT QUESTION
        # -----------------------------------------
        question_payload = generate_question(self.state)

        # Safety fallback
        if not question_payload:
            return {
                "type": "lead_ready",
                "category": self.state.category,
                "data": self.state.collected_attributes
            }

        return {
            "type": "question",
            "attribute": question_payload["attribute"],
            "question": question_payload["question"],
            "suggestions": question_payload.get("suggestions", [])
        }

    # -------------------------------------------------
    # USER ANSWER HANDLER
    # -------------------------------------------------
    def handle_user_answer(self, attribute: str, user_answer: str) -> dict:

        if not self.state:
            return {
                "type": "error",
                "message": "Conversation not initialized"
            }

        # Extract attribute value
        extracted = extract_attribute(
            self.state.category,
            attribute,
            user_answer
        )

        self.state.update(extracted)

        # Check lead readiness again
        if self.state.is_lead_ready():
            return {
                "type": "lead_ready",
                "category": self.state.category,
                "data": self.state.collected_attributes
            }

        # Ask next question
        question_payload = generate_question(self.state)

        return {
            "type": "question",
            "attribute": question_payload["attribute"],
            "question": question_payload["question"],
            "suggestions": question_payload.get("suggestions", [])
        }
