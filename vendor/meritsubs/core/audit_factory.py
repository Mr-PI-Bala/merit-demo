"""Create audit log backend: Supabase (prod) or local JSONL (dev)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Protocol

from .audit_supabase import SupabaseAuditLog
from .security import AuditEvent, AuditLog


class AuditLogProtocol(Protocol):
    def append(self, event: AuditEvent) -> None: ...


def create_audit_log() -> tuple[AuditLogProtocol, str]:
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    if url and key:
        return SupabaseAuditLog(url, key), "supabase"
    path = Path(os.environ.get("MERITSUBS_AUDIT_PATH", "output/audit/events.jsonl"))
    return AuditLog(path), "file"
