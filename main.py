#!/usr/bin/env python3
"""Museum of the Year 3000 — one-line museum label entry.

Entry (170 chars, one line):
Plastic Fork (c. 2025): Humans stabbed food with this, threw it away
after one meal, then bought a metal one that did the exact same thing.
Scientists are still confused.
"""

import os
import sys

ENTRY = (
    "Plastic Fork (c. 2025): Humans stabbed food with this, threw it away "
    "after one meal, then bought a metal one that did the exact same thing. "
    "Scientists are still confused."
)

MAX_CHARS = 200
DEFAULT_OUTPUT = "/tmp/u-donrulezz-museum-of-the-year-3000-b727a0bb/entry.txt"


def validate_entry(text):
    """Check the entry is a single line of at most 200 characters."""
    if not text or not text.strip():
        raise ValueError("entry must not be empty")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if "\t" in text or any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain tabs or control characters")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d chars, over the %d-char limit" % (len(text), MAX_CHARS)
        )
    return text


def candidate_output_paths():
    """Return output paths in priority order, never inside the repo."""
    paths = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        paths.append(os.path.join(env_dir, "entry.txt"))
    env_file = os.environ.get("MAKEFUN_OUTPUT")
    if env_file:
        # MAKEFUN_OUTPUT may be a directory (ending in /) or a file path.
        if env_file.endswith(os.sep):
            paths.append(os.path.join(env_file, "entry.txt"))
        else:
            paths.append(env_file)
    paths.append(DEFAULT_OUTPUT)
    # De-duplicate while preserving priority order.
    seen = set()
    unique_paths = []
    for path in paths:
        if path not in seen:
            seen.add(path)
            unique_paths.append(path)
    return unique_paths


def write_entry(text):
    """Write the entry to the first writable output location."""
    errors = []
    for path in candidate_output_paths():
        try:
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text + "\n")
            return path
        except OSError as exc:
            errors.append("%s: %s" % (path, exc))
    raise OSError("could not write entry to any output path: " + "; ".join(errors))


def main():
    entry = validate_entry(ENTRY)
    print(entry)
    sys.stdout.flush()
    print(
        "entry OK: %d/%d chars, single line" % (len(entry), MAX_CHARS),
        file=sys.stderr,
    )
    try:
        written = write_entry(entry)
        print("wrote entry to %s" % written, file=sys.stderr)
    except OSError as exc:
        print("warning: could not write output file: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
