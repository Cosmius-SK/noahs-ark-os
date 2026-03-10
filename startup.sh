#!/bin/bash
# ==========================================
# Noah's Ark OS — Codespace Startup Script
# ==========================================
# Run this at the start of every Codespace session.
# Restores runtime JSON files from committed templates.
# Usage: bash startup.sh
# ------------------------------------------

echo "🚀 Noah's Ark OS — Codespace Startup"
echo "======================================"

# ── Step 1: Restore runtime JSON files from templates ------------------
echo ""
echo "📂 Restoring runtime files..."

FILES_RESTORED=0

if [ ! -f "noah_souls.json" ]; then
    if [ -f "noah_souls_template.json" ]; then
        cp noah_souls_template.json noah_souls.json
        echo "   ✅ noah_souls.json restored from template"
        FILES_RESTORED=$((FILES_RESTORED + 1))
    else
        echo "   ⚠️  noah_souls_template.json not found — create it from your souls file"
    fi
else
    echo "   ✅ noah_souls.json already exists"
fi

if [ ! -f "global_history.json" ]; then
    echo '{"global_history": []}' > global_history.json
    echo "   ✅ global_history.json created (empty)"
    FILES_RESTORED=$((FILES_RESTORED + 1))
else
    echo "   ✅ global_history.json already exists"
fi

if [ ! -f "token_ledger.json" ]; then
    echo '[]' > token_ledger.json
    echo "   ✅ token_ledger.json created (empty)"
    FILES_RESTORED=$((FILES_RESTORED + 1))
else
    echo "   ✅ token_ledger.json already exists"
fi

# ── Step 2: Verify .env file -------------------------------------------
echo ""
echo "🔑 Checking API key..."

if [ -f ".env" ]; then
    echo "   ✅ .env file found"
elif [ -n "$GEMINI_API_KEY" ]; then
    echo "   ✅ GEMINI_API_KEY found in environment (Codespaces secret)"
else
    echo "   ⚠️  No .env file and no GEMINI_API_KEY secret found"
    echo "      Create .env with: GEMINI_API_KEY=your_key_here"
fi

# ── Step 3: Show current notebook versions ----------------------------
echo ""
echo "📓 Available notebooks:"
ls *.ipynb 2>/dev/null | sort | tail -5 || echo "   No notebooks found"

# ── Step 4: Show git status -------------------------------------------
echo ""
echo "📋 Git status:"
git status --short 2>/dev/null || echo "   Not a git repo"

echo ""
echo "======================================"
echo "✅ Startup complete. Open your notebook and run all cells."
echo ""
echo "📌 Remember before closing this session:"
echo "   bash commit.sh \"your message here\""
echo "======================================"
