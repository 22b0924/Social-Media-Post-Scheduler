# Mock posting adapters. Replace with real API calls (tweepy/requests) when ready.
import time

def post_to_twitter(text: str):
    # Simulate network latency & return mock id
    time.sleep(0.3)
    return {"ok": True, "id": f"tw_{int(time.time())}"}

def post_to_linkedin(text: str):
    time.sleep(0.3)
    return {"ok": True, "id": f"li_{int(time.time())}"}

PLATFORM_MAP = {
    "twitter": post_to_twitter,
    "linkedin": post_to_linkedin,
}
