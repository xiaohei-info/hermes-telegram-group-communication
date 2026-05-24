# Hermes Telegram Group Communication

Languages: [English](README.md) | [简体中文](README.zh-CN.md)


Hermes Telegram Group Communication is a reusable Hermes skill for visible, low-noise communication and coordination between multiple agent bots in a shared Telegram group or topic.

This repository is intended for Hermes users who want a standard operating protocol for multi-agent Telegram collaboration: explicit wake-ups, visible ownership, disciplined handoffs, and auditable reporting chains.

## Overview

When several agents share one Telegram group or topic, coordination often breaks down in predictable ways:

- the wrong bot wakes up because someone casually typed a handle
- the correct bot never wakes up because nobody explicitly addressed it
- multiple bots answer the same task and create noise
- conversations lose message-level lineage and become hard to audit
- nobody knows who owns the task or who should report upstream

This skill provides a common protocol for those situations.

## Expected outcomes

After this skill is installed and localized for your deployment, it helps produce:

- clearer wake-up behavior, because the target bot is explicitly addressed
- lower group noise, because duplicate replies and ambiguous handoffs are reduced
- visible task lineage, because native quote-reply, topic-post, and `reply-fallback` are treated as distinct coordination modes
- explicit ownership, because bots are expected to acknowledge, claim, hand off, and nominate an upstream reporter
- easier debugging, because humans can inspect the public thread and see where coordination failed
- better portability across fleets, because the protocol can be reused even when local role rosters and bot handles differ

## Prerequisites

Before using this skill, make sure your Telegram and Hermes environment is capable of group-based multi-agent coordination.

### 1. Create the Telegram bots you plan to use

Each participating agent/profile needs its own Telegram bot. Keep the bot token available for the matching Hermes profile.

### 2. Enable bot-to-bot communication where required

If your Telegram / gateway / multi-agent runtime requires an explicit **bot-to-bot communication** setting, enable it for every participating bot.

This skill assumes that bots can visibly coordinate with other bots in the same shared group/topic when the platform and gateway configuration allow it.

### 3. Disable Telegram group privacy mode

For every bot that needs to react to group messages and `@mentions`, disable **Group Privacy** / privacy mode.

Why this matters:

- if privacy mode stays enabled, the bot may not receive ordinary group messages
- other agents may not be visible to it in practice
- Hermes gateway may not receive the group `@mention` events needed to trigger the correct bot

In practical terms: if privacy mode is still on, the protocol may be correct but the message may never reach Hermes.

### 4. Add the bots to the target Telegram group or topic workspace

Make sure the intended bots are actually present in the shared group and, if you use Telegram topics, in the correct operational workspace context.

### 5. Configure each participating Hermes profile

For each profile that should use Telegram group coordination:

- set the correct Telegram bot token in that profile
- configure the profile's Telegram settings according to your deployment
- ensure the profile can load this skill from its accessible skill path

### 6. Restart the corresponding Hermes profile gateway

After changing Telegram bot settings, profile config, or local skill files, restart the corresponding Hermes gateway/profile runtime before testing.

A file change alone does not guarantee the running gateway has picked up:

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

The repository root already contains a valid Hermes skill layout:

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

## Standard usage flow

```bash
# 1) Clone into the Hermes skills directory
git clone https://github.com/xiaohei-info/hermes-telegram-group-communication.git \
  ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication

# 2) Edit the two deployment-specific reference files
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

This is an **optional advanced path**, not the default path.

## Verification checklist

Before relying on the skill in a real Telegram group workflow, verify:

- the bots were created and added to the correct Telegram group/topic
- bot-to-bot communication is enabled where your deployment requires it
- Telegram group privacy mode is disabled for the participating bots
- the correct Telegram bot tokens are configured in the matching Hermes profiles
- the corresponding Hermes gateways were restarted after config changes
- the two local reference files were updated with your real roster/routing information
- a new Hermes session can load `skill_view(name='hermes-telegram-group-communication')`
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

For Chinese documentation, see [README.zh-CN.md](README.zh-CN.md).

## Runtime scope and limits

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
