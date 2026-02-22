import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import mock_data

load_dotenv()

# Supabase接続情報（.envから取得）
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# DB接続が設定されているか確認（将来のSupabase統合用フラグ）
USE_SUPABASE = bool(SUPABASE_URL and SUPABASE_KEY)

app = FastAPI(title="旗アプリ")
templates = Jinja2Templates(directory="templates")


# ──────────────────────────────────────────
# トップページ
# ──────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ──────────────────────────────────────────
# 旗を探す
# ──────────────────────────────────────────

@app.get("/find/step1", response_class=HTMLResponse)
async def find_step1(request: Request):
    return templates.TemplateResponse("find/step1.html", {"request": request})


@app.post("/find/step2", response_class=HTMLResponse)
async def find_step2(
    request: Request,
    anxiety_level: str = Form(...),
):
    return templates.TemplateResponse("find/step2.html", {
        "request": request,
        "anxiety_level": anxiety_level,
    })


@app.post("/find/list", response_class=HTMLResponse)
async def find_list(
    request: Request,
    anxiety_level: str = Form(...),
    category: str = Form(...),
    vibe: str = Form(...),
):
    flags = mock_data.get_filtered_flags(anxiety_level, category, vibe)
    events = {e["id"]: e for e in mock_data.EVENTS}
    return templates.TemplateResponse("find/list.html", {
        "request": request,
        "flags": flags,
        "events": events,
        "anxiety_level": anxiety_level,
        "category": category,
        "vibe": vibe,
    })


# ──────────────────────────────────────────
# 旗の詳細・手を挙げる
# ──────────────────────────────────────────

@app.get("/raised", response_class=HTMLResponse)
async def raised(request: Request):
    return templates.TemplateResponse("flags/raised.html", {"request": request})


@app.get("/flags/{flag_id}", response_class=HTMLResponse)
async def flag_detail(request: Request, flag_id: str):
    flag = mock_data.get_flag(flag_id)
    if not flag:
        return RedirectResponse("/find/step1", status_code=303)
    event = mock_data.get_event(flag["event_id"])
    return templates.TemplateResponse("flags/detail.html", {
        "request": request,
        "flag": flag,
        "event": event,
    })


@app.get("/flags/{flag_id}/manage", response_class=HTMLResponse)
async def flag_manage(request: Request, flag_id: str):
    flag = mock_data.get_flag(flag_id)
    if not flag:
        return RedirectResponse("/find/step1", status_code=303)
    event = mock_data.get_event(flag["event_id"])
    raised_hands = mock_data.get_raised_hands(flag_id)
    return templates.TemplateResponse("flags/manage.html", {
        "request": request,
        "flag": flag,
        "event": event,
        "raised_hands": raised_hands,
    })


@app.post("/flags/{flag_id}/raise")
async def raise_hand(
    request: Request,
    flag_id: str,
    nickname: str = Form(...),
    email: str = Form(...),
    message: Optional[str] = Form(None),
    sns_type: Optional[str] = Form(None),
    sns_account: Optional[str] = Form(None),
):
    # モック：DBへの保存は行わず完了ページへリダイレクト
    return RedirectResponse("/raised", status_code=303)


# ──────────────────────────────────────────
# 旗を立てる
# ──────────────────────────────────────────

@app.get("/create/step1", response_class=HTMLResponse)
async def create_step1(request: Request):
    return templates.TemplateResponse("flags/create_step1.html", {
        "request": request,
        "events": mock_data.EVENTS,
    })


@app.post("/create/step2", response_class=HTMLResponse)
async def create_step2(
    request: Request,
    event_id: str = Form(...),
):
    event = mock_data.get_event(event_id)
    return templates.TemplateResponse("flags/create_step2.html", {
        "request": request,
        "event": event,
        "event_id": event_id,
    })


@app.post("/create/step3", response_class=HTMLResponse)
async def create_step3(
    request: Request,
    event_id: str = Form(...),
    nickname: str = Form(...),
    anxiety_level: str = Form(...),
    vibe: str = Form(...),
    reason: str = Form(...),
    sns_type: Optional[str] = Form(None),
    sns_account: Optional[str] = Form(None),
):
    event = mock_data.get_event(event_id)
    return templates.TemplateResponse("flags/create_step3.html", {
        "request": request,
        "event": event,
        "event_id": event_id,
        "nickname": nickname,
        "anxiety_level": anxiety_level,
        "vibe": vibe,
        "reason": reason,
        "sns_type": sns_type or "",
        "sns_account": sns_account or "",
    })


@app.post("/create/step4", response_class=HTMLResponse)
async def create_step4(
    request: Request,
    event_id: str = Form(...),
    nickname: str = Form(...),
    anxiety_level: str = Form(...),
    vibe: str = Form(...),
    reason: str = Form(...),
    group_size: str = Form(...),
    gender_pref: str = Form(...),
    member_type: str = Form(...),
    sns_type: Optional[str] = Form(None),
    sns_account: Optional[str] = Form(None),
):
    event = mock_data.get_event(event_id)
    return templates.TemplateResponse("flags/create_step4.html", {
        "request": request,
        "event": event,
        "event_id": event_id,
        "nickname": nickname,
        "anxiety_level": anxiety_level,
        "vibe": vibe,
        "reason": reason,
        "group_size": group_size,
        "gender_pref": gender_pref,
        "member_type": member_type,
        "sns_type": sns_type or "",
        "sns_account": sns_account or "",
    })


@app.post("/create/confirm", response_class=HTMLResponse)
async def create_confirm(
    request: Request,
    event_id: str = Form(...),
    nickname: str = Form(...),
    anxiety_level: str = Form(...),
    vibe: str = Form(...),
    reason: str = Form(...),
    group_size: str = Form(...),
    gender_pref: str = Form(...),
    member_type: str = Form(...),
    meeting_place: str = Form(...),
    meeting_date: str = Form(...),
    meeting_time_only: str = Form(...),
    deadline: str = Form(...),
    sns_type: Optional[str] = Form(None),
    sns_account: Optional[str] = Form(None),
):
    meeting_time = f"{meeting_date} {meeting_time_only}"
    event = mock_data.get_event(event_id)
    return templates.TemplateResponse("flags/create_confirm.html", {
        "request": request,
        "event": event,
        "event_id": event_id,
        "nickname": nickname,
        "anxiety_level": anxiety_level,
        "vibe": vibe,
        "reason": reason,
        "group_size": group_size,
        "gender_pref": gender_pref,
        "member_type": member_type,
        "meeting_place": meeting_place,
        "meeting_time": meeting_time,
        "deadline": deadline,
        "sns_type": sns_type or "",
        "sns_account": sns_account or "",
    })


@app.post("/create/submit")
async def create_submit(
    request: Request,
    event_id: str = Form(...),
    nickname: str = Form(...),
    anxiety_level: str = Form(...),
    vibe: str = Form(...),
    reason: str = Form(...),
    group_size: str = Form(...),
    gender_pref: str = Form(...),
    member_type: str = Form(...),
    meeting_place: str = Form(...),
    meeting_time: str = Form(...),
    deadline: str = Form(...),
    sns_type: Optional[str] = Form(None),
    sns_account: Optional[str] = Form(None),
):
    # モック：DBへの保存は行わず完了ページへリダイレクト
    return RedirectResponse("/create/done", status_code=303)


@app.get("/create/done", response_class=HTMLResponse)
async def create_done(request: Request):
    return templates.TemplateResponse("flags/created.html", {"request": request})
