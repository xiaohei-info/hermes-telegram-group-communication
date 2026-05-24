# Telegram Group Agent Cluster Communicate Protocol

A reusable Hermes skill for running visible, low-noise coordination between multiple agent bots in a shared Telegram group or topic.

This package was extracted from a real working Hermes deployment and sanitized for open-source reuse.
It keeps the protocol itself, but removes local bot handles, bot IDs, profile names, absolute paths, and workspace-specific roster data.

## What this repo contains

- `src/static/SKILL.md` — the sanitized protocol skill
- `src/static/references/` — reusable reference docs that do not depend on your local workspace
- `config/skill-config.example.json` — the template variables you should fill with your own local roles / bot usernames / capability map
- `scripts/render_skill.py` — renders the installable skill package using your config
- `scripts/audit_sensitive_strings.py` — scans the repo or rendered output for local/sensitive strings before publication

## What gets templated

The highest-local sections are rendered from config:
- `references/live-bot-roster.md`
- `references/profile-capability-routing.md`

Everything else is shipped as sanitized static content.

## Quick start

### 1) Clone or copy this repo

Put it somewhere under your code workspace, for example:

```bash
cd /path/to/your/code
# git clone <your-fork-or-local-repo>
```

### 2) Create your local config

Copy the example config:

```bash
cp config/skill-config.example.json config/skill-config.local.json
```

Edit these fields to match your own deployment:
- `workspace_label`
- `profiles_dir`
- `roles[*].role_key`
- `roles[*].display_name`
- `roles[*].telegram_bot_username`
- `roles[*].telegram_bot_id` (optional — leave empty if you do not want to publish/store it)
- `roles[*].has_topics_enabled`
- `roles[*].best_for`
- `roles[*].not_best_for`
- `roles[*].escalate_when`

### 3) Render the skill

```bash
python3 scripts/render_skill.py   --config config/skill-config.local.json   --output dist
```

By default this creates:

```text
dist/telegram-group-agent-cluster-communicate-protocol/
```

### 4) Install into Hermes

Copy the rendered skill into your Hermes skills directory:

```bash
mkdir -p ~/.hermes/skills/autonomous-ai-agents
rm -rf ~/.hermes/skills/autonomous-ai-agents/telegram-group-agent-cluster-communicate-protocol
cp -R dist/telegram-group-agent-cluster-communicate-protocol   ~/.hermes/skills/autonomous-ai-agents/
```

Start a **new Hermes session**, then load the skill:

```text
skill_view(name='telegram-group-agent-cluster-communicate-protocol')
```

## Optional: render directly into a custom install path

```bash
python3 scripts/render_skill.py   --config config/skill-config.local.json   --output ~/.hermes/skills/autonomous-ai-agents
```

If the output directory already contains a skill folder with the same name, delete it first or render into a clean path.

## Pre-publication audit

Before open-sourcing your customized copy, run the built-in audit script against both the repo and the rendered skill output.

### Example: repo audit

```bash
python3 scripts/audit_sensitive_strings.py   --path .   --deny your_company_name   --deny your_project_codename   --deny your_primary_bot_handle   --deny /home/your-user/.hermes
```

### Example: rendered output audit

```bash
python3 scripts/audit_sensitive_strings.py   --path dist/telegram-group-agent-cluster-communicate-protocol   --deny your_real_company_name   --deny your_real_bot_prefix   --deny /home/your-user
```

Use your **actual local sensitive strings** in the denylist.

## Suggested open-source workflow

1. Render from a clean config
2. Audit the repo root
3. Audit the rendered `dist/` package
4. Ask a second reviewer to search for:
   - real bot usernames
   - bot IDs
   - chat IDs / thread IDs
   - personal names / project names
   - absolute local filesystem paths
   - internal-only runtime notes that should be rewritten or removed
5. Only then push or make the repository public

## Notes on runtime limits

This skill can enforce protocol wording, caller anchoring, `reply-fallback`, `[ACK]`, owner nomination, and reporter discipline.

It **cannot** force your Telegram runtime to preserve a true message-level quote-reply if your gateway or tool path only provides topic continuity.
That is why the skill distinguishes:
- `native quote-reply`
- `topic-post`
- `reply-fallback`

## License

MIT
