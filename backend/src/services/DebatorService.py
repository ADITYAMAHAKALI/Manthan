import uuid
from typing import Dict, List
from src.services.GeminiService import GeminiService
from src.utils.storage import save_session, load_session

class DebatorService:
    def __init__(self):
        self.gemini = GeminiService()

    def generate_session(self, topic: str) -> str:
        session_id = str(uuid.uuid4())
        session = {"topic": topic, "history": []}
        save_session(session_id, session)
        return session_id

    def _build_prompt(self, session: Dict, role: str) -> str:
        topic = session["topic"]
        history = session["history"]

        prompt = f"You are debating on: '{topic}'. Your role is '{role}'.\n\n"
        prompt += "Conversation:\n"
        for entry in history:
            prompt += f"{entry['role'].upper()}: {entry['message']}\n"
        prompt += f"\nRespond now as {role.upper()}.\n"
        return prompt

    def generate_argument(self, session_id: str, role: str) -> str:
        session = load_session(session_id)
        if not session:
            raise ValueError("Invalid session")

        prompt = self._build_prompt(session, role)
        response = self.gemini.get_text(prompt)

        session["history"].append({"role": role, "message": response})
        save_session(session_id, session)
        return response

    def stream_argument(self, session_id: str, role: str):
        session = load_session(session_id)
        if not session:
            raise ValueError("Invalid session")

        prompt = self._build_prompt(session, role)
        return self.gemini.get_stream_generator(prompt)

    def get_session_data(self, session_id: str) -> Dict:
        return load_session(session_id)
