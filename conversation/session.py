# conversation/session.py

from conversation.orchestrator import LeadQualificationOrchestrator


class LeadQualifierSession:
    """
    Public interface for lead qualification.
    UI / API should only interact with this class.
    """

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.orchestrator = LeadQualificationOrchestrator()
        self.last_question_attribute = None

    def reset(self):
        """
        Reset the conversation.
        """
        self.orchestrator = LeadQualificationOrchestrator()
        self.last_question_attribute = None

    def process_message(self, user_message: str) -> dict:
        """
        Process a user message and return bot response.
        """

        # If last message was a question, treat this as an answer
        if self.last_question_attribute:
            response = self.orchestrator.handle_user_answer(
                self.last_question_attribute,
                user_message
            )
        else:
            response = self.orchestrator.handle_user_message(user_message)

        # Track last asked attribute
        if response.get("type") == "question":
            self.last_question_attribute = response.get("attribute")
        else:
            self.last_question_attribute = None

        if self.debug:
            response["_debug"] = self._debug_state()

        return response

    def _debug_state(self):
        """
        Internal debug snapshot.
        """
        state = self.orchestrator.state
        if not state:
            return {}

        return state.summary()
