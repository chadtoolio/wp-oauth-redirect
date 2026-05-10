#!/usr/bin/env python3
"""Reads CONTEXT.md and prints the Claude resume prompt."""
from pathlib import Path
import sys

repo = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
context_file = repo / "CONTEXT.md"
if not context_file.exists():
    print("No CONTEXT.md found. Run tools/session_save.py at end of your next session.")
    sys.exit(1)
ctx = context_file.read_text(encoding="utf-8")
print(ctx)
if "## Resume Prompt for Claude" in ctx:
    prompt = ctx.split("## Resume Prompt for Claude")[-1].strip().strip("`").strip()
    print("

=== PASTE THIS INTO CLAUDE ===
")
    print(prompt)
