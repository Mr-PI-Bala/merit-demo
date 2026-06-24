"""De-identified cohort event ingest (consumer → meritsubs)."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class CohortIngestResult:
    accepted: int
    aggregate_key: str


class CohortStore:
    def __init__(self, path: Path | None = None) -> None:
        if path is None:
            vercel = os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV")
            default = (
                "/tmp/meritsubs/cohort_events.jsonl"
                if vercel or os.environ.get("AWS_LAMBDA_FUNCTION_NAME")
                else "output/analytics/cohort_events.jsonl"
            )
            path = Path(os.environ.get("MERITSUBS_COHORT_PATH", default))
        self._path = path

    def ingest(self, *, consumer_id: str, events: list[dict[str, Any]]) -> CohortIngestResult:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        aggregate_key = f"{consumer_id}:{day}"
        with self._path.open("a", encoding="utf-8") as fh:
            for event in events:
                row = {
                    "at": datetime.now(timezone.utc).isoformat(),
                    "consumer_id": consumer_id,
                    "aggregate_key": aggregate_key,
                    "event": event,
                }
                fh.write(json.dumps(row, separators=(",", ":")) + "\n")
        return CohortIngestResult(accepted=len(events), aggregate_key=aggregate_key)

    def aggregates(self, *, consumer_id: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
        if not self._path.exists():
            return []
        counts: dict[str, int] = {}
        for line in self._path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if consumer_id and row.get("consumer_id") != consumer_id:
                continue
            key = str(row.get("aggregate_key", "unknown"))
            counts[key] = counts.get(key, 0) + 1
        items = [{"aggregate_key": k, "event_count": v} for k, v in sorted(counts.items())]
        return items[-limit:]
