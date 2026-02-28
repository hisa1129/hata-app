"""
モックデータ - Supabase未接続でもUIを確認できるようにするためのダミーデータ
"""

EVENTS = [
    {
        "id": "evt-001",
        "title": "地域の夏祭り 2024",
        "description": "地元の夏祭りです。地域の人たちと一緒に盛り上がりましょう！屋台や花火もあります。",
        "category": "祭り・地域行事",
        "location": "市民公園",
        "event_date": "2024-08-15",
    },
    {
        "id": "evt-002",
        "title": "川沿い清掃ボランティア",
        "description": "地域の川をみんなでキレイにするボランティア活動です。軍手・ゴミ袋は用意されています。",
        "category": "ボランティア",
        "location": "旭川沿い（北の橋集合）",
        "event_date": "2024-08-20",
    },
    {
        "id": "evt-003",
        "title": "古民家リノベーション体験",
        "description": "空き家になった古民家を地域の人たちと一緒に直す体験ワークショップ。DIY初心者も大歓迎！",
        "category": "ワークショップ・体験",
        "location": "旧田中家（市内北地区）",
        "event_date": "2024-09-07",
    },
    {
        "id": "evt-004",
        "title": "子ども食堂のお手伝い",
        "description": "月に一度開催される子ども食堂で調理・配膳のお手伝いをします。料理が得意でなくてもOK。",
        "category": "ボランティア",
        "location": "コミュニティセンター 調理室",
        "event_date": "2024-08-25",
    },
    {
        "id": "evt-005",
        "title": "伝統工芸体験ワークショップ",
        "description": "地域に伝わる伝統工芸を職人さんから直接教わる体験会。作ったものはお土産に持ち帰れます！",
        "category": "ワークショップ・体験",
        "location": "地域文化センター",
        "event_date": "2024-09-14",
    },
]

FLAGS = [
    {
        "id": "flag-001",
        "event_id": "evt-001",
        "nickname": "はるか",
        "anxiety_level": "初めてで不安",
        "vibe": "落ち着いて参加したい",
        "reason": "地域の人と繋がりたいと思っているけど、一人だと緊張してしまう。誰かと一緒なら安心して楽しめそう！地元の夏祭りの雰囲気を味わいたいです。",
        "group_size": "三人",
        "gender_pref": "こだわらない",
        "member_type": "大学生限定",
        "meeting_place": "市民公園 正面入口",
        "meeting_time": "2024-08-15 16:00",
        "deadline": "2024-08-13",
        "status": "募集中",
        "created_at": "2024-08-01",
        "sns_type": "Instagram",
        "sns_account": "@haruka_hokkaido",
    },
    {
        "id": "flag-002",
        "event_id": "evt-002",
        "nickname": "たくみ",
        "anxiety_level": "慣れている",
        "vibe": "ワイワイ参加したい",
        "reason": "ボランティアは何度か経験があるけど、いつも一人で参加してて少し寂しい。一緒に楽しく作業できる仲間を探しています！終わったらご飯でも行きましょう。",
        "group_size": "三人以上でワイワイ",
        "gender_pref": "こだわらない",
        "member_type": "社会人可",
        "meeting_place": "北の橋 橋のたもと",
        "meeting_time": "2024-08-20 09:00",
        "deadline": "2024-08-18",
        "status": "募集中",
        "created_at": "2024-08-05",
        "sns_type": "Twitter/X",
        "sns_account": "@takumi_vol",
    },
    {
        "id": "flag-003",
        "event_id": "evt-003",
        "nickname": "みおり",
        "anxiety_level": "初めてで不安",
        "vibe": "落ち着いて参加したい",
        "reason": "DIYや古い建物に興味があって参加してみたい。でも知らない人ばかりの場所に一人で行くのが怖くて。同じく少し不安に感じている人と一緒に行けたら嬉しい。",
        "group_size": "二人",
        "gender_pref": "同性のみ",
        "member_type": "大学生限定",
        "meeting_place": "市バス 北地区線「旧田中家前」停留所",
        "meeting_time": "2024-09-07 10:00",
        "deadline": "2024-09-05",
        "status": "募集中",
        "created_at": "2024-08-10",
        "sns_type": "",
        "sns_account": "",
    },
    {
        "id": "flag-004",
        "event_id": "evt-004",
        "nickname": "りょう",
        "anxiety_level": "慣れている",
        "vibe": "落ち着いて参加したい",
        "reason": "子ども食堂に関心があって、一度参加してみたかった。穏やかに、でも真剣に地域に貢献したい気持ちです。同じ気持ちの人がいれば嬉しいな。",
        "group_size": "三人",
        "gender_pref": "こだわらない",
        "member_type": "社会人可",
        "meeting_place": "コミュニティセンター ロビー",
        "meeting_time": "2024-08-25 10:30",
        "deadline": "2024-08-23",
        "status": "募集中",
        "created_at": "2024-08-12",
        "sns_type": "Twitter/X",
        "sns_account": "@ryo_local_act",
    },
    {
        "id": "flag-005",
        "event_id": "evt-005",
        "nickname": "あかり",
        "anxiety_level": "初めてで不安",
        "vibe": "ワイワイ参加したい",
        "reason": "伝統工芸って憧れるけど自分一人では絶対行けない。せっかくだから楽しく、テンション上げて参加したい！体験したあとはカフェでも行きませんか？",
        "group_size": "三人以上でワイワイ",
        "gender_pref": "こだわらない",
        "member_type": "大学生限定",
        "meeting_place": "地域文化センター 玄関前",
        "meeting_time": "2024-09-14 13:00",
        "deadline": "2024-09-12",
        "status": "募集中",
        "created_at": "2024-08-15",
        "sns_type": "Instagram",
        "sns_account": "@akari_craft_life",
    },
    {
        "id": "flag-006",
        "event_id": "evt-001",
        "nickname": "けんた",
        "anxiety_level": "慣れている",
        "vibe": "ワイワイ参加したい",
        "reason": "お祭りは毎年行くけど、いつも友達と行ってて今年は地元以外の知り合いを作りたい！大人数でワイワイ楽しみましょう。屋台制覇しましょう！",
        "group_size": "三人以上でワイワイ",
        "gender_pref": "こだわらない",
        "member_type": "社会人可",
        "meeting_place": "市民公園 南口 時計台前",
        "meeting_time": "2024-08-15 17:30",
        "deadline": "2024-08-14",
        "status": "募集中",
        "created_at": "2024-08-02",
        "sns_type": "",
        "sns_account": "",
    },
]


