#!/bin/zsh
# Biweekly Füssen Event Check runner. Called by launchd every Monday 07:00;
# the week-parity check below makes it effectively biweekly (even weeks).
REPO_DIR="/Users/lewis/Projects/events-calender"
cd "$REPO_DIR" || exit 1

week=$(( $(date +%s) / 604800 ))
if (( week % 2 != 0 )); then
  echo "$(date '+%Y-%m-%d %H:%M') off-week (index $week), skipping" >> run.log
  exit 0
fi

export PATH="/Users/lewis/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

echo "===== event check started $(date '+%Y-%m-%d %H:%M') =====" >> run.log
claude -p "$(cat fuessen-event-check.md)" \
  --allowedTools "WebSearch,WebFetch,Read,Write,Edit,Bash(git *),Bash(python3 *)" \
  --max-turns 60 >> run.log 2>&1
echo "===== event check finished $(date '+%Y-%m-%d %H:%M') exit=$? =====" >> run.log
