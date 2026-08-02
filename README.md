# Füssen Events, Self-Updating Calendar

Automated biweekly pipeline: Claude Code researches events around Füssen, maintains
`state/events.json` as the source of truth, and regenerates `fuessen-events.ics`.
Calendar apps subscribe to the raw URL of the ICS and stay in sync automatically.

## Subscribe (one time)

Raw ICS URL:

    https://raw.githubusercontent.com/garynz21/fuessen-events/main/fuessen-events.ics

- **Google Calendar:** Settings > Add calendar > From URL > paste the URL.
- **Apple Calendar (Mac):** File > New Calendar Subscription, paste URL, set auto-refresh to every day.
- **iPhone:** Settings > Apps > Calendar > Calendar Accounts > Add Account > Other > Add Subscribed Calendar.

## How it runs

- launchd job `com.garylewis.fuessen-event-check` fires every Monday 07:00,
  `scripts/run-check.sh` skips odd weeks so the check is biweekly.
- The runner executes `claude -p "$(cat fuessen-event-check.md)"` headless with
  pre-approved tools (web research, file edits, git).
- The run updates `state/events.json` (stable UIDs, SEQUENCE bumps on changes,
  cancellations kept as status cancelled) and runs `scripts/generate_ics.py`
  to rewrite the ICS, then commits and pushes.
- Human-readable run summaries land in `run.log` (not committed).

## Files

| File | Purpose |
|---|---|
| `fuessen-event-check.md` | The full standalone prompt: interest profile, sources, update algorithm |
| `state/events.json` | Event database, source of truth, never deletes history |
| `scripts/generate_ics.py` | Deterministic JSON to ICS generator (validates UIDs, folding, VTIMEZONE) |
| `scripts/run-check.sh` | Biweekly launchd entry point |
| `fuessen-events.ics` | Generated output, the file calendars subscribe to |

## Maintenance

- Change interests: edit the interest profile in `fuessen-event-check.md`. Nothing else changes.
- Run manually: `cd ~/Projects/events-calender && ./scripts/run-check.sh` (or run `claude` interactively and say "run the fuessen event check").
- If a run misbehaves: check `run.log`.
- Do not rename the repo or the ICS file; the raw URL is what every device subscribes to.
