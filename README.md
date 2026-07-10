# LoopSkill Claude Code Marketplace

A curated [Claude Code](https://code.claude.com) plugin marketplace maintained by
[WiseChef](https://wisechef.ai), distributing plugins that connect to the
[LoopSkill](https://app.loopskill.io) registry — a runnable-loop registry for AI
agents (skills, loops, bundles, and personalities) — plus a small set of
standalone skills curated from the same catalog.

## Install

```
/plugin marketplace add wisechef-ai/loopskill-marketplace
```

Then install any plugin listed below, for example:

```
/plugin install loopskill@loopskill
```

## Plugins

| Plugin | Description | License | Registry |
| --- | --- | --- | --- |
| [`loopskill`](./plugins/loopskill) | Connect your agent to the LoopSkill registry — search, install, run verified loops. | MPL-2.0 | [app.loopskill.io/skills/loopskill](https://app.loopskill.io/skills/loopskill) |
| [`super-memory`](./plugins/super-memory) | One-command installer for the full agent memory stack (cognee, LiteLLM proxy, CouchDB, Obsidian vault). | MIT | [app.loopskill.io/skills/super-memory](https://app.loopskill.io/skills/super-memory) |
| [`ruthless-mentor`](./plugins/ruthless-mentor) | Stress-test a plan or decision in attack mode — separate gold from trash and push each to bulletproof. | Apache-2.0 | [app.loopskill.io/skills/ruthless-mentor](https://app.loopskill.io/skills/ruthless-mentor) |
| [`plan-for-goal`](./plugins/plan-for-goal) | Author a goal-execution plan-doc ready to paste into a goal/issue tracker. | Apache-2.0 | [app.loopskill.io/skills/plan-for-goal](https://app.loopskill.io/skills/plan-for-goal) |
| [`llm-wiki-hermes`](./plugins/llm-wiki-hermes) | Karpathy's LLM Wiki pattern: a persistent, compounding knowledge base as interlinked markdown files. | MIT | [app.loopskill.io/skills/llm-wiki-hermes](https://app.loopskill.io/skills/llm-wiki-hermes) |
| [`hub-search-claude-code`](./plugins/hub-search-claude-code) | Discover locally-installed Claude Code skills and community npm plugins before authoring a duplicate. | Apache-2.0 | [app.loopskill.io/skills/hub-search-claude-code](https://app.loopskill.io/skills/hub-search-claude-code) |
| [`xquik`](./plugins/xquik) | Research public X data through Xquik MCP with source provenance and approval-gated write actions. | MIT | [Xquik MCP docs](https://docs.xquik.com/mcp/overview) |

The `loopskill` plugin is the flagship entry: it wires an agent directly into
the LoopSkill registry so it can search, install, and run additional verified
skills and loops beyond the ones bundled here.

## Learn more

- Registry: [app.loopskill.io](https://app.loopskill.io)
- Self-host the registry: [wisechef-ai/loopskill-api](https://github.com/wisechef-ai/loopskill-api)

## Licensing

This repository's scaffolding (marketplace manifest, README, directory
structure) is licensed under [MPL-2.0](./LICENSE). Each plugin retains its own
license as declared in its `plugin.json` — see the table above.
