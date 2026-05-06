#!/usr/bin/env python3
"""Install selected Claude Code skills without cloning the repository."""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import io
import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path


DEFAULT_ARCHIVE_URL = (
    "https://github.com/rsnemmen/claude-skills/archive/refs/heads/main.zip"
)
DEFAULT_INSTALL_DIR = Path.home() / ".claude" / "skills"


class InstallerError(Exception):
    """Raised for expected installer failures."""


def download_archive(url: str) -> bytes:
    print(f"Downloading skills archive from {url}")
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return response.read()
    except Exception as exc:  # noqa: BLE001 - keep CLI error concise.
        raise InstallerError(f"Could not download archive: {exc}") from exc


def safe_extract(archive_data: bytes, destination: Path) -> Path:
    try:
        with zipfile.ZipFile(io.BytesIO(archive_data)) as archive:
            members = archive.infolist()
            if not members:
                raise InstallerError("Archive is empty.")

            root_names = {
                Path(member.filename).parts[0]
                for member in members
                if member.filename
            }
            if len(root_names) != 1:
                raise InstallerError("Archive does not have a single top-level directory.")
            root_name = root_names.pop()

            destination_resolved = destination.resolve()
            for member in members:
                target = (destination / member.filename).resolve()
                if not str(target).startswith(str(destination_resolved) + os.sep):
                    raise InstallerError(f"Archive contains unsafe path: {member.filename}")

            archive.extractall(destination)
            return destination / root_name
    except zipfile.BadZipFile as exc:
        raise InstallerError("Downloaded file is not a valid zip archive.") from exc


def parse_frontmatter(skill_file: Path) -> dict[str, str]:
    metadata: dict[str, str] = {}
    try:
        lines = skill_file.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return metadata

    if not lines or lines[0].strip() != "---":
        return metadata

    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        clean_value = value.strip()
        if len(clean_value) >= 2 and clean_value[0] == clean_value[-1]:
            if clean_value[0] in {"'", '"'}:
                clean_value = clean_value[1:-1]
        metadata[key.strip()] = clean_value
    return metadata


def discover_skills(repo_root: Path) -> list[dict[str, str | Path]]:
    skills: list[dict[str, str | Path]] = []
    for child in sorted(repo_root.iterdir(), key=lambda path: path.name):
        skill_file = child / "SKILL.md"
        if not child.is_dir() or not skill_file.is_file():
            continue

        metadata = parse_frontmatter(skill_file)
        skills.append(
            {
                "dir_name": child.name,
                "path": child,
                "name": metadata.get("name", child.name),
                "description": metadata.get("description", ""),
                "argument_hint": metadata.get("argument-hint", ""),
            }
        )
    return skills


def open_prompt_stream():
    try:
        return open("/dev/tty", "r", encoding="utf-8")
    except OSError:
        return sys.stdin


def prompt(prompt_stream, message: str) -> str:
    print(message, end="", flush=True)
    answer = prompt_stream.readline()
    if answer == "":
        raise InstallerError("No input available for interactive prompt.")
    return answer.strip()


def print_menu(skills: list[dict[str, str | Path]]) -> None:
    print("\nAvailable skills:")
    for index, skill in enumerate(skills, start=1):
        name = skill["name"]
        dir_name = skill["dir_name"]
        description = skill["description"]
        argument_hint = skill["argument_hint"]
        print(f"  {index}. {dir_name} ({name})")
        if description:
            print(f"     {description}")
        if argument_hint:
            print(f"     Arguments: {argument_hint}")
    print("\nSelect skills by number, comma list, range, 'all', or 'q' to quit.")


def parse_selection(selection: str, skill_count: int) -> list[int] | None:
    normalized = selection.strip().lower()
    if normalized in {"q", "quit", "exit"}:
        return None
    if normalized in {"a", "all"}:
        return list(range(skill_count))

    selected: set[int] = set()
    for chunk in normalized.split(","):
        part = chunk.strip()
        if not part:
            continue
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            if not start_text.isdigit() or not end_text.isdigit():
                raise ValueError(f"Invalid range: {part}")
            start = int(start_text)
            end = int(end_text)
            if start > end:
                raise ValueError(f"Invalid descending range: {part}")
            numbers = range(start, end + 1)
        else:
            if not part.isdigit():
                raise ValueError(f"Invalid selection: {part}")
            numbers = [int(part)]

        for number in numbers:
            if number < 1 or number > skill_count:
                raise ValueError(f"Selection out of range: {number}")
            selected.add(number - 1)

    if not selected:
        raise ValueError("No skills selected.")
    return sorted(selected)


