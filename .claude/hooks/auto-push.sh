#!/bin/bash
# Claude Code セッション終了時に自動で git commit & push するスクリプト

cd /Users/kyouyuu/claude || exit 1

export PATH="$HOME/bin:$PATH"

# 変更がなければ何もしない
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
  exit 0
fi

git add -A
git commit -m "Auto-save: $(date '+%Y-%m-%d %H:%M')"
git push origin main
