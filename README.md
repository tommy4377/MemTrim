# Tommy Memory Cleaner v0.6.0

Historical release of the project now known as MemTrim.

## Highlights
- Setup polish
- Stable 500x700 layout
- Reliability cleanup

## Requirements
- Windows 10 or 11, 64-bit
- Administrator privileges
- Microsoft Edge WebView2 Runtime

## Portable usage
Run TommyMemoryCleaner.exe as administrator, choose a profile, then optimize from the UI, tray, hotkey or CLI.

CLI examples:
    TommyMemoryCleaner.exe /Profile:Balanced
    TommyMemoryCleaner.exe /?

## Build
    cd TMC/ui
    npm install
    npm run build
    cd ../src-tauri
    cargo build --release

Output: TMC/src-tauri/target/release/TommyMemoryCleaner.exe

Maintained by @tommy4377.
