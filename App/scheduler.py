from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone
from .db import get_conn
from .adapters import PLATFORM_MAP

scheduler = BackgroundScheduler()

def publish_due():
    now = datetime.now(timezone.utc)
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, platform, content, post_at FROM posts WHERE status='pending'")
        rows = cur.fetchall()
        for r in rows:
            pid, plat, content, post_at = r
            try:
                # parse post_at stored as ISO string
                post_time = datetime.fromisoformat(post_at)
            except Exception:
                # try relaxed format
                post_time = datetime.strptime(post_at, "%Y-%m-%d %H:%M")
            post_time = post_time.replace(tzinfo=timezone.utc) if post_time.tzinfo is None else post_time
            if post_time <= now:
                results = []
                all_ok = True
                for p in [x.strip().lower() for x in plat.split(",") if x.strip()]:
                    fn = PLATFORM_MAP.get(p)
                    if not fn:
                        results.append(f"{p}:unsupported")
                        all_ok = False
                        continue
                    try:
                        res = fn(content)
                        results.append(f"{p}:ok({res.get('id')})")
                    except Exception as e:
                        results.append(f"{p}:err({str(e)})")
                        all_ok = False
                status = "posted" if all_ok else "failed"
                cur.execute("UPDATE posts SET status=?, result=? WHERE id=?", (status, ";".join(results), pid))
        conn.commit()

def start(interval_seconds: int = 10):
    scheduler.add_job(publish_due, "interval", seconds=interval_seconds, id="publisher", replace_existing=True)
    scheduler.start()
