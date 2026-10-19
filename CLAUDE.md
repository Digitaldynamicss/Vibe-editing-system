# Vibe Editing project: [project name]

Talking-head videos edited as code with HyperFrames, following the Vibe Editing System
(Ideabro Studio): transcribe → pull frames → beat sheet → rough cut → effects → preview → render.

## Folders

| Folder | Holds | Rule |
|---|---|---|
| `input/` | Original footage as delivered | **Read-only. Never overwrite, re-encode, trim or rename in place.** Work from copies in `work/`. |
| `assets/` | Logos (`logos/`), music (`music/`), sound effects (`sfx/`), images | Only media the client has the rights to use. |
| `refs/` | Style references (screenshots, GIFs, short clips) | Study by pulling frames; build "similar, not a copy". |
| `project/` | HyperFrames compositions, one folder per version (`v1`, `v2`, …) | Save a new version before each round of notes. |
| `previews/` | Snapshots and short preview renders for review | Disposable. |
| `exports/` | Approved final renders | Only after sign-off. |
| `work/` | Transcripts, extracted frames, proxies, rough-cut intermediates | Git-ignored, regenerable. |

## Working rules

- Plan first: write a beat sheet (time, exact words, on-screen element, position, sound) and wait for OK.
- Rough cut before effects. Never cut inside a word; use word timings from `work/<take>.words.json`.
- Every effect starts on a named word. Snapshot frames (`npx hyperframes snapshot`) and check them before reporting done.
- Reels safe zone (9:16): no text in the bottom 20% or near the right edge.
- Spell names exactly as listed below; fix the transcript and captions to match.

## Names to spell correctly

- [your name], [brand], [product]

## Environment (cloud container)

Run `source scripts/setup.sh` at the start of each new session and in every shell that runs
HyperFrames: the container is ephemeral, and it exports `HYPERFRAMES_BROWSER_PATH` (HyperFrames
cannot download its own Chrome here).

- Transcribe with `python3 scripts/transcribe.py input/<take>.mp4 work/<take>.words.json --names "..."`,
  then import into a project with `npx hyperframes transcribe work/<take>.words.json -d project/<v>`.
- The render browser cannot reach CDNs. Vendor scripts locally (e.g. `project/<v>/vendor/gsap.min.js`
  via `npm pack gsap@<version>`) instead of `<script src="https://cdn...">`.
- Load fonts as local files for the same reason.
- `project/selftest/` is the setup test: captions + punch-in synced to word timings. Copy it as a starting point.
