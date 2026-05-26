#!/usr/bin/env python3
"""
deduplicate_puzzles.py
======================
Scans the puzzles/ folder for duplicate puzzle files, removes them,
then re-numbers all remaining puzzles sequentially starting from 1.

A puzzle is a duplicate when its meaningful content (header + 6×6 grid)
matches that of a previously-seen puzzle.  Comment lines and trailing
whitespace are ignored during comparison.

Usage
-----
    python deduplicate_puzzles.py [--dry-run]

Options
-------
    --dry-run   Print what would happen without deleting or renaming anything.
"""

import argparse
import hashlib
import os
import shutil
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_puzzle(filepath: Path) -> str:
    """
    Return a canonical string representing the puzzle's meaningful content.

    Meaningful lines are those that do NOT start with '#' and are not blank.
    Inline comments (text after the first '#' on a line) are stripped so that
    minor comment wording differences between files don't affect comparison.
    """
    meaningful = []
    with filepath.open("r", encoding="utf-8", errors="replace") as fh:
        for raw_line in fh:
            line = raw_line.rstrip()
            # Skip pure comment lines and blank lines
            if not line or line.lstrip().startswith("#"):
                continue
            # Strip inline comment (e.g. "R # T(op) vs B(ottom)…" → "R")
            if "#" in line:
                line = line[: line.index("#")].rstrip()
            meaningful.append(line)
    return "\n".join(meaningful)


def file_hash(content: str) -> str:
    """Return the MD5 hex-digest of the canonical puzzle content."""
    return hashlib.md5(content.encode("utf-8")).hexdigest()


def sorted_puzzle_files(folder: Path) -> list[Path]:
    """Return all *.txt files whose stem is a plain integer, sorted numerically."""
    files = [f for f in folder.glob("*.txt") if f.stem.isdigit()]
    return sorted(files, key=lambda f: int(f.stem))


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------

def find_duplicates(puzzle_files: list[Path]) -> tuple[list[Path], list[Path]]:
    """
    Partition *puzzle_files* into (unique_files, duplicate_files).

    The first occurrence of each distinct puzzle content is kept; every
    later occurrence is classified as a duplicate.
    """
    seen: dict[str, Path] = {}   # hash → first file that had it
    unique: list[Path] = []
    duplicates: list[Path] = []

    for i, fp in enumerate(puzzle_files, 1):
        if i % 1000 == 0 or i == len(puzzle_files):
            print(f"  Scanning … {i}/{len(puzzle_files)}", end="\r", flush=True)
        content = parse_puzzle(fp)
        h = file_hash(content)
        if h in seen:
            duplicates.append(fp)
        else:
            seen[h] = fp
            unique.append(fp)

    print()  # newline after the progress line
    return unique, duplicates


def remove_duplicates(duplicates: list[Path], dry_run: bool) -> None:
    """Delete duplicate files (or just report them in dry-run mode)."""
    if not duplicates:
        print("No duplicate files to remove.")
        return

    print(f"\n{'[DRY RUN] Would remove' if dry_run else 'Removing'} "
          f"{len(duplicates)} duplicate file(s):")
    for fp in duplicates:
        print(f"  - {fp.name}")
        if not dry_run:
            fp.unlink()


def renumber(unique_files: list[Path], folder: Path, dry_run: bool) -> None:
    """
    Rename files so they are numbered 1.txt, 2.txt, … N.txt with no gaps.

    Uses a temporary sub-directory to avoid collisions when the new name of
    one file matches the old name of another (e.g. 3.txt → 2.txt while
    2.txt still exists).
    """
    # Check whether any renaming is actually needed
    already_sequential = all(
        int(fp.stem) == idx
        for idx, fp in enumerate(unique_files, 1)
    )
    if already_sequential:
        print("\nPuzzles are already numbered sequentially — no renaming needed.")
        return

    n = len(unique_files)
    print(f"\n{'[DRY RUN] Would renumber' if dry_run else 'Renumbering'} "
          f"{n} puzzle(s) to 1.txt … {n}.txt …")

    if dry_run:
        changes = [
            (fp, folder / f"{i}.txt")
            for i, fp in enumerate(unique_files, 1)
            if int(fp.stem) != i
        ]
        print(f"  {len(changes)} file(s) would be renamed "
              f"(first few shown below):")
        for old, new in changes[:10]:
            print(f"    {old.name}  →  {new.name}")
        if len(changes) > 10:
            print(f"    … and {len(changes) - 10} more")
        return

    # Step 1 – move everything into a temporary staging directory
    staging = folder / "_staging_renumber"
    staging.mkdir(exist_ok=True)
    try:
        for i, fp in enumerate(unique_files, 1):
            if i % 1000 == 0 or i == n:
                print(f"  Stage 1/2 … {i}/{n}", end="\r", flush=True)
            shutil.move(str(fp), staging / f"{i}.txt")
        print()

        # Step 2 – move back into the puzzles folder under the final names
        staged = sorted(
            [f for f in staging.glob("*.txt") if f.stem.isdigit()],
            key=lambda f: int(f.stem),
        )
        for i, fp in enumerate(staged, 1):
            if i % 1000 == 0 or i == n:
                print(f"  Stage 2/2 … {i}/{n}", end="\r", flush=True)
            shutil.move(str(fp), folder / fp.name)
        print()

    finally:
        # Always clean up the staging directory
        if staging.exists():
            try:
                staging.rmdir()  # succeeds only if empty (it should be)
            except OSError:
                shutil.rmtree(staging)  # fallback if somehow not empty


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove duplicate puzzles and re-number them sequentially."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate all actions without modifying any files.",
    )
    args = parser.parse_args()

    # Resolve the puzzles folder relative to this script's location
    script_dir = Path(__file__).resolve().parent
    puzzles_dir = script_dir  # script lives inside puzzles/

    # Alternatively, if the script is placed one level up:
    # puzzles_dir = script_dir / "puzzles"

    if not puzzles_dir.is_dir():
        sys.exit(f"Error: puzzle folder not found at {puzzles_dir}")

    print(f"Puzzle folder : {puzzles_dir}")
    if args.dry_run:
        print("Mode          : DRY RUN (no files will be modified)\n")
    else:
        print("Mode          : LIVE\n")

    # ── 1. Inventory ─────────────────────────────────────────────────────────
    all_files = sorted_puzzle_files(puzzles_dir)
    print(f"Total puzzle files found : {len(all_files)}")
    if not all_files:
        sys.exit("No puzzle files found. Nothing to do.")

    # ── 2. Detect duplicates ──────────────────────────────────────────────────
    print("Scanning for duplicates …")
    unique_files, duplicates = find_duplicates(all_files)
    print(f"  Unique puzzles   : {len(unique_files)}")
    print(f"  Duplicate files  : {len(duplicates)}")

    # ── 3. Remove duplicates ──────────────────────────────────────────────────
    remove_duplicates(duplicates, dry_run=args.dry_run)

    # ── 4. Re-number ─────────────────────────────────────────────────────────
    renumber(unique_files, puzzles_dir, dry_run=args.dry_run)

    # ── 5. Summary ────────────────────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("SUMMARY")
    print("=" * 55)
    print(f"  Files before   : {len(all_files):>7,}")
    print(f"  Duplicates     : {len(duplicates):>7,}")
    print(f"  Files after    : {len(unique_files):>7,}")
    if len(unique_files) > 0:
        print(f"  Range after    : 1.txt … {len(unique_files)}.txt")
    if args.dry_run:
        print("\n(Dry-run complete — no files were changed.)")
    else:
        print("\nDone.")


if __name__ == "__main__":
    main()
