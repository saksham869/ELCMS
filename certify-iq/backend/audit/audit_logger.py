import json
import os
from datetime import datetime, timezone
from pathlib import Path


class AuditLogger:
    def __init__(self, log_path: str = "audit_log.jsonl"):
        self.log_path = Path(log_path)
        self.log_path.touch(exist_ok=True)

    def log(self, entry: dict) -> None:
        entry["logged_at"] = datetime.now(timezone.utc).isoformat()
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def get_recent(self, n: int = 20) -> list:
        if not self.log_path.exists():
            return []
        lines = self.log_path.read_text(encoding="utf-8").strip().splitlines()
        recent = lines[-n:] if len(lines) >= n else lines
        results = []
        for line in reversed(recent):
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError:
                pass
        return results


audit_logger = AuditLogger()