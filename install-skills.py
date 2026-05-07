#!/usr/bin/env python3
"""Install selected Claude Code and Codex CLI skills without cloning the repository."""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import io
import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

try:
    import curses as _curses_mod
    _CURSES_AVAILABLE = True
except ImportError:
    _CURSES_AVAILABLE = False


DEFAULT_ARCHIVE_URL = (
    "https://github.com/rsnemmen/claude-skills/archive/refs/heads/main.zip"
)


def default_codex_install_dir() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home) / "skills"
    return Path.home() / ".codex" / "skills"


PLATFORM_CONFIGS = {
    "claude": {
        "label": "Claude Code",
        "source_dir": "skills",
        "install_dir": Path.home() / ".claude" / "skills",
    },
    "codex": {
        "label": "Codex CLI",
        "source_dir": "codex-skills",
        "install_dir": default_codex_install_dir(),
    },
}

STATUS_LABELS = {
    "not_installed": "not installed",
    "outdated":      "outdated",
    "up_to_date":    "up-to-date",
    "linked":        "linked",
}

_ANSI = {
    "red":    "\033[31m",
    "yellow": "\033[33m",
    "green":  "\033[32m",
    "cyan":   "\033[36m",
    "dim":    "\033[2m",
    "bold":   "\033[1m",
    "reset":  "\033[0m",
}
_STATUS_COLORS = {
    "linked":        "green",
    "up_to_date":    "green",
    "outdated":      "yellow",
    "not_installed": "red",
}

_color_disabled = False


class InstallerError(Exception):
    """Raised for expected installer failures."""


# ─── Color helpers ────────────────────────────────────────────────────────────

def colorize(text: str, color: str, *, bold: bool = False) -> str:
    if _color_disabled or os.environ.get("NO_COLOR") or not sys.stdout.isatty():
        return text
    prefix = _ANSI.get(color, "")
    if bold:
        prefix = _ANSI["bold"] + prefix
    return f"{prefix}{text}{_ANSI['reset']}"


def _status_tag(status: str) -> str:
    label = STATUS_LABELS.get(status, status)
    tag = f"[{label}]"
    color = _STATUS_COLORS.get(status, "")
    return colorize(tag, color) if color else tag


# ─── Archive download / extraction ───────────────────────────────────────────

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


# ─── Source resolution ────────────────────────────────────────────────────────

def has_skill_source(path: Path) -> bool:
    return any(
        (path / str(config["source_dir"])).is_dir()
        and any(
            (child / "SKILL.md").is_file()
            for child in (path / str(config["source_dir"])).iterdir()
            if child.is_dir()
        )
        for config in PLATFORM_CONFIGS.values()
    )


def find_local_repo() -> Path | None:
    """Walk up from the script's location to find a repo root with skill source dirs."""
    candidate = Path(__file__).resolve().parent
    while True:
        if has_skill_source(candidate):
            return candidate
        parent = candidate.parent
        if parent == candidate:
            return None
        candidate = parent


def resolve_source(args: argparse.Namespace) -> tuple[Path | None, bool]:
    """Return (repo_root, is_local). repo_root=None means use the download path."""
    if args.source is not None:
        source = Path(args.source).expanduser().resolve()
        if not has_skill_source(source):
            raise InstallerError(f"--source path has no skill source dir: {source}")
        return source, True
    local = find_local_repo()
    if local is not None:
        return local, True
    return None, False


# ─── Skill discovery ──────────────────────────────────────────────────────────

def hash_skill_tree(path: Path) -> str:
    """SHA-256 over sorted (relative-path, content) pairs for every non-dotfile."""
    h = hashlib.sha256()
    for file in sorted(path.rglob("*")):
        if not file.is_file():
            continue
        if any(part.startswith(".") for part in file.relative_to(path).parts):
            continue
        h.update(str(file.relative_to(path)).encode())
        h.update(file.read_bytes())
    return h.hexdigest()


