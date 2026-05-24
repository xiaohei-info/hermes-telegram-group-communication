# Hermes Telegram Group Communication

A reusable Hermes skill for running visible, low-noise communication and coordination between multiple agent bots in a shared Telegram group or topic.

This project packages a real-world Telegram multi-agent coordination protocol into an open-source, deployment-adaptable format. The protocol itself is reusable; local bot rosters, role mappings, and deployment details are rendered from your own config.

## What problem this solves

When multiple agents share a Telegram group or topic, common failure modes appear quickly:

- the wrong bot wakes up because someone casually typed a handle
- the right bot never wakes up because nobody explicitly addressed it
- multiple bots answer the same task and create noise
- conversations fork into several top-level messages and lose task lineage
- nobody knows who owns the task or who should report upstream

This skill standardizes:

- explicit `@mention` wake-ups
- native quote-reply vs topic-post vs `reply-fallback`
- visible `[ACK]` ownership claims
- handoff structure
- upstream reporter nomination
- public coordination discipline with minimal noise

## Who should use this

Use this repo if you:

- run multiple Hermes agents in a shared Telegram group or topic
- want visible, auditable cross-agent coordination instead of hidden tool-only handoffs
- need a protocol that still works when your runtime cannot reliably preserve native message-level reply anchors
- want a reusable skill package you can adapt to your own local role fleet and bot usernames

## What this repo contains

- `src/static/SKILL.md` — the sanitized protocol skill
- `src/static/references/` — reusable reference docs that do not depend on your local workspace
- `config/skill-config.example.json` — the template variables you should fill with your own local roles / bot usernames / capability map
- `scripts/render_skill.py` — renders the installable skill package using your config
- `scripts/audit_sensitive_strings.py` — scans the repo or rendered output for local/sensitive strings before publication
- `CHANGELOG.md` — release notes / packaging history
- `CONTRIBUTING.md` — contribution guidance for protocol/doc changes

## Repository layout

```text
.
├── config/
│   └── skill-config.example.json
├── scripts/
│   ├── audit_sensitive_strings.py
│   └── render_skill.py
├── src/
│   └── static/
│       ├── SKILL.md
│       └── references/
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## What gets templated

The highest-local sections are rendered from config:

- `references/live-bot-roster.md`
- `references/profile-capability-routing.md`

Everything else ships as sanitized static content.

## Quick start

### 1) Clone the repo

```bash
git clone https://github.com/xiaohei-info/hermes-telegram-group-communication.git
cd hermes-telegram-group-communication
```

### 2) Create your local config

```bash
cp config/skill-config.example.json config/skill-config.local.json
```

Edit these fields to match your own deployment:

- `workspace_label`
- `profiles_dir`
- `roles[*].role_key`
- `roles[*].display_name`
- `roles[*].telegram_bot_username`
- `roles[*].telegram_bot_id` *(optional — leave empty if you do not want to publish/store it)*
- `roles[*].has_topics_enabled`
- `roles[*].best_for`
- `roles[*].not_best_for`
- `roles[*].escalate_when`

### 3) Render the skill

```bash
python3 scripts/render_skill.py \
  --config config/skill-config.local.json \
  --output dist
```

This creates:

```text
dist/hermes-telegram-group-communication/
```

### 4) Install into Hermes

```bash
mkdir -p ~/.hermes/skills/autonomous-ai-agents
rm -rf ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication
cp -R dist/hermes-telegram-group-communication \
  ~/.hermes/skills/autonomous-ai-agents/
```

Start a **new Hermes session**, then load the skill:

```text
skill_view(name='hermes-telegram-group-communication')
```

## Optional: render directly into your local Hermes skills tree

```bash
python3 scripts/render_skill.py \
  --config config/skill-config.local.json \
  --output ~/.hermes/skills/autonomous-ai-agents
```

If the output directory already contains a skill folder with the same name, delete it first or render into a clean path.

## Example adaptation workflow

A typical local rollout looks like this:

1. map your role fleet (`routing-specialist`, `backend-specialist`, etc.)
2. fill in local Telegram bot usernames
3. decide whether to include bot IDs at all
4. render the skill
5. install it into your Hermes skills directory
6. start a new Hermes session
7. test one real Telegram handoff using `[PING]`, `[ACK]`, and `reply-fallback`

## Pre-publication audit

Before open-sourcing **your customized copy**, run the built-in audit script against both the repo and the rendered skill output.

### Example: repo audit

```bash
python3 scripts/audit_sensitive_strings.py \
  --path . \
  --deny your_company_name \
  --deny your_project_codename \
  --deny your_primary_bot_handle \
  --deny /home/your-user/.hermes
```

### Example: rendered output audit

```bash
python3 scripts/audit_sensitive_strings.py \
  --path dist/hermes-telegram-group-communication \
  --deny your_real_company_name \
  --deny your_real_bot_prefix \
  --deny /home/your-user
```

Use your **actual local sensitive strings** in the denylist.

## Suggested open-source workflow

1. render from a clean config
2. audit the repo root
3. audit the rendered `dist/` package
4. ask a second reviewer to search for:
   - real bot usernames
   - bot IDs
   - chat IDs / thread IDs
   - personal names / project names
   - absolute local filesystem paths
   - internal-only runtime notes that should be rewritten or removed
5. only then push or make the repository public

## Runtime limits and scope

This skill can enforce:

- protocol wording
- caller anchoring
- `reply-fallback`
- `[ACK]`
- owner nomination
- reporter discipline

It **cannot** force your Telegram runtime to preserve a true message-level quote-reply if your gateway or tool path only provides topic continuity.

That is why the skill distinguishes:

- `native quote-reply`
- `topic-post`
- `reply-fallback`

## FAQ

### Why is `dist/` not committed?

Because the rendered output depends on your local deployment config. The repo stores the reusable static source plus the render script, not one specific deployment snapshot.

### Do I need bot IDs?

No. Bot IDs are optional. If your deployment does not need them, leave them blank in config and do not publish them.

### Can I rename the role keys?

Yes. The example config uses generic names, but you should rename them to match your own role fleet.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
