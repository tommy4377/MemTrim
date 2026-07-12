# Tommy Memory Cleaner v0.8.0

Historical release of the project now known as MemTrim.

## Highlights

- Safer elevation
- Logging improvements
- Window handling fixes

## Requirements

- Windows 10 or Windows 11, 64-bit
- Administrator privileges
- Microsoft Edge WebView2 Runtime

## Portable usage

Run `TommyMemoryCleaner.exe` as administrator, choose a profile, then optimize from the UI, tray, hotkey or CLI.

```text
TommyMemoryCleaner.exe /Profile:Balanced
TommyMemoryCleaner.exe /?
```

## Build from source

```powershell
cd TMC/ui
npm install
npm run build
cd ../src-tauri
cargo build --release
```

Output: `TMC/src-tauri/target/release/TommyMemoryCleaner.exe`.

## Credits

Maintained by [@tommy4377](https://github.com/tommy4377).

This release includes Windows elevation, logging and window-handling contributions from [@LAMAgalletta0IQ](https://github.com/LAMAgalletta0IQ).

## License

Released under the [MIT License](LICENSE).
