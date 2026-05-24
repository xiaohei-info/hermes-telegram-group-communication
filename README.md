# Hermes Telegram Group Communication

A reusable Hermes skill for running visible, low-noise communication and coordination between multiple agent bots in a shared Telegram group or topic.

This repository is intentionally structured so that the **repository root is also a valid Hermes skill folder**.
That means the fastest install path is:

- clone this repository directly into your Hermes skills directory
- edit a small number of placeholder/reference files
- start a new Hermes session
- load the skill immediately

## Quickest path (recommended)

Clone directly into your Hermes skills directory:

```bash
git clone https://github.com/xiaohei-info/hermes-telegram-group-communication.git   ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication
```

Then edit these files:

- `references/live-bot-roster.md`
- `references/profile-capability-routing.md`

Optional structured source-of-truth file:

- `templates/skill-config.example.json`

After editing, start a **new Hermes session**, then load:

```text
skill_view(name='hermes-telegram-group-communication')
```

## Why this repo can be cloned directly as a skill

The repository root contains the standard Hermes skill layout:

```text
hermes-telegram-group-communication/
├── SKILL.md
├── references/
├── templates/
└── scripts/
```

So if you clone it into:

```text
~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication
```

your Hermes installation already has the correct shape to load it.

## Minimal customization steps

If you want the smallest possible setup effort, you can ignore most of the repo and only update:

### 1. `references/live-bot-roster.md`
Fill in your real:
- profile/role keys
- bot usernames
- optional bot IDs
- topic capability flags

### 2. `references/profile-capability-routing.md`
Adjust:
- which role owns which kind of work
- how escalation should happen in your deployment
- where your local role docs live

That is enough for many deployments.

## Standard clone-to-skill workflow

```bash
# 1) Clone into the Hermes skills directory
git clone https://github.com/xiaohei-info/hermes-telegram-group-communication.git   ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication

# 2) Edit the deployment-specific files
$EDITOR ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication/references/live-bot-roster.md
$EDITOR ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication/references/profile-capability-routing.md

# 3) Start a new Hermes session, then load the skill
```

Load command inside Hermes:

```text
skill_view(name='hermes-telegram-group-communication')
```

## Alternative: keep a local config and regenerate the reference files

If you prefer maintaining role/bot info as structured JSON rather than editing markdown by hand:

```bash
cp templates/skill-config.example.json templates/skill-config.local.json
```

Then update `templates/skill-config.local.json`, and render the two high-locality reference files into a separate output directory:

```bash
python3 scripts/render_skill.py   --config templates/skill-config.local.json   --output /tmp/hermes-telegram-group-communication-rendered
```

Then copy the rendered files back into your installed skill directory if you want to use them there.

## What problem this skill solves

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

## Repository layout

```text
.
├── SKILL.md
├── references/
│   ├── live-bot-roster.md
│   ├── profile-capability-routing.md
│   └── ...
├── templates/
│   └── skill-config.example.json
├── scripts/
│   ├── audit_sensitive_strings.py
│   └── render_skill.py
├── README.md
├── README.zh-CN.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

## Chinese documentation

Chinese guide:
- [README.zh-CN.md](README.zh-CN.md)

## Pre-publication audit for your customized copy

Before open-sourcing **your own modified deployment copy**, run the built-in audit script against the installed skill folder or your working copy.

### Example: audit the working copy

```bash
python3 scripts/audit_sensitive_strings.py   --path .   --deny your_company_name   --deny your_project_codename   --deny your_primary_bot_handle   --deny /home/your-user/.hermes
```

### Example: audit an installed skill folder

```bash
python3 scripts/audit_sensitive_strings.py   --path ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication   --deny your_real_company_name   --deny your_real_bot_prefix   --deny /home/your-user
```

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

### Do I need to run the render script?

No.

For most users, the fastest path is:
- clone into the Hermes skill directory
- edit `references/live-bot-roster.md`
- edit `references/profile-capability-routing.md`
- start a new Hermes session
- load the skill

### Do I need bot IDs?

No. Bot IDs are optional. If your deployment does not need them, omit them.

### Can I rename the role keys?

Yes. The example files use generic names; change them to match your own local role fleet.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
