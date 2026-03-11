#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# vision_log.sh — Append a raw thought to VISION_LOG.md and commit it.
# Usage:
#   bash vision_log.sh "your thought here"
#   bash vision_log.sh "multi-line" "thought" "across args"
#   bash vision_log.sh   (opens nano for longer entries)
# ─────────────────────────────────────────────────────────────────────────────

LOGFILE="VISION_LOG.md"
DATE=$(date "+%d %b %Y")
TIME=$(date "+%H:%M")

if [ ! -f "$LOGFILE" ]; then
  echo "❌ $LOGFILE not found. Are you in the repo root?"
  exit 1
fi

# ── Capture the thought ──────────────────────────────────────────────────────

if [ $# -eq 0 ]; then
  # No args — open nano for longer entry
  TMPFILE=$(mktemp /tmp/vision_entry.XXXXXX)
  echo "# Write your thought below. Save and exit when done (Ctrl+X, Y, Enter)." > "$TMPFILE"
  echo "# Tag line format: ## $DATE — <Tag>" >> "$TMPFILE"
  echo "" >> "$TMPFILE"
  nano "$TMPFILE"
  THOUGHT=$(grep -v '^#' "$TMPFILE" | sed '/^$/d')
  rm "$TMPFILE"
  
  if [ -z "$THOUGHT" ]; then
    echo "⚠️  No content entered. Vision log unchanged."
    exit 0
  fi
  
  echo "" >> "$LOGFILE"
  echo "## $DATE $TIME — Note" >> "$LOGFILE"
  echo "$THOUGHT" >> "$LOGFILE"

else
  # Args provided — join them as a single entry
  THOUGHT="$*"
  echo "" >> "$LOGFILE"
  echo "## $DATE $TIME — Note" >> "$LOGFILE"
  echo "$THOUGHT" >> "$LOGFILE"
fi

# ── Commit ───────────────────────────────────────────────────────────────────

echo "📝 Appended to $LOGFILE"

# Check if we're in a git repo
if git rev-parse --git-dir > /dev/null 2>&1; then
  # Check .env is not staged
  if git check-ignore -q .env; then
    git add "$LOGFILE"
    git commit -m "vision-log: $DATE entry"
    git push
    echo "✅ Vision log committed and pushed."
  else
    echo "⚠️  .env not gitignored — aborting commit. Fix .gitignore first."
  fi
else
  echo "⚠️  Not in a git repo. Entry saved locally only."
fi