def skill_status(source_skill: Path, target: Path) -> str:
    """Classify a skill's install state relative to the source."""
    if target.is_symlink():
        if os.path.realpath(target) == os.path.realpath(source_skill):
            return "linked"
        if not target.exists():
            return "not_installed"  # dangling symlink
    elif not target.exists():
        return "not_installed"
    if hash_skill_tree(source_skill) == hash_skill_tree(target):
        return "up_to_date"
    return "outdated"


def short_description(full: str, limit: int = 100) -> str:
    """Return the first sentence of a description, capped at limit chars."""
    text = full.strip()
    period = text.find(". ")
    sentence = text[: period + 1] if period != -1 else text
    if len(sentence) > limit:
        return sentence[: limit - 1] + "…"
    return sentence


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


def discover_skills(repo_root: Path, install_dir: Path, source_dir: str) -> list[dict]:
    skills_root = repo_root / source_dir
    if not skills_root.is_dir():
        raise InstallerError(f"No {source_dir}/ directory found in source.")
    skills: list[dict] = []
    for child in sorted(skills_root.iterdir(), key=lambda p: p.name):
        skill_file = child / "SKILL.md"
        if not child.is_dir() or not skill_file.is_file():
            continue
        metadata = parse_frontmatter(skill_file)
        target = install_dir / child.name
        status = skill_status(child, target)
        description = metadata.get("description", "")
        skills.append({
            "dir_name":          child.name,
            "path":              child,
            "name":              metadata.get("name", child.name),
            "description":       description,
            "short_description": short_description(description),
            "argument_hint":     metadata.get("argument-hint", ""),
            "status":            status,
        })
    return skills


def merged_skills_by_name(platform_skills: dict[str, list[dict]]) -> list[dict]:
    names = sorted(
        set.intersection(
            *[set(skill["dir_name"] for skill in skills) for skills in platform_skills.values()]
        )
    )
    merged: list[dict] = []
    for name in names:
        by_platform = {
            platform: next(skill for skill in skills if skill["dir_name"] == name)
            for platform, skills in platform_skills.items()
        }
        statuses = [str(skill.get("status", "")) for skill in by_platform.values()]
        if any(status == "outdated" for status in statuses):
            status = "outdated"
        elif all(status in {"linked", "up_to_date"} for status in statuses):
            status = "up_to_date"
        elif any(status == "not_installed" for status in statuses):
            status = "not_installed"
        else:
            status = statuses[0] if statuses else ""
        first = by_platform[sorted(by_platform)[0]]
        merged.append({
            "dir_name": first["dir_name"],
            "name": first["name"],
            "description": first["description"],
            "short_description": first["short_description"],
            "status": status,
            "platform_skills": by_platform,
        })
    return merged


# ─── Text-mode menu (fallback) ────────────────────────────────────────────────

def open_prompt_stream():
    try:
        return open("/dev/tty", "r", encoding="utf-8")
    except OSError:
        return sys.stdin


def can_prompt() -> bool:
    if sys.stdin.isatty() or sys.stdout.isatty():
        return True
    try:
        fd = os.open("/dev/tty", os.O_RDWR)
    except OSError:
        return False
    os.close(fd)
    return True


def prompt(prompt_stream, message: str) -> str:
    print(message, end="", flush=True)
    answer = prompt_stream.readline()
    if answer == "":
        raise InstallerError("No input available for interactive prompt.")
    return answer.strip()


def print_menu(skills: list[dict]) -> None:
    print("\nAvailable skills:")
    for index, skill in enumerate(skills, start=1):
        dir_name  = skill["dir_name"]
        short_desc = skill.get("short_description", "")
        status    = str(skill.get("status", ""))
        tag = f"  {_status_tag(status)}" if status else ""
        print(f"  {index}. {colorize(dir_name, 'bold')}{tag}")
        if short_desc:
            print(f"     {colorize(short_desc, 'dim')}")
    print(
        "\nSelect by number, range, 'all', 'outdated'/'o', 'missing'/'m', or 'q' to quit."
    )


