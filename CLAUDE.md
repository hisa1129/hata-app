# 旗アプリ — Claude Code 作業ガイド

> このファイルはClaude Codeがセッション開始時に自動で読み込む作業ガイドです。
> 実装に入る前に **`docs/design.md`** も必ず合わせて読んでください。
> 「何を作るか・なぜそうするか」は design.md に、「どう作るか」はこのファイルに書いてあります。

---

## プロジェクト概要

県外から進学してきた大学生が地域のイベントに一緒に行く仲間を見つけるためのWebアプリ。
「旗」という仕組みで、気持ちの合う人とマッチングする。詳細は `docs/design.md` を参照。

- **GitHub:** https://github.com/hisa1129/hata-app
- **本番URL:** https://hata-app.onrender.com

---

## 現在の状況

> **⚠️ ここはステップ・フェーズの切り替わり時に必ず更新する**

- **現在地:** Step 1-B 着手前（Phase B-0 から開始）
- **直前に完了したこと:** Step 1-A（モックUI全画面の実装）
- **次にやること:** Gitタグ打ち → Supabase接続 → モックデータ差し替え

---

## 技術スタック

| レイヤー | 技術 |
|---|---|
| バックエンド | FastAPI（Python 3.9.6） |
| テンプレート | Jinja2 |
| CSS | Tailwind CSS（CDN版） |
| DB | Supabase（PostgreSQL） |
| デプロイ | Render（GitHub連携・自動デプロイ） |
| Python仮想環境 | venv |

---

## 環境構築・起動

```bash
# 仮想環境の有効化
source venv/bin/activate

# 依存インストール
pip install -r requirements.txt

# ローカル起動
uvicorn main:app --reload

# 依存を追加した後
pip freeze > requirements.txt
```

---

## ファイル構成と役割

```
main.py          # FastAPIアプリ本体・全ルート定義
mock_data.py     # モックデータ（Step 1-B完了後は削除する）
database.py      # Supabaseクライアント・DB操作関数（Step 1-Bで作成）
requirements.txt
.env             # 環境変数（Gitに含めない）
.env.example     # 項目名のみ記載したサンプル
CLAUDE.md        # このファイル
docs/design.md   # 設計書（仕様・思想・ロードマップ）
static/          # 静的ファイル（画像等）
templates/       # Jinja2テンプレート
```

---

## コーディング規約

- ルートは `main.py` に集約する（ファイルを分けない）
- DB操作は `database.py` の関数を通じて行う（`main.py` に直書きしない）
- テンプレートは `templates/` の既存ディレクトリ構造に従う
- 環境変数は必ず `.env` から取得する（コードにハードコードしない）
- Tailwindは CDN版のユーティリティクラスのみ使用する（カスタムクラス追加不可）

---

## やってはいけないこと

- `.env` を Git にコミットしない
- `mock_data.py` への新しい依存を増やさない（DB実装移行中のため）
- `main.py` に DB操作のロジックを直書きしない（`database.py` を経由する）
- Tailwind のカスタムクラスを追加しない（CDN版では動作しない）
- `docs/archive/` 内のファイルを参照しない（古い仕様書のアーカイブ。現行仕様は `docs/design.md` のみ）

---

## このファイルの更新ルール

**必ず見直すタイミング：ステップまたはフェーズの切り替わり時**

ステップ・フェーズが切り替わるとき、上部の「現在の状況」セクションを必ず更新する。
あわせて、技術スタック・禁止事項・コーディング規約に変更がないかも確認する。

**随時更新するタイミング：**
- 「やってはいけないこと」が新たに判明したとき（失敗の教訓として追記）
- コーディング規約が決まったとき
- よく使うコマンドが変わったとき
- 技術スタックに変更が入ったとき
