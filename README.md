# Social Media Post Scheduler (Demo)

# What
Small demo app to schedule social posts and auto-publish via a background scheduler. Uses mock adapters by default.

# Run
cd social-scheduler/backend
python -m venv venv && source venv/bin/activate (or Windows)
pip install -r requirements.txt

# Replace mocks
Edit adapters.py to implement real API calls for Twitter/LinkedIn. 
# Notes
APScheduler runs every 10s for demo responsiveness; in production use an external worker or Celery.
Store real credentials in environment variables or a secrets manager.
