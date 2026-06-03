# AI Threads Post Writer

Codex skill for turning AI-related X posts, videos, official links, and rough notes into copy-ready Traditional Chinese Threads drafts.

This skill is built for a semi-automatic social posting workflow:

1. Inspect the X post and any attached official/original URL.
2. Download X video media when available.
3. Keep video output Threads-friendly with a 1080p maximum by default.
4. Summarize official source details in plain Traditional Chinese.
5. Rewrite the post in an energetic, white-space-friendly AI community style.
6. Return a copy-ready Threads draft, source notes, media path, and publishing checklist.

## What It Does

- Drafts Threads posts in Traditional Chinese.
- Uses a lively first-person community style instead of neutral news summaries.
- Opens official/original websites when a post includes URLs.
- Separates verified source facts from inferred commentary.
- Downloads X videos through `yt-dlp`.
- Uses bundled or system `ffmpeg` to merge video/audio.
- Defaults to 1080p max format for easier Threads publishing.
- Does not publish automatically unless a verified Threads publishing tool is added later.

## Folder Structure

```text
ai-threads-post-writer/
  SKILL.md
  README.md
  agents/
    openai.yaml
  references/
    source-rules.md
    writing-style.md
  scripts/
    download_x_video.py
```

## Install

Copy this folder into your Codex skills directory:

```powershell
Copy-Item -Path .\ai-threads-post-writer -Destination C:\Users\situn\.codex\skills\ai-threads-post-writer -Recurse -Force
```

Restart Codex after installing or updating the skill.

## Usage

Invoke the skill explicitly:

```text
Use $ai-threads-post-writer 幫我把這則 X 影片整理成 Threads 貼文：
https://x.com/.../status/...
```

For posts with official links:

```text
Use $ai-threads-post-writer 幫我整理這則 AI 產品更新，先看官方網站再改寫成 Threads：
[X post URL or official URL]
```

## Video Download

Check readiness:

```powershell
python C:\Users\situn\.codex\skills\ai-threads-post-writer\scripts\download_x_video.py --check
```

Download a public X video:

```powershell
python C:\Users\situn\.codex\skills\ai-threads-post-writer\scripts\download_x_video.py "https://x.com/.../status/..."
```

If X requires login context:

```powershell
python C:\Users\situn\.codex\skills\ai-threads-post-writer\scripts\download_x_video.py "https://x.com/.../status/..." --cookies-from-browser chrome
```

Downloaded media is written to:

```text
work/ai-threads-media
```

## Output Format

The skill returns:

- Threads draft
- Official website summary when a URL was reviewed
- Alternate opening
- Source links
- Downloaded media path
- Publishing checklist

## Current Guardrail

This is a draft-first workflow. It prepares posts and media, but it does not publish to Threads automatically.

To add full publishing later, connect a Threads API or third-party publishing service, add a dry-run mode, and require explicit confirmation before posting.
