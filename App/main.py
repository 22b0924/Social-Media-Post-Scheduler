from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db, get_conn
from .models import ScheduleRequest
from .scheduler import start
import os, json, datetime

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# initialize DB and scheduler
init_db()
start(interval_seconds=10)   # check every 10s for demo

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
INDEX_HTML = os.path.join(TEMPLATES_DIR, "index.html")

@app.get("/", response_class=HTMLResponse)
def index():
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/schedule")
async def schedule(req: ScheduleRequest):
    created = datetime.datetime.utcnow().isoformat()
    # store post
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO posts (platform, content, post_at, created_at, status) VALUES (?, ?, ?, ?, ?)",
            (req.platform, req.content, req.post_at, created, "pending")
        )
        conn.commit()
        return {"ok": True, "id": cur.lastrowid}

@app.get("/posts")
def posts():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, platform, content, post_at, created_at, status, result FROM posts ORDER BY id DESC")
        rows = cur.fetchall()
        keys = ["id","platform","content","post_at","created_at","status","result"]
        out = [ dict(zip(keys, r)) for r in rows ]
        return out
