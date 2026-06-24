"""Basic hardening primitives for API rate limits and audit trail."""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


class FixedWindowRateLimiter:
    """Simple in-memory limiter keyed by caller identifier."""

    def __init__(self, limit: int = 120, window_seconds: int = 60):
        self._limit = limit
        self._window = timedelta(seconds=window_seconds)
        self._hits: dict[str, list[datetime]] = {}
        self._lock = threading.Lock()

    def allow(self, key: str) -> bool:
        now = datetime.now(timezone.utc)
        with self._lock:
            bucket = self._hits.setdefault(key, [])
            cutoff = now - self._window
            self._hits[key] = [ts for ts in bucket if ts >= cutoff]
            if len(self._hits[key]) >= self._limit:
                return False
            self._hits[key].append(now)
            return True


@dataclass
class AuditEvent:
    at: str
    action: str
    subscriber_id: str | None
    consumer_id: str | None
    result: str
    detail: dict[str, Any]


class AuditLog:
    """Append-only JSONL audit log."""

    def __init__(self, path: Path):
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def append(self, event: AuditEvent) -> None:
        line = json.dumps(asdict(event), separators=(",", ":"))
        with self._lock:
            with self._path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")
