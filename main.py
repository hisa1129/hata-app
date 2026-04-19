import os
import secrets
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import database
import mock_data

load_dotenv()

# Supabase接続情報（.envから取得）
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# DB接続が設定されているか確認（将来のSupabase統合用フラグ）
USE_SUPABASE = bool(SUPABASE_URL and SUPABASE_KEY)

app = FastAPI(title="旗アプリ")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ── HTTPException のレスポンスに charset=utf-8 を明示 ──────────
# デフォルトの application/json は charset 未指定のため、
# ブラウザが Shift-JIS として誤検出するケースを防ぐ
@app.exception_handler(HTTPException)
async def _http_exception_handler(request: Request, exc: HTTPException):
    headers = dict(exc.headers or {})
    headers["Content-Type"] = "application/json; charset=utf-8"
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=headers,
    )


# ── 管理者認証 ──────────────────────────────────────────────
_http_basic = HTTPBasic()


def verify_admin(credentials: HTTPBasicCredentials = Depends(_http_basic)):
    admin_password = os.getenv("ADMIN_PASSWORD", "admin")
    ok = secrets.compare_digest(
        credentials.password.encode(), admin_password.encode()
    )
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )


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
# イベント詳細
# ──────────────────────────────────────────

@app.get("/events/{event_id}", response_class=HTMLResponse)
async def event_detail(request: Request, event_id: str):
    event = mock_data.get_event(event_id)
    if not event:
        return RedirectResponse("/", status_code=303)
    flags = mock_data.get_flags_by_event(event_id)
    return templates.TemplateResponse("events/detail.html", {
        "request": request,
        "event": event,
        "flags": flags,
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
    # 同じイベントに既にエントリー済みか確認（棄却を除く）
    my_entries = mock_data.get_my_entries()
    already_entered = any(
        e["flag"]["event_id"] == flag["event_id"] and e["status"] != "棄却"
        for e in my_entries
    )
    return templates.TemplateResponse("flags/detail.html", {
        "request": request,
        "flag": flag,
        "event": event,
        "already_entered": already_entered,
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
    email: Optional[str] = Form(None),
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
        "email": email or "",
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
    email: Optional[str] = Form(None),
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
        "email": email or "",
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
    email: Optional[str] = Form(None),
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
        "email": email or "",
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
    email: Optional[str] = Form(None),
):
    # モック：DBへの保存は行わず完了ページへリダイレクト
    return RedirectResponse("/create/done", status_code=303)


@app.get("/create/done", response_class=HTMLResponse)
async def create_done(request: Request):
    return templates.TemplateResponse("flags/created.html", {"request": request})


# ──────────────────────────────────────────
# マイエントリー
# ──────────────────────────────────────────

@app.get("/my/flags", response_class=HTMLResponse)
async def my_flags(request: Request):
    flags = mock_data.get_my_flags()
    events = {e["id"]: e for e in mock_data.EVENTS}
    raised_counts = {f["id"]: len(mock_data.get_raised_hands(f["id"])) for f in flags}
    return templates.TemplateResponse("my/flags.html", {
        "request": request,
        "flags": flags,
        "events": events,
        "raised_counts": raised_counts,
    })


@app.get("/my/entries", response_class=HTMLResponse)
async def my_entries(request: Request):
    entries = mock_data.get_my_entries()
    return templates.TemplateResponse("my/entries.html", {
        "request": request,
        "entries": entries,
    })


# ──────────────────────────────────────────
# 管理画面：イベント管理
# ──────────────────────────────────────────

_ADMIN_MESSAGES = {
    "created": "イベントを登録しました",
    "updated": "イベントを更新しました",
    "deleted": "イベントを削除しました",
}


@app.get("/admin/events", response_class=HTMLResponse)
async def admin_events(
    request: Request,
    msg: Optional[str] = None,
    _: None = Depends(verify_admin),
):
    events = database.get_all_events()
    return templates.TemplateResponse(request, "admin/events.html", {
        "events": events,
        "message": _ADMIN_MESSAGES.get(msg),
    })


@app.get("/admin/events/new", response_class=HTMLResponse)
async def admin_events_new(
    request: Request,
    _: None = Depends(verify_admin),
):
    return templates.TemplateResponse(request, "admin/events_new.html", {})


@app.post("/admin/events")
async def admin_events_create(
    request: Request,
    _: None = Depends(verify_admin),
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    location: str = Form(...),
    event_date: str = Form(...),
    organizer: Optional[str] = Form(None),
    url: Optional[str] = Form(None),
    image_url: Optional[str] = Form(None),
    area: Optional[str] = Form(None),
):
    data: dict = {
        "title": title,
        "description": description,
        "category": category,
        "location": location,
        "event_date": event_date,
    }
    if organizer:
        data["organizer"] = organizer
    if url:
        data["url"] = url
    if image_url:
        data["image_url"] = image_url
    if area:
        data["area"] = area

    database.create_event(data)
    return RedirectResponse("/admin/events?msg=created", status_code=303)


@app.get("/admin/events/{event_id}/edit", response_class=HTMLResponse)
async def admin_events_edit(
    request: Request,
    event_id: str,
    _: None = Depends(verify_admin),
):
    event = database.get_event(event_id)
    if not event:
        return RedirectResponse("/admin/events", status_code=303)
    return templates.TemplateResponse(request, "admin/events_edit.html", {
        "event": event,
    })


@app.post("/admin/events/{event_id}/edit")
async def admin_events_update(
    request: Request,
    event_id: str,
    _: None = Depends(verify_admin),
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    location: str = Form(...),
    event_date: str = Form(...),
    organizer: Optional[str] = Form(None),
    url: Optional[str] = Form(None),
    image_url: Optional[str] = Form(None),
    area: Optional[str] = Form(None),
):
    data = {
        "title": title,
        "description": description,
        "category": category,
        "location": location,
        "event_date": event_date,
        "organizer": organizer or None,
        "url": url or None,
        "image_url": image_url or None,
        "area": area or None,
    }
    database.update_event(event_id, data)
    return RedirectResponse("/admin/events?msg=updated", status_code=303)


@app.post("/admin/events/{event_id}/delete")
async def admin_events_delete(
    request: Request,
    event_id: str,
    _: None = Depends(verify_admin),
):
    database.delete_event(event_id)
    return RedirectResponse("/admin/events?msg=deleted", status_code=303)
