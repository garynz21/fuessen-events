#!/usr/bin/env python3
"""Regenerate fuessen-events.ics from state/events.json.

Rules:
- Only events starting >= (today - 7 days) are written.
- OV film events (category "ov-film") only from today onward.
- Cancelled events are kept as STATUS:CANCELLED so subscribers remove them.
- VALARM (-P14D) on events flagged "alarm": true.
- Fails loudly on duplicate UIDs or malformed entries.
"""

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parent.parent
STATE = REPO / "state" / "events.json"
OUT = REPO / "fuessen-events.ics"
TZ = ZoneInfo("Europe/Berlin")

VTIMEZONE = """BEGIN:VTIMEZONE
TZID:Europe/Berlin
BEGIN:STANDARD
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:CET
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:CEST
END:DAYLIGHT
END:VTIMEZONE"""


def esc(text):
    return (
        str(text)
        .replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\r\n", "\\n")
        .replace("\n", "\\n")
    )


def fold(line):
    """Fold a content line at 75 octets (UTF-8 safe), RFC 5545 3.1."""
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return [line]
    out = []
    cur = b""
    limit = 75
    for ch in line:
        b = ch.encode("utf-8")
        if len(cur) + len(b) > limit:
            out.append(cur.decode("utf-8"))
            cur = b" " + b
            limit = 75
        else:
            cur += b
    if cur:
        out.append(cur.decode("utf-8"))
    return out


def local_dt(iso):
    dt = datetime.fromisoformat(iso)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=TZ)
    return dt.astimezone(TZ)


def fmt(dt):
    return dt.strftime("%Y%m%dT%H%M%S")


def main():
    events = json.loads(STATE.read_text(encoding="utf-8"))
    if not isinstance(events, list):
        sys.exit("state/events.json must be a JSON array")

    uids = [e.get("uid") for e in events]
    dupes = {u for u in uids if uids.count(u) > 1}
    if dupes or None in uids:
        sys.exit(f"Duplicate or missing UIDs: {dupes}")

    now_utc = datetime.now(timezone.utc)
    today = now_utc.astimezone(TZ).date()
    cutoff = today - timedelta(days=7)
    dtstamp = now_utc.strftime("%Y%m%dT%H%M%SZ")

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Gary Lewis//Fuessen Event Check//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:Füssen Events (Gary)",
        "X-WR-TIMEZONE:Europe/Berlin",
        "REFRESH-INTERVAL;VALUE=DURATION:P1D",
        "X-PUBLISHED-TTL:P1D",
    ]
    lines += VTIMEZONE.split("\n")

    written = 0
    for e in sorted(events, key=lambda e: e["start"]):
        start = local_dt(e["start"])
        end = local_dt(e["end"]) if e.get("end") else start + timedelta(hours=2)
        if start.date() < cutoff:
            continue
        if e.get("category") == "ov-film" and start.date() < today:
            continue
        status = {"confirmed": "CONFIRMED", "tentative": "TENTATIVE",
                  "cancelled": "CANCELLED"}.get(e.get("status", "confirmed"), "CONFIRMED")
        lines += [
            "BEGIN:VEVENT",
            f"UID:{e['uid']}",
            f"SEQUENCE:{int(e.get('sequence', 0))}",
            f"DTSTAMP:{dtstamp}",
            f"DTSTART;TZID=Europe/Berlin:{fmt(start)}",
            f"DTEND;TZID=Europe/Berlin:{fmt(end)}",
            f"SUMMARY:{esc(e['title'])}",
        ]
        if e.get("location"):
            lines.append(f"LOCATION:{esc(e['location'])}")
        if e.get("description"):
            lines.append(f"DESCRIPTION:{esc(e['description'])}")
        if e.get("url"):
            lines.append(f"URL:{e['url']}")
        if e.get("category"):
            lines.append(f"CATEGORIES:{esc(e['category'])}")
        lines.append(f"STATUS:{status}")
        lines.append("TRANSP:TRANSPARENT")
        if e.get("alarm") and status != "CANCELLED":
            lines += [
                "BEGIN:VALARM",
                "ACTION:DISPLAY",
                f"DESCRIPTION:{esc('Tickets: ' + e['title'])}",
                "TRIGGER:-P14D",
                "END:VALARM",
            ]
        lines.append("END:VEVENT")
        written += 1

    lines.append("END:VCALENDAR")

    folded = []
    for line in lines:
        folded.extend(fold(line))
    OUT.write_text("\r\n".join(folded) + "\r\n", encoding="utf-8")

    begins = sum(1 for l in lines if l.startswith("BEGIN:"))
    ends = sum(1 for l in lines if l.startswith("END:"))
    if begins != ends:
        sys.exit(f"BEGIN/END mismatch: {begins} vs {ends}")
    print(f"Wrote {OUT.name}: {written} events (of {len(events)} in database)")


if __name__ == "__main__":
    main()
