#!/usr/bin/env python3
"""Search the public skill registries through LoopSkill and print compact results.

Usage:
  loopskill_search.py search "<query>" [--limit N] [--json]
  loopskill_search.py show <install_ref> [--lines N] [--json]

Standard library only. No API key. The API allows 60 requests per minute from
one IP address: on HTTP 429 this script stops with exit code 2 and does not
retry. Set LOOPSKILL_API_BASE to use a self-hosted LoopSkill instance.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API_BASE = os.environ.get("LOOPSKILL_API_BASE", "https://app.loopskill.io").rstrip("/")
USER_AGENT = "loopskill-search-skill/1.0"
TIMEOUT_S = 30

# Lines a person must read before installing a third-party skill.
RISK = re.compile(
    r"(curl|wget|bash\s+-c|sh\s+-c|\beval\b|base64|rm\s+-rf|sudo\b|chmod\s+\+x|"
    r"api[_-]?key|token|secret|password|ssh\b|\.env\b|https?://)",
    re.IGNORECASE,
)


class RateLimited(Exception):
    pass


def _get(path: str, params: dict) -> dict:
    url = f"{API_BASE}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as err:
        if err.code == 429:
            raise RateLimited from err
        if err.code == 404:
            return {"_not_found": True}
        raise


def search(query: str, limit: int) -> dict:
    return _get("/api/skills/metasearch", {"q": query, "page_size": max(1, min(limit, 50))})


def show(install_ref: str) -> dict:
    return _get("/api/skills/metasearch/install", {"install_ref": install_ref})


def format_search(data: dict, limit: int) -> str:
    rows = (data.get("skills") or [])[:limit]
    if not rows:
        return "No results. Write the query as the task, for example 'convert pdf to text'."
    out = []
    for i, r in enumerate(rows, 1):
        flag = "installable" if r.get("installable") else "link only"
        desc = " ".join((r.get("description") or "").split())[:160]
        out.append(
            f"{i}. {r.get('title') or r.get('slug')} [{r.get('source_badge') or r.get('source')}, "
            f"{r.get('quality')}, {flag}]\n   {desc}\n   ref: {r.get('install_ref')}\n   origin: {r.get('origin_url')}"
        )
    degraded = data.get("sources_degraded") or []
    if degraded:
        out.append(f"(No answer in time from: {', '.join(degraded)}. Search again later for those.)")
    return "\n".join(out)


def risk_lines(body: str) -> list[str]:
    return [f"{n}: {line.strip()[:160]}" for n, line in enumerate(body.splitlines(), 1) if RISK.search(line)]


def format_show(data: dict, lines: int) -> str:
    if data.get("_not_found"):
        return "Not found: the source no longer has this skill. Pick the next result."
    body = data.get("body") or ""
    cmds = data.get("commands") or {}
    out = [f"source: {data.get('source')}  origin: {data.get('origin_url')}"]
    if data.get("preview_only"):
        out.append("preview only: install it from its source (see commands.clawhub).")
    for key in ("hermes", "skills_cli", "claude_code", "clawhub"):
        if cmds.get(key):
            out.append(f"install ({key}): {cmds[key]}")
    risky = risk_lines(body)
    out.append(f"--- review before install: {len(risky)} line(s) with commands, URLs or credentials ---")
    out.extend(risky[:40])
    out.append(f"--- SKILL.md (first {lines} lines) ---")
    out.extend(body.splitlines()[:lines])
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Search agent skills across registries (LoopSkill).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--limit", type=int, default=8)
    s.add_argument("--json", action="store_true")
    sh = sub.add_parser("show")
    sh.add_argument("install_ref")
    sh.add_argument("--lines", type=int, default=60)
    sh.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        data = search(args.query, args.limit) if args.cmd == "search" else show(args.install_ref)
    except RateLimited:
        print("Rate limited (60 requests per minute per IP). Wait 60 seconds, then try again.", file=sys.stderr)
        return 2
    except (urllib.error.URLError, TimeoutError, ValueError) as err:
        print(f"Request failed: {err}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(data, indent=2))
    elif args.cmd == "search":
        print(format_search(data, args.limit))
    else:
        print(format_show(data, args.lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