def print_status_report(skills: list[dict]) -> None:
    print("Skills status:")
    for skill in skills:
        dir_name = skill["dir_name"]
        platform_skills = skill.get("platform_skills")
        if platform_skills:
            parts = []
            for platform, platform_skill in platform_skills.items():
                label = str(PLATFORM_CONFIGS[platform]["label"])
                parts.append(f"{label}: {_status_tag(str(platform_skill.get('status', '')))}")
            print(f"  {colorize(dir_name, 'bold')}  " + "  ".join(parts))
            continue
        status   = str(skill.get("status", ""))
        tag      = _status_tag(status) if status else ""
        print(f"  {colorize(dir_name, 'bold')}  {tag}")


def parse_selection(selection: str, skills: list[dict]) -> list[int] | None:
    normalized = selection.strip().lower()
    if normalized in {"q", "quit", "exit"}:
        return None
    if normalized in {"a", "all"}:
        return list(range(len(skills)))
    if normalized in {"o", "outdated"}:
        return [i for i, s in enumerate(skills) if s.get("status") == "outdated"]
    if normalized in {"m", "missing"}:
        return [i for i, s in enumerate(skills) if s.get("status") == "not_installed"]

    skill_count = len(skills)
    selected: set[int] = set()
    for chunk in normalized.split(","):
        part = chunk.strip()
        if not part:
            continue
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            if not start_text.isdigit() or not end_text.isdigit():
                raise ValueError(f"Invalid range: {part}")
            start, end = int(start_text), int(end_text)
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


def choose_skills_text(prompt_stream, skills: list[dict]) -> list[dict]:
    while True:
        print_menu(skills)
        answer = prompt(prompt_stream, "Selection: ")
        try:
            indexes = parse_selection(answer, skills)
        except ValueError as exc:
            print(f"{exc}. Try again.")
            continue
        if indexes is None:
            return []
        return [skills[index] for index in indexes]


def choose_target_text(prompt_stream) -> str:
    choices = {
        "": "claude",
        "1": "claude", "c": "claude", "claude": "claude",
        "2": "codex", "x": "codex", "codex": "codex",
        "3": "both", "b": "both", "both": "both",
    }
    print("\nInstall skills for:")
    print("  1. Claude Code (default)")
    print("  2. Codex CLI")
    print("  3. Both")
    while True:
        answer = prompt(prompt_stream, "Target [1/2/3]: ").lower()
        if answer in choices:
            return choices[answer]
        print("Please enter 1, 2, or 3.")


# ─── Curses TUI picker ────────────────────────────────────────────────────────

_CP_GREEN  = 1
_CP_YELLOW = 2
_CP_RED    = 3

_STATUS_TAG_W = max(len(f"[{lbl}]") for lbl in STATUS_LABELS.values())  # 15
_MAX_NAME_W   = 20


def _cp_for_status(status: str) -> int:
    if _CURSES_AVAILABLE:
        import curses
        if status in ("linked", "up_to_date"):
            return curses.color_pair(_CP_GREEN)
        if status == "outdated":
            return curses.color_pair(_CP_YELLOW)
        if status == "not_installed":
            return curses.color_pair(_CP_RED)
    return 0


