#!/usr/bin/env bash
# Paced walkthrough of the agent for screen recording (~5-6 min live).
#   ./demo.sh            # live LLM (needs OPENROUTER_API_KEY in .env)
#   ./demo.sh --offline  # heuristic fallbacks, no API calls
set -euo pipefail
cd "$(dirname "$0")"
PY=.venv/bin/python
PACE=${PACE:-2}

banner() { printf '\n\033[1;35m━━ %s ━━\033[0m\n' "$1"; sleep 1; }

banner "State machine (LangGraph)"
cat docs/state_machine.mmd | sed -n '/graph TD/,/classDef/p' | grep -- '-->' | sed 's/^\t/  /'
sleep "$PACE"

banner "Flow 1 — JD file → 3-round screen → borderline suggestions"
$PY chat_cli.py "$@" --pace "$PACE" --script flows/01_jd_full_report.txt
banner "Flow 2 — natural-language search (no JD file)"
$PY chat_cli.py "$@" --pace "$PACE" --script flows/02_natural_language_search.txt
banner "Flow 3 — compare the top 3 side by side"
$PY chat_cli.py "$@" --pace "$PACE" --script flows/03_compare_top3.txt
banner "Flow 4 — why did X rank higher than Y?"
$PY chat_cli.py "$@" --pace "$PACE" --script flows/04_why_ranking.txt
banner "Flow 5 — refine requirements mid-conversation → re-rank → explain changes"
$PY chat_cli.py "$@" --pace "$PACE" --script flows/05_refine_rerank.txt
banner "Flow 6 — interview questions + save with file tools"
$PY chat_cli.py "$@" --pace "$PACE" --script flows/06_interview_questions.txt
