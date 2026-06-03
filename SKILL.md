---
name: ai-threads-post-writer
description: Use when transforming AI-related X posts, X videos, linked articles, pasted post text, or rough notes into the user's personal Traditional Chinese Threads drafts. Supports semi-automatic source review, concise community-oriented rewriting, attribution, and copy-ready output without publishing unless explicitly requested.
---

# AI Threads Post Writer

## Default Mode

Draft-first and semi-automatic. Prepare copy-ready Threads content, but do not publish or schedule anything unless the user explicitly asks and a verified Threads publishing tool is available.

Default language is Traditional Chinese. Keep English only for product names, model names, quoted terms, or when the user asks for an English variant.

## Workflow

1. Gather inputs
   - Accept X post URLs, pasted X text, downloaded video paths, article URLs, screenshots, or rough notes.
   - For X URLs with video, run `scripts/download_x_video.py` before drafting when the user asks for video handling or when video context is required.
   - If an X post or pasted post has an external URL, inspect the linked official/original website before drafting.
   - If only post text is available, draft from that text and clearly avoid claiming unverified details.
   - If video is provided, summarize the visible/spoken content before drafting the Threads post.

2. Review official/original sources
   - Read `references/source-rules.md` before summarizing source-backed claims.
   - Prefer the official website, official blog, docs, release notes, paper, GitHub repo, model card, or direct company/person announcement.
   - Summarize what the official source says in plain Traditional Chinese before writing the Threads draft.
   - Pull out product names, feature names, launch status, supported platforms/apps, limits, pricing, and target users when available.
   - If the linked URL is not official, look for the official source when feasible and label the non-official URL separately.
   - If official source access fails, say what was checked and draft only from available source material.

3. Extract the angle
   - Identify the core AI news, product update, research result, workflow tip, or community discussion point.
   - Separate source facts from the user's possible opinion.
   - Prefer the angle that is useful to AI builders, product people, operators, and AI community readers.

4. Rewrite in the user's Threads style
   - Read `references/writing-style.md` when style guidance is needed.
   - Start with a first-person, useful, or lively community-style opening instead of a generic news summary.
   - Keep the post energetic, plainspoken, conversational, and credible.
   - Use `📍` feature sections when summarizing multiple concrete capabilities.
   - Avoid hype, press-release wording, and invented claims.
   - Include one practical takeaway, implication, or discussion prompt when it fits naturally.

5. Package the output
   - Include an "官方網站整理" section when an external URL or official source was reviewed.
   - Provide one primary draft and, when useful, one alternate hook.
   - Include source links and media notes.
   - Include the local downloaded video path when video download succeeds.
   - Include a short publish checklist.
   - If the draft may exceed Threads limits, split it into a short thread or provide a tighter version.

## Video Download

Use `scripts/download_x_video.py` for semi-automatic X video download.

Check readiness:

```powershell
python C:\Users\situn\.codex\skills\ai-threads-post-writer\scripts\download_x_video.py --check
```

Download:

```powershell
python C:\Users\situn\.codex\skills\ai-threads-post-writer\scripts\download_x_video.py "https://x.com/.../status/..."
```

If public download fails because X requires login context, retry with browser cookies:

```powershell
python C:\Users\situn\.codex\skills\ai-threads-post-writer\scripts\download_x_video.py "https://x.com/.../status/..." --cookies-from-browser chrome
```

Default output folder is `work/ai-threads-media` under the current workspace. The downloader defaults to a 1080p maximum format for Threads compatibility. Do not repost downloaded media unless the user has the rights or the post is being used under an appropriate reuse policy.

## Output Format

```markdown
**Threads 草稿**
[copy-ready draft]

**官方網站整理**
- [plain-language source summary]

**備用開頭**
[optional alternate hook]

**來源**
- [source label](source URL)

**媒體**
- [video/image path or note]

**發布前檢查**
- 事實是否已從原始來源確認：
- 是否要附影片/圖片：
- 是否保留原文連結：
- 是否需要縮短：
```

## Source Rules

Read `references/source-rules.md` when source quality, attribution, or verification is unclear.

Never invent dates, benchmark numbers, model capabilities, company claims, release status, or pricing. If the source is only an X post and cannot be verified, say so briefly in the notes.

## Publishing Guardrail

Do not call a Threads publishing API by default. If the user asks to publish, first verify the available Threads tool/account health with a harmless read or account check. If publishing health cannot be verified, return the copy-ready draft and explain the blocker.