def _curses_picker(stdscr, skills: list[dict]):
    import curses

    rows, cols = stdscr.getmaxyx()
    if rows < 8 or cols < 50:
        return None  # terminal too small — signal failure

    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(_CP_GREEN,  curses.COLOR_GREEN,  -1)
    curses.init_pair(_CP_YELLOW, curses.COLOR_YELLOW, -1)
    curses.init_pair(_CP_RED,    curses.COLOR_RED,    -1)
    curses.curs_set(0)

    cursor:   int      = 0
    selected: set[int] = set()

    footer = " ↑/↓ move  space select  a=all  o=outdated  m=missing  enter=install  q=quit "

    while True:
        rows, cols = stdscr.getmaxyx()
        # desc width fills the space between name and status
        desc_w = max(0, cols - 6 - _MAX_NAME_W - 2 - _STATUS_TAG_W - 1)

        stdscr.erase()

        # Header
        try:
            stdscr.addstr(0, 0, "  Skills Installer"[:cols - 1], curses.A_BOLD)
        except curses.error:
            pass

        # Skill rows (start at row 2, leave row 0=title, 1=blank, last=footer)
        for i, skill in enumerate(skills):
            row = 2 + i
            if row >= rows - 1:
                break

            is_hi  = (i == cursor)
            is_sel = (i in selected)
            status = str(skill.get("status", ""))
            name   = str(skill["dir_name"])
            desc   = str(skill.get("short_description", ""))

            checkbox = "[x]" if is_sel else "[ ]"
            tag      = f"[{STATUS_LABELS.get(status, status)}]"

            name_field   = name[:_MAX_NAME_W].ljust(_MAX_NAME_W)
            desc_field   = desc[:desc_w].ljust(desc_w)
            status_field = tag[:_STATUS_TAG_W].ljust(_STATUS_TAG_W)

            # "  [x] name_field  desc_field status_field"
            #   2  3  1 MAX_NAME  2 desc_w   1 STATUS_W
            line = f"  {checkbox} {name_field}  {desc_field} {status_field}"
            line = line[:cols]  # guard against off-by-one

            base = curses.A_REVERSE if is_hi else 0
            try:
                stdscr.addstr(row, 0, line, base)
                # Re-color: status tag
                sc = cols - _STATUS_TAG_W
                if sc >= 0:
                    cp = _cp_for_status(status)
                    stdscr.addstr(row, sc, status_field[:cols - sc], (base | cp) if cp else base)
                # Dim: description
                if not is_hi and desc_w > 0:
                    dc = 6 + _MAX_NAME_W + 2
                    stdscr.addstr(row, dc, desc_field[:desc_w], curses.A_DIM)
            except curses.error:
                pass

        # Footer
        try:
            stdscr.addstr(
                rows - 1, 0,
                footer[: cols - 1].ljust(cols - 1),
                curses.A_REVERSE,
            )
        except curses.error:
            pass

        stdscr.refresh()
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord("k")):
            cursor = (cursor - 1) % len(skills)
        elif key in (curses.KEY_DOWN, ord("j")):
            cursor = (cursor + 1) % len(skills)
        elif key == ord(" "):
            selected ^= {cursor}
        elif key == ord("a"):
            selected = set(range(len(skills))) if len(selected) < len(skills) else set()
        elif key == ord("o"):
            selected = {i for i, s in enumerate(skills) if s.get("status") == "outdated"}
        elif key == ord("m"):
            selected = {i for i, s in enumerate(skills) if s.get("status") == "not_installed"}
        elif key in (10, 13, curses.KEY_ENTER):
            return [skills[i] for i in sorted(selected)]
        elif key in (ord("q"), 27):
            return None  # cancelled


def acquire_tty() -> bool:
    """Redirect fd 0/1 to /dev/tty so curses can run even when stdin is piped."""
    if sys.stdin.isatty() and sys.stdout.isatty():
        return True
    try:
        fd = os.open("/dev/tty", os.O_RDWR)
        os.dup2(fd, 0)
        os.dup2(fd, 1)
        os.close(fd)
        return True
    except OSError:
        return False


def choose_skills_curses(skills: list[dict]) -> tuple[list[dict], str]:
    """
    Returns (selected_list, status) where status is one of:
      'selected'  — user confirmed (list may be empty if nothing ticked)
      'cancelled' — user pressed q/Esc
      'failed'    — curses unavailable or terminal too small
    """
    if not _CURSES_AVAILABLE:
        return [], "failed"
    try:
        import curses
        result = curses.wrapper(_curses_picker, skills)
    except Exception:  # noqa: BLE001
        return [], "failed"

    if result is None:
        return [], "cancelled"
    return result, "selected"


