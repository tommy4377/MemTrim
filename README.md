# Tommy Memory Cleaner v0.2.0

Historical release of the project now known as MemTrim.

## Highlights
- Tray controls
- Taskbar-aware placement

## Requirements
- Windows 10 or 11, 64-bit
- Administrator privileges
- Microsoft Edge WebView2 Runtime

## Portable usage
Run TMC.exe as administrator, choose a profile, then optimize from the UI, tray, hotkey or CLI.

CLI examples:
    TMC.exe /Profile:Balanced
    TMC.exe /?

## Build
    cd TMC/ui
    npm install
    npm run build
    cd ../src-tauri
    cargo build --release

Output: TMC/src-tauri/target/release/TMC.exe

Maintained by @tommy4377.
