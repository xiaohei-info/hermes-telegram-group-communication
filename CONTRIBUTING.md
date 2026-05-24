# Contributing

Thanks for contributing.

This repository is not a generic Telegram bot library; it is a reusable Hermes skill package for **public multi-agent coordination discipline**.

## Contribution priorities

Good contributions usually improve one of these:

- protocol clarity
- template quality
- deployment portability
- public coordination safety
- installability for new Hermes users
- sensitivity / sanitization guidance

## Before opening a PR

Please check:

1. does this improve the reusable protocol rather than one local deployment?
2. does it preserve the distinction between:
   - native quote-reply
   - topic-post
   - `reply-fallback`
3. does it avoid introducing local bot handles, local paths, or private deployment notes?
4. if you changed templates or docs, did you update the README and/or CHANGELOG when needed?

## Local development flow

```bash
cp config/skill-config.example.json config/skill-config.local.json
# edit config/skill-config.local.json
python3 scripts/render_skill.py --config config/skill-config.local.json --output dist
```

If you are changing publication or sanitization logic, also run an audit:

```bash
python3 scripts/audit_sensitive_strings.py --path . --deny your_local_string
python3 scripts/audit_sensitive_strings.py --path dist/hermes-telegram-group-communication --deny your_local_string
```

## Sensitive data rules

Do **not** commit:

- real bot usernames unless they are intentionally public examples
- bot tokens
- real bot IDs unless explicitly intended for publication
- chat IDs / topic IDs / thread IDs from private deployments
- local filesystem paths tied to one machine or user
- internal-only incident notes that should instead be generalized

## Style guidance

Prefer:

- explicit trigger conditions
- concise operational language
- examples that are class-shaped, not diary-shaped
- deployment-generic wording where possible

Avoid:

- vague motivational prose
- hidden local assumptions
- examples that only make sense in one private workspace
- turning runtime limitations into protocol claims without labeling them clearly

## Review checklist

Before merging, ask:

- is the skill still understandable to a stranger who was not part of the original deployment?
- are local values still templated?
- is the protocol more reliable after this change, or just longer?
- would this change create noise or ambiguity in a real Telegram agent cluster?
