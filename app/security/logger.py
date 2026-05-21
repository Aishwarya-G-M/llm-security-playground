from collections import deque
from datetime import datetime, timezone
from typing import Optional

# Bounded in-memory log store — keeps last 1000 entries only
_logs: deque = deque(maxlen=1000)

def log_request(
        endpoint: str,
        prompt: str,
        is_safe: bool,
        reason: str,
        response: Optional[str] = None
) -> None:
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "endpoint": endpoint,
        "prompt": prompt,
        "is_safe": is_safe,
        "reason": reason,
        "response": response
    }
    _logs.append(entry)

def get_logs() -> list[dict]:
    return list(_logs)  # convert deque to list for JSON serialization


