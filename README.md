# MemTrim

**MemTrim** is a lightweight Windows 10/11 memory optimization utility built with Rust, Tauri 2 and Svelte. It can optimize selected Windows memory areas manually, from the tray, by global hotkey, from the CLI, or through its automatic memory-optimization scheduler.

## Highlights

- Multiple memory targets, including working sets, standby lists and system caches.
- Normal, Balanced and Gaming optimization profiles.
- Automatic memory optimization by interval or free-memory threshold.
- Live tray memory monitor with customizable warning levels and colors.
- Global optimization hotkey and process exclusions.
- Compact/full views, light/dark themes and nine UI languages.
- Console mode for scripts and Task Scheduler.
- Portable-only distribution.

## Download

Download the latest `MemTrim-vX.Y.Z-portable.exe` from **Releases**.

There is **no installer and no built-in software auto-updater**. Updating MemTrim is intentionally manual: replace the portable executable with the newer release.

Requirements: Windows 10 or Windows 11 (64-bit), WebView2, and administrator privileges for memory-management operations.

## Usage

Launch MemTrim, select an optimization profile and press **Optimize**. The automatic optimization settings control RAM cleanup only; they do not update the application.

CLI examples:

```bat
MemTrim.exe /WorkingSet /StandbyList
MemTrim.exe /Profile:Balanced
MemTrim.exe /?
```

## Build from source

Prerequisites: Node.js 20+, stable Rust, and the Windows build dependencies required by Tauri 2.

```bash
git clone https://github.com/tommy4377/Tommy-Memory-Cleaner.git
cd Tommy-Memory-Cleaner/TMC/ui
npm install
cd ..
npx --yes @tauri-apps/cli@2 build --no-bundle
```

The portable executable is generated under `TMC/src-tauri/target/release/`.

## Release workflow

Pushing a semantic-version tag such as `v5.1.0` runs `.github/workflows/release.yml`. The workflow builds with `--no-bundle` and publishes **only** `MemTrim-v5.1.0-portable.exe`.

No NSIS/MSI installer, updater manifest, signature sidecar, or `latest.json` is generated.

## Project layout

- `TMC/ui` — Svelte + TypeScript frontend.
- `TMC/src-tauri` — Rust/Tauri backend, Windows integration, tray, hotkeys and CLI.
- `.github/workflows/release.yml` — portable-only tagged release pipeline.

## Maintainer

Created and maintained by [Tommy437 (@tommy4377)](https://github.com/tommy4377).

## License

© 2026 Tommy437. All rights reserved. This repository does not currently include an open-source license; contact the maintainer regarding reuse.