def choose_skills(
    prompt_stream,
    skills: list[dict[str, str | Path]],
) -> list[dict[str, str | Path]]:
    while True:
        print_menu(skills)
        answer = prompt(prompt_stream, "Selection: ")
        try:
            indexes = parse_selection(answer, len(skills))
        except ValueError as exc:
            print(f"{exc}. Try again.")
            continue
        if indexes is None:
            return []
        return [skills[index] for index in indexes]


def remove_existing(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def backup_existing(path: Path) -> Path:
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    base = path.with_name(f"{path.name}.backup-{timestamp}")
    backup_path = base
    suffix = 1
    while backup_path.exists() or backup_path.is_symlink():
        backup_path = path.with_name(f"{base.name}-{suffix}")
        suffix += 1
    path.rename(backup_path)
    return backup_path


def resolve_conflict(prompt_stream, target: Path) -> str:
    choices = {"s": "skip", "skip": "skip", "o": "overwrite", "overwrite": "overwrite"}
    choices.update({"b": "backup", "backup": "backup", "a": "abort", "abort": "abort"})

    while True:
        answer = prompt(
            prompt_stream,
            (
                f"Conflict: {target} already exists. "
                "[s]kip, [o]verwrite, [b]ackup, or [a]bort? "
            ),
        ).lower()
        if answer in choices:
            return choices[answer]
        print("Please enter skip, overwrite, backup, or abort.")


def install_skill(prompt_stream, skill: dict[str, str | Path], install_dir: Path) -> bool:
    source = Path(skill["path"])
    dir_name = str(skill["dir_name"])
    target = install_dir / dir_name

    if target.exists() or target.is_symlink():
        decision = resolve_conflict(prompt_stream, target)
        if decision == "skip":
            print(f"Skipped {dir_name}.")
            return True
        if decision == "abort":
            print("Aborted.")
            return False
        if decision == "backup":
            backup_path = backup_existing(target)
            print(f"Backed up existing {dir_name} to {backup_path}.")
        elif decision == "overwrite":
            remove_existing(target)
            print(f"Removed existing {dir_name}.")

    shutil.copytree(source, target, symlinks=True)
    print(f"Installed {dir_name} to {target}")
    return True


def install_selected(
    prompt_stream,
    selected_skills: list[dict[str, str | Path]],
    install_dir: Path,
) -> int:
    install_dir.mkdir(parents=True, exist_ok=True)
    installed = 0
    for skill in selected_skills:
        should_continue = install_skill(prompt_stream, skill, install_dir)
        if not should_continue:
            break
        target = install_dir / str(skill["dir_name"])
        if target.exists():
            installed += 1
    return installed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install selected Claude Code skills without cloning the repo."
    )
    parser.add_argument(
        "--archive-url",
        default=DEFAULT_ARCHIVE_URL,
        help=f"Zip archive URL to install from. Default: {DEFAULT_ARCHIVE_URL}",
    )
    parser.add_argument(
        "--install-dir",
        type=Path,
        default=DEFAULT_INSTALL_DIR,
        help=f"Install destination. Default: {DEFAULT_INSTALL_DIR}",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        with tempfile.TemporaryDirectory(prefix="claude-skills-") as temp_dir:
            archive_data = download_archive(args.archive_url)
            repo_root = safe_extract(archive_data, Path(temp_dir))
            skills = discover_skills(repo_root)
            if not skills:
                raise InstallerError("No skills found in archive.")

            stream = open_prompt_stream()
            stream_context = (
                contextlib.nullcontext(stream)
                if stream is sys.stdin
                else contextlib.closing(stream)
            )
            with stream_context as prompt_stream:
                selected_skills = choose_skills(prompt_stream, skills)
                if not selected_skills:
                    print("No skills selected.")
                    return 0
                installed = install_selected(
                    prompt_stream,
                    selected_skills,
                    args.install_dir.expanduser(),
                )

            print(f"\nDone. Installed or kept {installed} skill(s).")
            return 0
    except KeyboardInterrupt:
        print("\nAborted.")
        return 130
    except InstallerError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
