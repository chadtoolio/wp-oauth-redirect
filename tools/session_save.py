#!/usr/bin/env python3
"""Session Handoff Tool — saves current working context to CONTEXT.md. Run at end of each coding session before switching computers."""
import subprocess, datetime, socket, sys
from pathlib import Path

def get_git_status():
    try:
        branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
        changed = subprocess.check_output(["git", "diff", "--name-only"], text=True).strip()
        staged = subprocess.check_output(["git", "diff", "--cached", "--name-only"], text=True).strip()
        last_commit = subprocess.check_output(["git", "log", "-1", "--pretty=%s"], text=True).strip()
        return branch, changed, staged, last_commit
    except subprocess.CalledProcessError:
        return "unknown", "", "", ""

def save_context(repo_path=None):
    if repo_path is None:
        repo_path = Path.cwd()
    branch, changed, staged, last_commit = get_git_status()
    computer = socket.gethostname()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"
=== Session Handoff Tool ===
Repo: {repo_path.name}
Branch: {branch}
Computer: {computer}
Time: {timestamp}
")
    current_work = input("What are you currently working on?
> ").strip()
    accomplished = input("
What did you accomplish this session?
> ").strip()
    next_steps = input("
What are the next steps? (comma-separated)
> ").strip()
    blockers = input("
Any blockers or open questions? (Enter to skip)
> ").strip()
    resume_prompt = input("
Write a short Claude resume prompt for next session:
> ").strip()
    next_list = "
".join(f"- [ ] {s.strip()}" for s in next_steps.split(","))
    changed_files = "
".join(f"- {f}" for f in changed.splitlines()) if changed else "_None_"
    staged_files = "
".join(f"- {f}" for f in staged.splitlines()) if staged else "_None_"
    context = f"""# Session Context -- {repo_path.name}

## Last Updated
{timestamp} | Computer: {computer} | Chad

## Git State
- **Branch:** {branch}
- **Last Commit:** {last_commit}
- **Modified Files:**
{changed_files}
- **Staged Files:**
{staged_files}

## Current State
{current_work}

## What Was Accomplished
{accomplished}

## Next Steps
{next_list}

## Open Questions / Blockers
{blockers if blockers else '_None_'}

## Resume Prompt for Claude
{resume_prompt}
"""
    context_file = repo_path / "CONTEXT.md"
    context_file.write_text(context, encoding="utf-8")
    print(f"
Context saved to {context_file}")
    if input("
Auto-commit CONTEXT.md to Git? (y/n) > ").strip().lower() == "y":
        subprocess.run(["git", "add", "CONTEXT.md"])
        subprocess.run(["git", "commit", "-m", f"chore: session handoff [{computer}] {timestamp}"])
        subprocess.run(["git", "push"])
        print("Pushed to GitHub")

if __name__ == "__main__":
    save_context(Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd())
