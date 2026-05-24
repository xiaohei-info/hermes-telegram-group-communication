#!/usr/bin/env python3
import argparse
import json
import pathlib
import shutil

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
STATIC_ROOT = REPO_ROOT / 'src' / 'static'


def write(path: pathlib.Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def render_roster(config: dict) -> str:
    lines = [
        '# Live Telegram Bot Roster For This Deployment',
        '',
        'You can edit this file directly for local use; rendering from JSON is optional.',
        'If you do use a structured local config, keep this file aligned with it. Verify every bot username, bot ID, and capability flag against your current Telegram runtime before relying on it.',
        '',
        '## Shared-skill visibility note',
        '',
        '- Adjust this section to match how your own Hermes profiles load shared skills.',
        '- If you do not maintain a central shared-skills directory, rewrite this note accordingly.',
        '',
        '## Verified addressable bots',
        '',
    ]
    for role in config['roles']:
        lines.append(f"- `{role['role_key']}` -> `@{role['telegram_bot_username']}`")
        lines.append(f"  - display_name: `{role['display_name']}`")
        if role.get('telegram_bot_id'):
            lines.append(f"  - bot_id: `{role['telegram_bot_id']}`")
        if role.get('has_topics_enabled'):
            lines.append(f"  - has_topics_enabled: `{role['has_topics_enabled']}`")
        lines.append('')
    lines += [
        '## Operational reminders',
        '',
        '- Re-verify usernames after token rotation, bot replacement, or Telegram-side configuration changes.',
        '- If your deployment does not expose bot IDs publicly, omit them from config and from this rendered file.',
    ]
    return '\n'.join(lines).rstrip() + '\n'


def render_profile_routing(config: dict) -> str:
    roles = config['roles']
    profiles_dir = config.get('profiles_dir', '<profiles_dir>')
    lines = [
        '# Profile Capability Routing Reference',
        '',
        'Use this reference when an agent needs to decide **which other agent to @mention** for help in a Telegram group.',
        '',
        'You can edit this file directly for local use; rendering from JSON is optional. It gives a fast routing map, but it does not replace reading the underlying role docs when boundaries are important.',
        '',
        '## Primary rule',
        '',
        'Before asking another agent to act, prefer this order:',
        '1. identify the real problem type',
        '2. map it to the most relevant profile capability',
        '3. pick the **smallest sufficient specialist set**',
        '4. only expand to more agents if the first specialist explicitly needs another boundary crossed',
        '',
        'Do **not** start by mentioning many bots “just in case”.',
        '',
        '## Quick routing map',
        '',
    ]
    for role in roles:
        lines.append(f"### `{role['role_key']}`")
        lines.append('Best for:')
        for item in role.get('best_for', []):
            lines.append(f'- {item}')
        nb = role.get('not_best_for', [])
        if nb:
            lines.append('')
            lines.append('Not best for:')
            for item in nb:
                lines.append(f'- {item}')
        ew = role.get('escalate_when', [])
        if ew:
            lines.append('')
            lines.append(f"Escalate to {role['role_key']} when:")
            for item in ew:
                lines.append(f'- {item}')
        lines.append('')
    lines += [
        '## Suggested decision pattern in-group',
        '',
        'Before mentioning another bot, mentally ask:',
        '1. What exact capability do I need that I do not already have?',
        '2. Which role doc most clearly owns that capability?',
        '3. Is this a direct request, a review gate, a verification gate, or a decomposition request?',
        '4. Can I keep the request bounded to one branch instead of expanding the whole graph?',
        '5. If the target later expands again, who still owns the parent branch?',
        '',
        '## Source basis',
        '',
        f"Derived from role definitions under: `{profiles_dir}`",
    ]
    for role in roles:
        lines.append(f"- `{profiles_dir}/{role['role_key']}/SOUL.md`")
    lines += [
        '',
        'Use this file as the quick routing sheet; read the underlying role docs directly when the boundary is important or disputed.',
    ]
    return '\n'.join(lines).rstrip() + '\n'


def main():
    ap = argparse.ArgumentParser(description='Render the Telegram coordination skill from local config.')
    ap.add_argument('--config', required=True, help='Path to local JSON config')
    ap.add_argument('--output', required=True, help='Output directory (repo root for rendered dist or direct install parent)')
    args = ap.parse_args()

    config = json.loads(pathlib.Path(args.config).read_text())
    skill_name = config.get('skill_name', 'hermes-telegram-group-communication')
    output_root = pathlib.Path(args.output).expanduser().resolve()

    if output_root.name == skill_name:
        skill_root = output_root
    else:
        skill_root = output_root / skill_name

    if skill_root.exists():
        shutil.rmtree(skill_root)
    shutil.copytree(STATIC_ROOT, skill_root)

    write(skill_root / 'references' / 'live-bot-roster.md', render_roster(config))
    write(skill_root / 'references' / 'profile-capability-routing.md', render_profile_routing(config))

    print(f'Rendered skill to: {skill_root}')


if __name__ == '__main__':
    main()
