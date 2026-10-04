---
name: loopskill-search
description: >
  Find an agent skill before you write one. Searches skills.sh, ClawHub, the
  Hermes Skills Hub, LobeHub, browse.sh and curated GitHub skill repos in one
  query, then gives the SKILL.md, the lines to review, and a working install
  command for Hermes, Claude Code, Codex or Cursor. No API key and no signup.
  Use when the user asks "is there a skill for X", "find a skill that does X",
  "search skills.sh / ClawHub / the skills hub", or when you are about to write
  a new skill and a published one can already exist.
version: 1.0.0
author: Adam Krawczyk (adamkrawczyk), WiseChef
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [skills, search, discovery, skills-sh, clawhub, lobehub, install]
    category: productivity
    homepage: https://github.com/wisechef-ai/loopskill-marketplace
---

# LoopSkill Search Skill

Search skills.sh, ClawHub, the Hermes Skills Hub, LobeHub, browse.sh and curated
GitHub skill repositories with one query, and get one ranked list. For a result,
get its SKILL.md, the lines to review, and an install command for Hermes, Claude
Code, Codex or Cursor. This skill does not install anything without the user's
approval, and it does not search code libraries or MCP servers.

## When to Use

- The user asks for a skill: "is there a skill for X", "find a skill that does X".
- The user names a registry: skills.sh, ClawHub, the Hermes Skills Hub, LobeHub.
- You are about to write a new SKILL.md. Search first. A published skill with a
  history is usually better than a new draft.

## Prerequisites

- Python 3.8 or later. The helper script uses the standard library only.
- Network access to `https://app.loopskill.io`. No API key and no account.
- Optional: set `LOOPSKILL_API_BASE` to use a self-hosted LoopSkill instance.

## How to Run

Run the helper script with your shell tool:

```bash
python3 scripts/loopskill_search.py search "rewrite docs in simplified technical english"
python3 scripts/loopskill_search.py show hermes-hub:official-creative-simple-english
```

The path is relative to this skill's directory. Add `--json` to get the raw API
response.

## Quick Reference

| Command | Result |
|---|---|
| `search "<task>" [--limit N]` | Ranked results: title, source, quality, `installable`, `ref`, origin |
| `show <ref> [--lines N]` | Install commands, lines to review, start of the SKILL.md |

The script calls two public endpoints:

| Endpoint | Returns |
|---|---|
| `GET /api/skills/metasearch?q=<task>&page_size=<n>` | `skills` (rank order), `sources_degraded` |
| `GET /api/skills/metasearch/install?install_ref=<ref>` | `body`, `origin_url`, `preview_only`, `commands` |

`commands` has these keys. An empty string means that no command of that type
is available for this skill.

| Key | Command |
|---|---|
| `hermes` | `hermes skills install <url to SKILL.md>` |
| `skills_cli` | `npx skills add https://github.com/<owner>/<repo>/tree/<branch>/<dir>`, or `npx skills add <owner/repo> --skill <name>` for a skill at the repository root (Claude Code, Codex, Cursor, and 40+ other agents) |
| `claude_code` | The `skills_cli` command with `-a claude-code` |
| `clawhub` | `clawhub install <slug>` (ClawHub results only) |

## Procedure

1. Write the query as the task, not as a skill name. "convert pdf to text"
   finds more than "pdf-skill". Run `search`.
2. Pick three candidates or fewer. Prefer `installable` results whose
   description agrees with the task.
3. Run `show` for each candidate. Read the lines in "review before install":
   commands, URLs, and requests for credentials.
4. Give the user, for each candidate: the title, the source, one sentence about
   what it does, the lines to review, and the install command for their agent.
5. CAUTION: Do not install a community skill without the approval of the user.
   A SKILL.md can tell an agent to run shell commands.
6. When the user approves, run the install command for their agent. For Claude Code, use
   `commands.claude_code`. For Codex, Cursor and others, use `commands.skills_cli`
   with `-a <agent>`.

## Pitfalls

- The API accepts 60 requests per minute from one IP address. On HTTP 429 the
  script stops with exit code 2. Wait 60 seconds. Do not retry in a loop.
- A search takes 1 to 3 seconds because it asks the registries live. If
  `sources_degraded` is not empty and you found nothing, search again after 30
  seconds.
- `quality` is `curated` (reviewed by LoopSkill) or `community` (everything
  else, including official skills of other registries). Use `source` to see
  where a skill comes from.
- A "link only" result (for example, a GitHub code-search hit) has no SKILL.md
  that LoopSkill can read. Give the user its origin URL only.
- `show` prints "Not found" when the source no longer has the skill. Pick the
  next result.
- The ranking is a suggestion. Compare the descriptions yourself.

## Verification

```bash
python3 scripts/loopskill_search.py search "simplified technical english" --limit 3
```

The output is a numbered list. One of the results is `simple-english`.
