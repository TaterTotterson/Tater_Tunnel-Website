#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
WEBSITE_DIR = SCRIPT_DIR.parent
DEFAULT_REPO = "https://github.com/TaterTotterson/Tater_Tunnel.git"
DEFAULT_BRANCH = "main"
DEFAULT_SOURCE_DIR = WEBSITE_DIR / "Tater_Tunnel"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def log(message: str) -> None:
    print(f"[{utc_now()}] {message}", flush=True)


def run(args: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(args, cwd=str(cwd) if cwd else None, text=True, capture_output=True)
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.stderr:
        print(completed.stderr, end="", file=sys.stderr)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
    return completed


def source_dir_from_env() -> Path:
    override = str(os.getenv("TATER_TUNNEL_SOURCE_DIR", "") or "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return DEFAULT_SOURCE_DIR.resolve()


def main() -> None:
    parser = argparse.ArgumentParser(description="Clone or update the Tater Tunnel source used by the website builder.")
    parser.add_argument("--repo", default=os.getenv("TATER_TUNNEL_REPO", DEFAULT_REPO), help="Tater Tunnel git repository URL.")
    parser.add_argument("--branch", default=os.getenv("TATER_TUNNEL_BRANCH", DEFAULT_BRANCH), help="Branch to fetch. Default: main.")
    parser.add_argument("--source-dir", default=str(source_dir_from_env()), help="Local source checkout directory.")
    args = parser.parse_args()

    source_dir = Path(args.source_dir).expanduser().resolve()
    if source_dir == WEBSITE_DIR:
        raise SystemExit("Source directory cannot be the website project root.")

    if (source_dir / ".git").exists():
        log(f"Fetching Tater Tunnel source in {source_dir}")
        run(["git", "fetch", "--quiet", "origin", args.branch], cwd=source_dir)
        run(["git", "checkout", "-B", args.branch, f"origin/{args.branch}"], cwd=source_dir)
        return

    if source_dir.exists() and any(source_dir.iterdir()):
        raise SystemExit(f"{source_dir} exists and is not an empty git checkout. Set TATER_TUNNEL_SOURCE_DIR to a valid checkout.")

    log(f"Cloning Tater Tunnel source to {source_dir}")
    source_dir.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "clone", "--depth", "1", "--branch", args.branch, args.repo, str(source_dir)])


if __name__ == "__main__":
    main()
