#!/bin/bash
# ==========================================
# Noah's Ark OS — Session Commit Script
# ==========================================
# Run this at the END of every Codespace session.
# Commits notebooks, docs, scripts. Never commits secrets or runtime state.
# Usage: bash commit.sh "your commit message"
# ------------------------------------------

MSG=${1:-"Session checkpoint"}

echo "💾 Noah's Ark OS — Committing session work"
echo "=========================================="
echo "Message: $MSG"
echo ""

# ── Safety: never commit .env or raw JSON state -----------------------
if git check-ignore -q .env 2>/dev/null; then
    echo "   ✅ .env is gitignored — safe"
else
    echo "   ⚠️  WARNING: .env is NOT gitignored — check .gitignore before proceeding"
    exit 1
fi

# ── Stage safe files only --------------------------------------------
echo "📂 Staging files..."

# Notebooks
git add *.ipynb 2>/dev/null && echo "   ✅ Notebooks staged" || echo "   — No notebooks"

# Docs
find . -maxdepth 1 \( -name "*.docx" -o -name "*.xlsx" -o -name "*.pdf" \) | xargs git add 2>/dev/null && echo "   ✅ Docs staged" || echo "   — No docs"

# Scripts
git add *.sh 2>/dev/null && echo "   ✅ Scripts staged" || echo "   — No scripts"

# Templates (souls template is safe — no secrets)
git add *_template.json 2>/dev/null && echo "   ✅ Templates staged" || echo "   — No templates"

# Config and infra
git add .devcontainer/ 2>/dev/null && echo "   ✅ devcontainer staged" || echo "   — No devcontainer"
git add .gitignore 2>/dev/null

# ── Show what's being committed ----------------------------------------
echo ""
echo "📋 Staged changes:"
git diff --staged --name-only

# ── Commit ------------------------------------------------------------
echo ""
git commit -m "$MSG"

if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 Pushing to GitHub..."
    git push
    echo ""
    echo "✅ Done. Session committed and pushed."
else
    echo ""
    echo "⚠️  Nothing to commit or commit failed."
fi

echo "=========================================="
