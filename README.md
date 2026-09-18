<div align="center">

# MemTrim

**A lightweight, portable Windows memory optimization utility.**

[![CI](https://github.com/tommy4377/MemTrim/actions/workflows/ci.yml/badge.svg)](https://github.com/tommy4377/MemTrim/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/tommy4377/MemTrim?display_name=tag&sort=semver)](https://github.com/tommy4377/MemTrim/releases/latest)
[![License](https://img.shields.io/github/license/tommy4377/MemTrim)](LICENSE)
![Windows](https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-0078D4?logo=windows11&logoColor=white)

![Rust](https://img.shields.io/badge/Rust-000000?logo=rust&logoColor=white)
![Tauri](https://img.shields.io/badge/Tauri%202-24C8DB?logo=tauri&logoColor=white)
![Svelte](https://img.shields.io/badge/Svelte%205-FF3E00?logo=svelte&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)

</div>

MemTrim gives you direct control over several Windows memory areas from a compact desktop UI, the system tray, a global hotkey, scheduled automation or the command line. It ships as a **single portable executable**: no installer and no in-app updater.

## Highlights

- **Eight memory targets** — optimize selected Windows memory areas instead of applying one opaque cleanup action.
- **Three profiles** — Normal, Balanced and Gaming presets for different workloads.
- **Automatic optimization** — scheduled runs and low-memory triggers.
- **Tray-first workflow** — live memory indicator, quick controls and global hotkey support.
- **Process exclusions** — keep selected applications out of automated optimization flows.
- **GUI + CLI** — both interfaces are provided by the same executable.
- **Compact and full views** — multiple themes plus nine UI languages.
- **Native Windows integration** — Rust backend using Windows/NT APIs where appropriate.

## Download

Download the latest portable build from [GitHub Releases](https://github.com/tommy4377/MemTrim/releases/latest).

```text
MemTrim.exe
```

MemTrim requires **Windows 10 or Windows 11 (64-bit)**, the Microsoft Edge WebView2 Runtime and administrator privileges for operations that need elevated Windows access.

## Usage notes

Memory optimization is workload-dependent. More free RAM does not automatically mean better performance, so use the profiles and automation conservatively and compare behavior before and after changing your setup.

The application can run from any writable location. Configuration and runtime state are managed separately from the executable so the release itself remains portable.

## Build from source

Prerequisites:

- Node.js
- Rust stable
- Tauri 2 Windows prerequisites
- Microsoft Edge WebView2 Runtime

```bash
cd MemTrim/ui
npm ci
npm run check
npm run build

cd ../src-tauri
cargo fmt --check
cargo check --locked
cargo build --release --locked
```

Portable executable:

```text
MemTrim/src-tauri/target/release/MemTrim.exe
```

## Project layout

```text
MemTrim/
├─ ui/          Svelte 5 + TypeScript frontend
└─ src-tauri/   Rust/Tauri backend and Windows integration
```

CI validates the frontend and Rust backend on GitHub Actions. Version tags publish only the portable `MemTrim.exe`.

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), [SUPPORT.md](SUPPORT.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Credits

Maintained by [@tommy4377](https://github.com/tommy4377).

Gabriele R. / [@LAMAgalletta0IQ](https://github.com/LAMAgalletta0IQ) contributed Windows elevation, logging and window-handling work in the v4 line.

## License

Released under the [MIT License](LICENSE).
