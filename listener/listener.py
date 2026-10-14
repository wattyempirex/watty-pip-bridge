#!/usr/bin/env python3
"""
AgentMail inbox listener — near-real-time new-mail detection via tight REST polling.

Watches one inbox for new received messages and drops one JSON event file per
new message into the spool directory, where a hook/worker picks it up for
notification. Also maintains a persistent seen-id log so restarts and backup
pollers never double-notify.

Auth: uses AGENTMAIL_API_KEY env var if set; otherwise the Hatch
dynamic-credential surrogate for `custom.agentmail` (works inside Hatch
agent contexts, including background processes started from one).

Env:
  AGENTMAIL_INBOX       inbox address to watch (required)
  AGENTMAIL_API_KEY     API key (optional when running under Hatch)
  AGENTMAIL_POLL_SECS   poll interval seconds (default 45)
  AGENTMAIL_SPOOL_DIR   new-event spool dir (default ./spool/new)
  AGENTMAIL_SEEN_FILE   persistent seen message-id log
  AGENTMAIL_PID_FILE    pid file for the supervisor
  AGENTMAIL_LOG_FILE    log file
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

BASE = "https://api.agentmail.to"
INBOX = os.environ.get("AGENTMAIL_INBOX", "").strip()
POLL_SECS = int(os.environ.get("AGENTMAIL_POLL_SECS", "45"))
SPOOL = os.path.expanduser(os.environ.get(
    "AGENTMAIL_SPOOL_DIR", "./spool/new"))
SEEN = os.path.expanduser(os.environ.get(
    "AGENTMAIL_SEEN_FILE",
    "./seen-ids.txt"))
PIDFILE = os.path.expanduser(os.environ.get(
    "AGENTMAIL_PID_FILE", "./listener.pid"))
LOGFILE = os.path.expanduser(os.environ.get(
    "AGENTMAIL_LOG_FILE", "./listener.log"))

API_KEY = os.environ.get("AGENTMAIL_API_KEY", "").strip()

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
try:
    from dynamic_credentials import add_surrogate_to_request
    HAVE_SURROGATE = True
except Exception:
    HAVE_SURROGATE = False


def log(msg):
    line = f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {msg}"
    print(line, flush=True)
    try:
        with open(LOGFILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def api_get(path):
    """GET against the AgentMail REST API with whichever auth is available."""
    url = BASE + path
    req = urllib.request.Request(url, method="GET")
    if API_KEY:
        req.add_header("Authorization", f"Bearer {API_KEY}")
    elif HAVE_SURROGATE:
        add_surrogate_to_request(req, "custom.agentmail",
                                 allowed_hosts=["api.agentmail.to"])
    else:
        raise RuntimeError("no API key and no surrogate available")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_seen():
    seen = set()
    try:
        with open(SEEN) as f:
            for line in f:
                line = line.strip()
                if line:
                    seen.add(line)
    except FileNotFoundError:
        pass
    return seen


def save_seen(mid):
    with open(SEEN, "a") as f:
        f.write(mid + "\n")


def handle_message(m):
    """Fetch full body and spool one event file. Returns True on success."""
    mid = m["message_id"]
    try:
        full = api_get(f"/v0/inboxes/{urllib.parse.quote(INBOX, safe='')}"
                       f"/messages/{urllib.parse.quote(mid, safe='')}")
    except Exception as e:
        log(f"fetch failed for {mid[:30]}: {e}")
        return False
    event = {
        "message_id": mid,
        "thread_id": full.get("thread_id"),
        "inbox_id": INBOX,
        "timestamp": full.get("timestamp"),
        "from": full.get("from"),
        "subject": full.get("subject"),
        "preview": (full.get("preview") or "")[:500],
        "detected_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    os.makedirs(SPOOL, exist_ok=True)
    # filename-safe id
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in mid)[:120]
    tmp = os.path.join(SPOOL, f".{safe}.tmp")
    dst = os.path.join(SPOOL, f"{safe}.json")
    with open(tmp, "w") as f:
        json.dump(event, f)
    os.replace(tmp, dst)  # atomic publish
    save_seen(mid)
    log(f"new mail spooled: {event['from']} | {event['subject']}")
    return True


def poll_once(seen):
    data = api_get(f"/v0/inboxes/{urllib.parse.quote(INBOX, safe='')}"
                   f"/messages?limit=15")
    fresh = 0
    for m in data.get("messages", []):
        labels = m.get("labels", [])
        if "received" not in labels:
            continue
        mid = m["message_id"]
        if mid in seen:
            continue
        if handle_message(m):
            seen.add(mid)
            fresh += 1
    return fresh


def main():
    if not INBOX:
        print("AGENTMAIL_INBOX is required", file=sys.stderr)
        sys.exit(2)
    os.makedirs(os.path.dirname(PIDFILE), exist_ok=True)
    with open(PIDFILE, "w") as f:
        f.write(str(os.getpid()))
    seen = load_seen()
    log(f"listener started for {INBOX} (poll {POLL_SECS}s, {len(seen)} seen)")
    backoff = POLL_SECS
    while True:
        try:
            n = poll_once(seen)
            backoff = POLL_SECS
            if n:
                log(f"poll ok, {n} new")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                retry = e.headers.get("Retry-After")
                wait = int(retry) if retry and retry.isdigit() else 120
                log(f"rate limited, backing off {wait}s")
                time.sleep(wait)
                continue
            log(f"HTTP error {e.code}, backing off")
            time.sleep(backoff)
            backoff = min(backoff * 2, 600)
            continue
        except Exception as e:
            log(f"poll error: {type(e).__name__}: {str(e)[:200]}")
            time.sleep(backoff)
            backoff = min(backoff * 2, 600)
            continue
        time.sleep(POLL_SECS)


if __name__ == "__main__":
    main()
