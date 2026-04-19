"""
Supabase クライアント・DB操作関数
"""
import os
from typing import Optional

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

_client: Optional[Client] = None


def _get_client() -> Client:
    global _client
    if _client is None:
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


# ── Events ──────────────────────────────────────────────────


def get_all_events() -> list:
    res = _get_client().table("events").select("*").order("event_date").execute()
    return res.data


def get_event(event_id: str) -> Optional[dict]:
    res = _get_client().table("events").select("*").eq("id", event_id).execute()
    if res.data:
        return res.data[0]
    return None


def create_event(data: dict) -> dict:
    res = _get_client().table("events").insert(data).execute()
    return res.data[0]


def update_event(event_id: str, data: dict) -> dict:
    res = _get_client().table("events").update(data).eq("id", event_id).execute()
    return res.data[0]


def delete_event(event_id: str) -> None:
    _get_client().table("events").delete().eq("id", event_id).execute()
