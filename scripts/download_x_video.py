#!/usr/bin/env python
"""Download video media from an X/Twitter URL for the AI Threads workflow."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_OUTPUT_DIR = Path.cwd() / "work" / "ai-threads-media"


def find_downloader() -> list[str] | None:
    exe = shutil.which("yt-dlp")
    if exe:
        return [exe]

    try:
        result = subprocess.run(
            [sys.executable, "-m", "yt_dlp", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError:
        return None

    if result.returncode == 0:
        return [sys.executable, "-m", "yt_dlp"]

    return None


def find_ffmpeg() -> str | None:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe

    try:
        import imageio_ffmpeg
    except ImportError:
        return None

    return imageio_ffmpeg.get_ffmpeg_exe()


def run_check() -> int:
    downloader = find_downloader()
    ffmpeg = find_ffmpeg()
    if not downloader:
        print(
            json.dumps(
                {
                    "ready": False,
                    "missing": "yt-dlp",
                    "install": f"{sys.executable} -m pip install -U yt-dlp",
                    "ffmpeg": ffmpeg,
                },
                ensure_ascii=False,
            )
        )
        return 2

    version = subprocess.run(
        downloader + ["--version"],
        text=True,
        capture_output=True,
        check=False,
    )
    print(
        json.dumps(
            {
                "ready": version.returncode == 0,
                "downloader": " ".join(downloader),
                "version": version.stdout.strip(),
                "ffmpeg": ffmpeg,
            },
            ensure_ascii=False,
        )
    )
    return 0 if version.returncode == 0 else version.returncode


def build_command(args: argparse.Namespace, downloader: list[str]) -> list[str]:
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    template = str(output_dir / "%(extractor)s_%(id)s_%(title).80s.%(ext)s")
    ffmpeg = find_ffmpeg()
    command = downloader + [
        "--no-playlist",
        "--format",
        args.format,
        "--merge-output-format",
        "mp4",
        "--write-info-json",
        "--write-thumbnail",
        "--print",
        "after_move:filepath",
        "--output",
        template,
    ]

    if ffmpeg:
        command += ["--ffmpeg-location", ffmpeg]

    if args.cookies_from_browser:
        command += ["--cookies-from-browser", args.cookies_from_browser]

    command.append(args.url)
    return command


def download(args: argparse.Namespace) -> int:
    downloader = find_downloader()
    if not downloader:
        print("yt-dlp is not installed. Run with --check for the install command.", file=sys.stderr)
        return 2

    command = build_command(args, downloader)
    result = subprocess.run(command, text=True, capture_output=True, check=False)

    payload = {
        "ok": result.returncode == 0,
        "output_dir": str(Path(args.output_dir).resolve()),
        "stdout": result.stdout.strip().splitlines(),
        "stderr": result.stderr.strip().splitlines()[-12:],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return result.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download video media from an X/Twitter URL.")
    parser.add_argument("url", nargs="?", help="X/Twitter status URL.")
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Folder for downloaded media and metadata.",
    )
    parser.add_argument(
        "--cookies-from-browser",
        choices=["chrome", "edge", "firefox", "brave", "chromium", "opera", "vivaldi"],
        help="Use browser cookies when X requires login context.",
    )
    parser.add_argument(
        "--format",
        default="bv*[height<=1080]+ba/b[height<=1080]/b",
        help="yt-dlp format selector.",
    )
    parser.add_argument("--check", action="store_true", help="Check whether yt-dlp is available.")
    args = parser.parse_args()

    if not args.check and not args.url:
        parser.error("url is required unless --check is used")

    return args


def main() -> int:
    args = parse_args()
    if args.check:
        return run_check()
    return download(args)


if __name__ == "__main__":
    raise SystemExit(main())
