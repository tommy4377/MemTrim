# MemTrim

MemTrim is a lightweight portable Windows memory-optimization utility, formerly Tommy Memory Cleaner.

## Features
- Eight targetable Windows memory areas
- Normal, Balanced and Gaming profiles
- Scheduled and low-memory automatic optimization
- Tray memory indicator and global hotkey
- Process exclusions and administrator elevation
- Compact/full views, themes and nine UI languages
- GUI and CLI from the same portable executable

## Portable only
MemTrim ships only as MemTrim.exe. There is no installer, in-app auto-updater, updater signing key or latest.json manifest.

## Requirements
- Windows 10 or 11, 64-bit
- Administrator privileges
- Microsoft Edge WebView2 Runtime

## Build
    cd MemTrim/ui
    npm install
    npm run build
    cd ../src-tauri
    cargo build --release

Output: MemTrim/src-tauri/target/release/MemTrim.exe

## Project health
See CONTRIBUTING.md, SECURITY.md, SUPPORT.md, CODE_OF_CONDUCT.md and NOTICE.md.

## Credits
Created and maintained by @tommy4377.
Gabriele R. / @LAMAgalletta0IQ contributed Windows elevation, logging and window-handling work in the v4 line.

## License
No open-source license is granted yet. A project-wide license can be added after all copyright holders of existing contributions agree to the terms.
