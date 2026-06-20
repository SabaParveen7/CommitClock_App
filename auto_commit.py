"""
auto_commit.py
----------------
Watches this project folder and automatically commits + pushes any
changes to GitHub every CHECK_INTERVAL seconds. Free, no paid tools —
just Python (already installed) and Git.

HOW TO USE:
1. Make sure this folder is already a git repo connected to GitHub
   (see GITHUB_SETUP_GUIDE.md, steps 1-5) before running this.
2. Run it in a terminal and leave it running in the background:
       python auto_commit.py
3. Stop it any time with Ctrl+C.

It will only make a commit if something actually changed — it won't
spam empty commits.
"""
import subprocess
import time
from datetime import datetime

CHECK_INTERVAL = 60  # seconds between checks — change if you want


def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def has_changes():
    result = run("git status --porcelain")
    return bool(result.stdout.strip())


def commit_and_push():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    run("git add -A")
    commit = run(f'git commit -m "Auto-update: {timestamp}"')
    print(commit.stdout.strip() or commit.stderr.strip())
    push = run("git push")
    if push.returncode == 0:
        print(f"[{timestamp}] Pushed to GitHub successfully.")
    else:
        print(f"[{timestamp}] Push failed:\n{push.stderr.strip()}")
        print("(Common cause: not logged in / remote not set — see GITHUB_SETUP_GUIDE.md)")


def main():
    print("auto_commit.py running. Watching for changes every "
          f"{CHECK_INTERVAL} seconds. Press Ctrl+C to stop.\n")
    try:
        while True:
            if has_changes():
                print("Change detected...")
                commit_and_push()
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
