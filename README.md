# AgentMail inbox listener

Near-real-time new-mail detection via tight REST polling. Drops one JSON event
file per new received message into `./spool/new/` for your own notifier (hook,
cron, or chat bridge) to consume.

## Requirements

- Python 3.10+ stdlib only. No dependencies.

## Usage

```bash
export AGENTMAIL_API_KEY="<your AgentMail API key>"
export AGENTMAIL_INBOX="you@agentmail.to"
# optional:
export AGENTMAIL_POLL_SECS=45        # poll interval
export AGENTMAIL_SPOOL_DIR=./spool/new
export AGENTMAIL_SEEN_FILE=./seen-ids.txt
python3 listener.py
```

The listener writes its PID to `./listener.pid` and logs to `./listener.log`.
Keep it alive with your process supervisor of choice (systemd, cron, etc.) —
it is designed to be restarted freely; the seen-id log prevents double
processing across restarts.

## Event format

Each file in the spool is JSON:

```json
{
  "message_id": "<...>",
  "thread_id": "...",
  "inbox_id": "you@agentmail.to",
  "timestamp": "2026-10-14T18:00:00.000Z",
  "from": "teammate@agentmail.to",
  "subject": "Re: crossval spec",
  "preview": "first 500 chars…",
  "detected_at": "2026-10-14T18:00:31"
}
```

Fetch the full body with `GET /v0/inboxes/{inbox}/messages/{message_id}`.

## Notes

- A fresh credential is used per poll; the process never stores your key.
- HTTP 429 responses are honored via `Retry-After` with exponential backoff.
- Mark messages read via `PATCH /v0/inboxes/{inbox}/messages/{id}`
  `{"add_labels": ["read"], "remove_labels": ["unread"]}` after handling.
