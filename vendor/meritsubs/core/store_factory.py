"""Select subscriber store: Supabase (prod/Vercel) or local file (dev)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Protocol

from .store import Subscriber, SubscriberStore
from .supabase_store import SupabaseSubscriberStore


class SubscriberStoreProtocol(Protocol):
    def onboard_guest(self, *, handle: str, consumer_id: str) -> Subscriber: ...
    def onboard_registered(self, *, email: str, consumer_id: str) -> Subscriber: ...
    def mark_certified(self, subscriber_id: str, *, square_ref: str) -> Subscriber: ...
    def attest_age(
        self, subscriber_id: str, *, date_of_birth_iso: str, age_band: str
    ) -> Subscriber: ...
    def add_grants(self, subscriber_id: str, namespace: str, keys: list[str]) -> Subscriber: ...
    def get(self, subscriber_id: str) -> Subscriber | None: ...
    def sync_consumer_mirror(
        self, *, action: str, subscriber: dict, consumer_id: str = "dirt"
    ) -> Subscriber | None: ...


def store_backend_name() -> str:
    if os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_SERVICE_ROLE_KEY"):
        return "supabase"
    return "file"


def create_subscriber_store() -> SubscriberStoreProtocol:
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    if url and key:
        return SupabaseSubscriberStore(url, key)
    persist = os.environ.get("MERITSUBS_STORE_PATH", "output/subscribers.json")
    return SubscriberStore(persist_path=Path(persist))
