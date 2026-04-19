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


# ── Flags ──────────────────────────────────────────────────


def get_filtered_flags(anxiety_level: str, category: str, vibe: str) -> list:
    events_res = (
        _get_client().table("events").select("id").eq("category", category).execute()
    )
    event_ids = [e["id"] for e in events_res.data]
    if not event_ids:
        return []
    res = (
        _get_client()
        .table("flags")
        .select("*")
        .eq("status", "募集中")
        .eq("anxiety_level", anxiety_level)
        .eq("vibe", vibe)
        .in_("event_id", event_ids)
        .execute()
    )
    return res.data


def create_flag(data: dict) -> dict:
    res = _get_client().table("flags").insert(data).execute()
    return res.data[0]


def get_flag(flag_id: str) -> Optional[dict]:
    res = _get_client().table("flags").select("*").eq("id", flag_id).execute()
    if res.data:
        return res.data[0]
    return None


def get_all_flags() -> list:
    res = (
        _get_client()
        .table("flags")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return res.data


def update_flag_status(flag_id: str, status: str) -> None:
    _get_client().table("flags").update({"status": status}).eq("id", flag_id).execute()


def get_flags_by_event(event_id: str) -> list:
    res = (
        _get_client()
        .table("flags")
        .select("*")
        .eq("event_id", event_id)
        .eq("status", "募集中")
        .execute()
    )
    return res.data


# ── Applicants ──────────────────────────────────────────────


def create_applicant(data: dict) -> dict:
    res = _get_client().table("applicants").insert(data).execute()
    return res.data[0]


def get_applicant(applicant_id: str) -> Optional[dict]:
    res = _get_client().table("applicants").select("*").eq("id", applicant_id).execute()
    if res.data:
        return res.data[0]
    return None


def get_applicants_by_flag(flag_id: str) -> list:
    res = (
        _get_client()
        .table("applicants")
        .select("*")
        .eq("flag_id", flag_id)
        .order("created_at")
        .execute()
    )
    return res.data


def get_applicant_counts_for_flags(flag_ids: list) -> dict:
    """複数の旗IDに対する申請者数を一括取得"""
    if not flag_ids:
        return {}
    res = (
        _get_client()
        .table("applicants")
        .select("flag_id")
        .in_("flag_id", flag_ids)
        .execute()
    )
    counts: dict = {}
    for a in res.data:
        fid = a["flag_id"]
        counts[fid] = counts.get(fid, 0) + 1
    return counts


def get_all_applicants_joined() -> list:
    """全申請者を取得し、flag・event データを結合して返す"""
    applicants = (
        _get_client()
        .table("applicants")
        .select("*")
        .order("created_at", desc=True)
        .execute()
        .data
    )
    if not applicants:
        return []
    flag_ids = list({a["flag_id"] for a in applicants})
    flags_res = _get_client().table("flags").select("*").in_("id", flag_ids).execute()
    flags_map = {f["id"]: f for f in flags_res.data}
    event_ids = list({f["event_id"] for f in flags_res.data if f.get("event_id")})
    events_map: dict = {}
    if event_ids:
        events_res = (
            _get_client().table("events").select("*").in_("id", event_ids).execute()
        )
        events_map = {e["id"]: e for e in events_res.data}
    result = []
    for a in applicants:
        flag = flags_map.get(a["flag_id"], {})
        event = events_map.get(flag.get("event_id", ""), {})
        result.append({**a, "flag": flag, "event": event})
    return result


def update_applicant_status(applicant_id: str, status: str) -> None:
    _get_client().table("applicants").update({"status": status}).eq("id", applicant_id).execute()


_GROUP_MAX = {"二人": 1, "三人": 2, "四人": 3, "三人以上でワイワイ": 2}


def check_and_close_flag_if_full(flag_id: str) -> bool:
    """承認数が上限に達したら旗を締め切る。締め切った場合 True を返す。"""
    flag = get_flag(flag_id)
    if not flag or flag["status"] != "募集中":
        return False
    max_approvals = _GROUP_MAX.get(flag["group_size"], 2)
    res = (
        _get_client()
        .table("applicants")
        .select("id", count="exact")
        .eq("flag_id", flag_id)
        .eq("status", "承認済み")
        .execute()
    )
    if (res.count or 0) >= max_approvals:
        update_flag_status(flag_id, "締切済")
        return True
    return False
