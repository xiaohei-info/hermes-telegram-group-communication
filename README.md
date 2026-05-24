# Hermes Telegram Group Communication

A reusable Hermes skill for visible, low-noise communication and coordination between multiple agent bots in a shared Telegram group or topic.

This repository is published in a **directly loadable Hermes skill layout**. The repository root is itself a valid skill directory, so the normal installation path is to clone it directly into your Hermes skills tree, update a small number of deployment-specific files, start a new Hermes session, and load the skill.

## What this skill is for

Use this skill when:

- multiple agent bots share one Telegram group or topic
- you want visible, auditable coordination instead of hidden internal-only handoffs
- you need clear wake-up rules, owner rules, handoff rules, and reporting rules
- you want a standard way to distinguish native quote-reply, topic-post, and `reply-fallback`

It is designed to reduce common multi-agent Telegram failure modes:

- the wrong bot wakes up because someone casually typed a handle
- the right bot never wakes up because nobody explicitly addressed it
- multiple bots answer the same task and create noise
- a conversation forks into several top-level messages and loses task lineage
- nobody knows who owns the task or who should report upstream

## Prerequisites

Before using this skill, make sure your Telegram + Hermes environment is actually capable of group-based multi-agent coordination.

### 1. Create the Telegram bots you plan to use

For each participating agent/profile, create a Telegram bot and keep the bot token available for the matching Hermes profile.

### 2. Enable bot-to-bot communication for your deployment

If your Telegram / gateway / multi-agent runtime requires an explicit **bot-to-bot communication** setting, enable it for every participating bot.

This skill assumes that bots can visibly coordinate with other bots in the same shared group/topic when the platform and gateway configuration allow it.

### 3. Disable Telegram group privacy mode

For every bot that needs to react to group messages and `@mentions`, disable **Group Privacy** / privacy mode.

Why this matters:

- if privacy mode stays enabled, the bot may not receive ordinary group messages
- other agents may not be visible to it in practice
- Hermes gateway may not receive the group `@mention` events needed to trigger the correct bot

In practical terms: if privacy mode is still on, this skill can be perfectly written and still fail operationally because the message never reaches Hermes.

### 4. Add the bots to the target Telegram group or topic workspace

Make sure the intended bots are actually present in the shared group and, if you use Telegram topics, in the correct operational workspace context.

### 5. Configure each participating Hermes profile

For each profile that should use Telegram group coordination:

- set the correct Telegram bot token in that profile
- configure the profile's Telegram settings according to your deployment
- ensure the profile can load the shared skill library or has this skill installed directly under its accessible skill path

### 6. Restart the corresponding Hermes profile gateway

After changing Telegram bot settings, profile config, or local skill files, restart the corresponding Hermes gateway/profile runtime before testing.

This is important because a config file change alone does not guarantee the running gateway has picked up:

- the new bot token
- updated Telegram settings
- new skill files
- changed routing/reference files

## Installation

### Recommended installation path

Clone this repository directly into your Hermes skills directory:

```bash
git clone https://github.com/xiaohei-info/hermes-telegram-group-communication.git \
  ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication
```

This works because the repository root already contains the standard Hermes skill layout:

```text
hermes-telegram-group-communication/
├── SKILL.md
├── references/
├── templates/
└── scripts/
```

## Minimum required local customization

For most users, the minimum setup is to edit **two files**.

### 1. `references/live-bot-roster.md`

Update this file with your real:

- role/profile keys
- bot usernames
- optional bot IDs
- topic capability flags

### 2. `references/profile-capability-routing.md`

Update this file with your real:

- role ownership boundaries
- escalation paths
- profile capability mapping
- local role-document paths (if you use them)

For many deployments, editing those two files is enough.

## Fast start workflow

```bash
# 1) Clone into the Hermes skills directory
git clone https://github.com/xiaohei-info/hermes-telegram-group-communication.git \
  ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication

# 2) Edit the two local deployment files
$EDITOR ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication/references/live-bot-roster.md
$EDITOR ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication/references/profile-capability-routing.md

# 3) Restart the relevant Hermes profile gateway(s)
#    (use your normal Hermes gateway/profile restart flow)

# 4) Start a new Hermes session, then load the skill
```

Load command inside Hermes:

```text
skill_view(name='hermes-telegram-group-communication')
```

## Optional structured configuration workflow

If you prefer maintaining deployment-specific role/bot information as structured JSON instead of editing markdown by hand:

```bash
cp templates/skill-config.example.json templates/skill-config.local.json
```

Then update `templates/skill-config.local.json` and render the high-locality reference files into a separate output directory:

```bash
python3 scripts/render_skill.py \
  --config templates/skill-config.local.json \
  --output /tmp/hermes-telegram-group-communication-rendered
```

Then copy the rendered files back into your installed skill directory if you want to use them there.

This is an **optional advanced path**, not the required default path.

## Verification checklist

Before relying on the skill in a real Telegram group workflow, verify:

- the bots were created and added to the correct Telegram group/topic
- bot-to-bot communication is enabled where your deployment requires it
- Telegram group privacy mode is disabled for the participating bots
- the correct Telegram bot tokens are configured in the matching Hermes profiles
- the corresponding Hermes gateways were restarted after config changes
- the two local reference files were updated with your real roster/routing information
- a new Hermes session can load:
  - `skill_view(name='hermes-telegram-group-communication')`
- a real test `@mention` in the group reaches the intended bot

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
python3 scripts/audit_sensitive_strings.py \
  --path . \
  --deny your_company_name \
  --deny your_project_codename \
  --deny your_primary_bot_handle \
  --deny /home/your-user/.hermes
```

### Example: audit an installed skill folder

```bash
python3 scripts/audit_sensitive_strings.py \
  --path ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication \
  --deny your_real_company_name \
  --deny your_real_bot_prefix \
  --deny /home/your-user
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

For most users, the default path is:

- clone into the Hermes skill directory
- edit `references/live-bot-roster.md`
- edit `references/profile-capability-routing.md`
- restart the relevant Hermes gateway/profile
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