# ─── Install logic ────────────────────────────────────────────────────────────

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
    choices = {
        "s": "skip",  "skip": "skip",
        "o": "overwrite", "overwrite": "overwrite",
        "b": "backup", "backup": "backup",
        "a": "abort",  "abort": "abort",
    }
    while True:
        answer = prompt(
            prompt_stream,
            f"Conflict: {target} already exists. [s]kip, [o]verwrite, [b]ackup, or [a]bort? ",
        ).lower()
        if answer in choices:
            return choices[answer]
        print("Please enter skip, overwrite, backup, or abort.")


def install_skill(
    prompt_stream,
    skill: dict,
    install_dir: Path,
    link_mode: bool,
) -> bool:
    source   = Path(skill["path"])
    dir_name = str(skill["dir_name"])
    status   = str(skill.get("status", ""))
    target   = install_dir / dir_name

    if status in ("linked", "up_to_date"):
        print(f"  {dir_name}: already up-to-date, skipping.")
        return True

    # Remove dangling symlinks silently before proceeding.
    if target.is_symlink() and not target.exists():
        target.unlink()

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

    if link_mode:
        target.symlink_to(source.resolve())
        print(f"Linked {dir_name} -> {source.resolve()}")
    else:
        shutil.copytree(source, target, symlinks=True)
        print(f"Installed {dir_name} to {target}")
    return True


def install_selected(
    prompt_stream,
    selected_skills: list[dict],
    install_dir: Path,
    link_mode: bool,
) -> int:
    install_dir.mkdir(parents=True, exist_ok=True)
    installed = 0
    for skill in selected_skills:
        if not install_skill(prompt_stream, skill, install_dir, link_mode):
            break
        target = install_dir / str(skill["dir_name"])
        if target.exists() or target.is_symlink():
            installed += 1
    return installed


def install_selected_for_platforms(
    prompt_stream,
    selected_skills: list[dict],
    platforms: list[str],
    install_dirs: dict[str, Path],
    link_mode: bool,
) -> int:
    installed = 0
    for platform in platforms:
        install_dirs[platform].mkdir(parents=True, exist_ok=True)
    for skill in selected_skills:
        platform_skills = skill.get("platform_skills")
        for platform in platforms:
            platform_skill = (
                platform_skills[platform]
                if platform_skills
                else skill
            )
            label = str(PLATFORM_CONFIGS[platform]["label"])
            print(f"\n{label}:")
            if install_skill(prompt_stream, platform_skill, install_dirs[platform], link_mode):
                target = install_dirs[platform] / str(platform_skill["dir_name"])
                if target.exists() or target.is_symlink():
                    installed += 1
            else:
                return installed
    return installed


# ─── CLI ─────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install selected Claude Code or Codex CLI skills without cloning the repo."
    )
    parser.add_argument(
        "--archive-url",
        default=DEFAULT_ARCHIVE_URL,
        help=f"Zip archive URL to install from. Default: {DEFAULT_ARCHIVE_URL}",
    )
    parser.add_argument(
        "--install-dir",
        type=Path,
        help="Single-target install destination. Defaults to the target platform's user skills dir.",
    )
    parser.add_argument(
        "--claude-install-dir",
        type=Path,
        default=PLATFORM_CONFIGS["claude"]["install_dir"],
        help=f"Claude Code install destination. Default: {PLATFORM_CONFIGS['claude']['install_dir']}",
    )
    parser.add_argument(
        "--codex-install-dir",
        type=Path,
        default=PLATFORM_CONFIGS["codex"]["install_dir"],
        help=f"Codex CLI install destination. Default: {PLATFORM_CONFIGS['codex']['install_dir']}",
    )
    parser.add_argument(
        "--target",
        choices=("claude", "codex", "both"),
        help="Install target. Defaults to Claude Code unless omitted in an interactive install.",
    )
    parser.add_argument(
        "--source",
        metavar="PATH",
        help="Use a local checkout as the source instead of downloading.",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Print install status for every skill and exit without installing.",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI color output.",
    )
    parser.add_argument(
        "--no-tui",
        action="store_true",
        help="Force the text-based numeric menu instead of the interactive TUI.",
    )
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--link",
        action="store_true",
        help="Install as symlinks (default when source is local).",
    )
    mode_group.add_argument(
        "--copy",
        action="store_true",
        help="Install as copies (default when source is downloaded).",
    )
    return parser


