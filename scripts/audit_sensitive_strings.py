#!/usr/bin/env python3
import argparse
import pathlib
import re
import sys

DEFAULT_EXTS = {'.md', '.txt', '.json', '.yaml', '.yml', '.py'}


def iter_files(root: pathlib.Path):
    for path in root.rglob('*'):
        if path.is_file() and path.suffix.lower() in DEFAULT_EXTS:
            yield path


def main():
    parser = argparse.ArgumentParser(description='Scan a repo or rendered skill for local/sensitive strings.')
    parser.add_argument('--path', required=True, help='Root path to scan')
    parser.add_argument('--deny', action='append', default=[], help='Literal string or regex pattern to flag')
    parser.add_argument('--regex', action='store_true', help='Treat deny values as regex patterns')
    args = parser.parse_args()

    root = pathlib.Path(args.path).expanduser().resolve()
    if not root.exists():
        print(f'path not found: {root}', file=sys.stderr)
        return 2

    findings = []
    for file in iter_files(root):
        text = file.read_text(errors='ignore')
        lines = text.splitlines()
        for pat in args.deny:
            if args.regex:
                for match in re.finditer(pat, text, flags=re.MULTILINE):
                    line_no = text.count('\n', 0, match.start()) + 1
                    excerpt = lines[line_no - 1] if 0 < line_no <= len(lines) else ''
                    findings.append((file, line_no, pat, excerpt[:200]))
            else:
                for line_no, line_text in enumerate(lines, start=1):
                    if pat in line_text:
                        findings.append((file, line_no, pat, line_text[:200]))

    if findings:
        print('Sensitive/localization audit findings:')
        for file, line_no, pat, excerpt in findings:
            print(f'- {file}:{line_no} | matched={pat!r} | {excerpt}')
        return 1

    print(f'No denylist matches under {root}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