def get_event(event_id: str):
    for event in EVENTS:
        if event["id"] == event_id:
            return event
    return None


def get_flag(flag_id: str):
    for flag in FLAGS:
        if flag["id"] == flag_id:
            return flag
    return None


def get_filtered_flags(anxiety_level: str, category: str, vibe: str):
    """カテゴリーと温度感でフィルタリングしたフラグ一覧を返す"""
    event_ids = {e["id"] for e in EVENTS if e["category"] == category}
    result = [
        f for f in FLAGS
        if f["status"] == "募集中"
        and f["event_id"] in event_ids
        and f["vibe"] == vibe
    ]
    return result


def get_all_active_flags():
    return [f for f in FLAGS if f["status"] == "募集中"]


def get_flags_by_event(event_id: str):
    return [f for f in FLAGS if f["event_id"] == event_id and f["status"] == "募集中"]


# 手を挙げた人のモックデータ
RAISED_HANDS = [
    {
        "id": "raise-001",
        "flag_id": "flag-001",
        "nickname": "さきこ",
        "email": "sakiko@example.com",
        "message": "同じく不安だけど参加してみたいです！一緒に行けたら心強いです。",
        "sns_type": "Instagram",
        "sns_account": "@sakiko_life",
        "status": "pending",
        "created_at": "2024-08-02",
    },
    {
        "id": "raise-002",
        "flag_id": "flag-001",
        "nickname": "ゆい",
        "email": "yui@example.com",
        "message": "地域のお祭り、ずっと気になってました！",
        "sns_type": "Twitter/X",
        "sns_account": "@yui_tan0812",
        "status": "pending",
        "created_at": "2024-08-03",
    },
    {
        "id": "raise-003",
        "flag_id": "flag-002",
        "nickname": "こうへい",
        "email": "kohei@example.com",
        "message": "ボランティア初めてですが、ぜひ参加させてください！",
        "sns_type": "Instagram",
        "sns_account": "@kohei_outdoor",
        "status": "pending",
        "created_at": "2024-08-06",
    },
]


def get_raised_hands(flag_id: str):
    return [r for r in RAISED_HANDS if r["flag_id"] == flag_id]


# 自分が立てた旗のID（モック：ログインユーザーが立てた旗とみなす）
MY_FLAG_IDS = ["flag-003", "flag-005"]


def get_my_flags():
    return [f for f in FLAGS if f["id"] in MY_FLAG_IDS]


# 自分がエントリーした旗のモックデータ（ログインユーザーのエントリー履歴）
MY_ENTRIES = [
    {
        "id": "my-entry-001",
        "flag_id": "flag-001",
        "status": "承認待ち",
        "created_at": "2024-08-04",
    },
    {
        "id": "my-entry-002",
        "flag_id": "flag-004",
        "status": "承認済み",
        "created_at": "2024-08-13",
    },
    {
        "id": "my-entry-003",
        "flag_id": "flag-002",
        "status": "棄却",
        "created_at": "2024-08-06",
    },
]


def get_my_entries():
    result = []
    for entry in MY_ENTRIES:
        flag = get_flag(entry["flag_id"])
        if flag:
            event = get_event(flag["event_id"])
            result.append({**entry, "flag": flag, "event": event})
    return result
