import os
import json
from typing import Dict

SESSIONS_DIR = "sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

def save_session(session_id: str, data: Dict):
    filepath = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def load_session(session_id: str) -> Dict:
    filepath = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)
