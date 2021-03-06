import os


# Access log settings

accesslog = os.environ.get("GUNICORN_ACCESSLOG", "-")
timeout = 60 * 5
access_log_format = os.environ.get(
    "GUNICORN_ACCESS_LOG_FORMAT",
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)s %({X-Forwarded-For}i)s',
)