def main() -> int:
    global _color_disabled

    parser = build_parser()
    args = parser.parse_args()

    if args.no_color:
        _color_disabled = True

    try:
        if args.install_dir is not None and args.target == "both":
            raise InstallerError("--install-dir cannot be used with --target both.")

        repo_root, is_local = resolve_source(args)

        if args.link:
            link_mode = True
        elif args.copy:
            link_mode = False
        else:
            link_mode = is_local

        if link_mode and not is_local:
            raise InstallerError(
                "--link requires a local source (use --source or run from inside the repo)."
            )

        def run(root: Path) -> int:
            target = args.target
            if target is None:
                if args.status or not can_prompt():
                    target = "claude"
                else:
                    stream = open_prompt_stream()
                    ctx = (
                        contextlib.nullcontext(stream)
                        if stream is sys.stdin
                        else contextlib.closing(stream)
                    )
                    with ctx as prompt_stream:
                        target = choose_target_text(prompt_stream)

            if args.install_dir is not None and target == "both":
                raise InstallerError("--install-dir cannot be used when installing both targets.")

            platforms = ["claude", "codex"] if target == "both" else [target]
            install_dirs = {
                "claude": Path(args.claude_install_dir).expanduser(),
                "codex": Path(args.codex_install_dir).expanduser(),
            }
            if args.install_dir is not None:
                install_dirs[str(target)] = args.install_dir.expanduser()

            platform_skills = {
                platform: discover_skills(
                    root,
                    install_dirs[platform],
                    str(PLATFORM_CONFIGS[platform]["source_dir"]),
                )
                for platform in platforms
            }
            skills = (
                merged_skills_by_name(platform_skills)
                if len(platforms) > 1
                else platform_skills[platforms[0]]
            )
            if not skills:
                raise InstallerError("No skills found in source.")

            if args.status:
                print_status_report(skills)
                return 0

            # Try curses TUI first
            if not args.no_tui and acquire_tty():
                selected, picker_status = choose_skills_curses(skills)
                if picker_status == "cancelled":
                    print("No skills selected.")
                    return 0
                if picker_status == "selected":
                    if not selected:
                        print("No skills selected.")
                        return 0
                    ps = open_prompt_stream()
                    ctx = contextlib.nullcontext(ps) if ps is sys.stdin else contextlib.closing(ps)
                    with ctx as prompt_stream:
                        installed = install_selected_for_platforms(
                            prompt_stream,
                            selected,
                            platforms,
                            install_dirs,
                            link_mode,
                        )
                    print(f"\nDone. Installed or kept {installed} skill(s).")
                    return 0
                # picker_status == "failed" — fall through to text menu

            # Text menu fallback
            stream = open_prompt_stream()
            ctx = (
                contextlib.nullcontext(stream)
                if stream is sys.stdin
                else contextlib.closing(stream)
            )
            with ctx as prompt_stream:
                selected = choose_skills_text(prompt_stream, skills)
                if not selected:
                    print("No skills selected.")
                    return 0
                installed = install_selected_for_platforms(
                    prompt_stream,
                    selected,
                    platforms,
                    install_dirs,
                    link_mode,
                )
            print(f"\nDone. Installed or kept {installed} skill(s).")
            return 0

        if repo_root is not None:
            print(f"Using local source: {repo_root}")
            return run(repo_root)

        with tempfile.TemporaryDirectory(prefix="claude-skills-") as temp_dir:
            archive_data = download_archive(args.archive_url)
            dl_root = safe_extract(archive_data, Path(temp_dir))
            return run(dl_root)

    except KeyboardInterrupt:
        print("\nAborted.")
        return 130
    except InstallerError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
