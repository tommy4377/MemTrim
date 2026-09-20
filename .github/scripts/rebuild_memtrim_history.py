from __future__ import annotations
import json, os, re, shutil, subprocess, tempfile
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path.cwd(); TMP=Path(tempfile.mkdtemp(prefix="memtrim-")); W=TMP/"w"; IDX=TMP/"idx"
M=[
("d2fc594b6ef87f69b33cb1d0562919bc34d9bcb6","v1.0.0","feat(core): establish memory optimization baseline","Core engine;Administrator handling;Normal, Balanced and Gaming profiles"),
("e49bd5b716fdc90e795a6b410cdf37f55180170c","v1.1.0","feat(tray): add taskbar-aware tray controls","Tray controls;Taskbar-aware placement"),
("024866ab501ae7b905f74a97d93c268c24ca3095","v1.2.0","feat(cli): add console mode","Console mode;Script and Task Scheduler support"),
("bdc3d7760eb70483ba7afb4dc76fb55cd72ff2ff","v1.3.0","fix(config): stabilize first-run setup","Reliable AppData config;Stable first-run setup"),
("b60449ff9fa61f75b714270e7934585dd8bc1c28","v1.4.0","fix(tray): support multi-monitor placement","Multi-monitor tray placement;Desktop integration polish"),
("5863aaca94c842fc2540e28e5b3ea34d9e0581b8","v2.0.0","feat(security): add validation and rate limiting","Nine-language UI;Input validation;Rate limiting"),
("088e2d10bae9a23706f2208ab0cb0a170671bdb5","v2.1.0","fix(cli): stabilize GUI and console mode","Reliable GUI and CLI dual mode;Console attachment fixes"),
("ead7b3a5a547b8950baa679611bb787d377d3235","v2.2.0","feat(ui): add memory statistics","Memory-freed statistics;Refined compact and full views"),
("18d979f7a662a53bbed8e3d8957784d9dd6646cc","v2.3.0","perf(memory): harden optimization fallbacks","Advanced memory paths;Compatibility fallbacks;Safety improvements"),
("7e356197b63ca0410d4a44eebae56be008a8447d","v2.4.0","perf(ui): optimize accent color updates","Responsive accent picker;Reduced UI overhead"),
("e79e3b7e802108df9d67d714be72b84829d3fbd8","v2.5.0","fix(windows): improve Windows 10 rendering","Windows 10 border fixes;Dark-theme consistency"),
("ffecc2bb1d2e5101717f413cfab4efce9a66b6fc","v2.6.0","fix(windows): stabilize DPI and window geometry","DPI fixes;Window centering;Rounded-corner handling"),
("3d03090c92b43b73f6e543504419dde2818ed46f","v3.0.0","release: polish setup and layout","Setup polish;Stable 500x700 layout;Reliability cleanup"),
("1916b445696fd57f0f7658ad3462fc5b0634ffd1","v4.0.0","feat(windows): harden elevation and logging","Safer elevation;Logging improvements;Window handling fixes"),
]
def run(*a,env=None,cap=False,cwd=None):
 e=os.environ.copy(); e.update(env or {}); return subprocess.run(a,cwd=cwd or ROOT,env=e,text=True,capture_output=cap,check=True)
def go(*a): return run("git",*a,cap=True).stdout.strip()
def wr(p,s): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding="utf-8",newline="\n")
def meta(s): return tuple(go("show","-s","--format=%an%x00%ae%x00%aI",s).split("\x00"))
def load(s):
 shutil.rmtree(W,ignore_errors=True); W.mkdir(); IDX.unlink(missing_ok=True)
 e={"GIT_INDEX_FILE":str(IDX),"GIT_WORK_TREE":str(W)}; run("git","read-tree",f"{s}^{{tree}}",env=e); run("git","checkout-index","-a","-f",env=e)
def clean():
 for p in sorted(W.rglob("*"),reverse=True):
  if p.is_file() and (p.suffix.lower() in {".pfx",".p12",".ogg",".mp3",".mp4",".exe"} or p.name.lower()=="optimization_analysis.md"): p.unlink(missing_ok=True)
  elif p.is_dir() and p.name.lower() in {"releases","windows-fix","file_bordi"}: shutil.rmtree(p,ignore_errors=True)
def noup(b):
 p=b/"ui/src/components/BasicSettings.svelte"
 if p.exists(): wr(p,re.sub(r'\n\s*<div class="row">\s*<label>\s*<input[^>]*checked=\{cfg\?\.auto_update\}[^>]*/>\s*\{\$t\(\'Auto update\'\)\}\s*</label>\s*</div>\s*',"\n",p.read_text(encoding="utf-8"),flags=re.S))
 for rel,pat in {
 "ui/src/lib/types.ts":r'(?m)^\s*auto_update:\s*boolean\s*\n',
 "src-tauri/src/config/mod.rs":r'(?m)^\s*(?:pub auto_update:\s*bool,|auto_update:\s*(?:true|false),)\s*\n',
 "src-tauri/src/commands/config.rs":r'(?m)^\s*update_bool!\(auto_update\);\s*\n'}.items():
  p=b/rel
  if p.exists(): wr(p,re.sub(pat,"",p.read_text(encoding="utf-8")))
 for p in (b/"ui/src/i18n").glob("*.json") if (b/"ui/src/i18n").exists() else []:
  try:o=json.loads(p.read_text(encoding="utf-8")); o.pop("Auto update",None); wr(p,json.dumps(o,indent=2,ensure_ascii=False)+"\n")
  except: pass
def ver(b,v):
 p=b/"src-tauri/Cargo.toml"
 if p.exists(): wr(p,re.sub(r'(?m)^version = "[^"]+"',f'version = "{v}"',p.read_text(encoding="utf-8"),count=1))
 for p in [b/"src-tauri/tauri.conf.json",b/"ui/package.json"]:
  if p.exists(): o=json.loads(p.read_text(encoding="utf-8")); o["version"]=v; wr(p,json.dumps(o,indent=2,ensure_ascii=False)+"\n")
def workflow(project,exe,title):
 token="$"+"{{ github.token }}"
 return f"""name: Release portable
on:
  push:
    tags: ['v*.*.*']
permissions:
  contents: write
jobs:
  portable:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - working-directory: {project}/ui
        run: npm install
      - working-directory: {project}/ui
        run: npm run build
      - working-directory: {project}/src-tauri
        run: cargo build --release
      - name: Publish portable executable
        shell: pwsh
        env:
          GH_TOKEN: {token}
        run: |
          gh release delete "$env:GITHUB_REF_NAME" --yes 2>$null
          gh release create "$env:GITHUB_REF_NAME" "{project}/src-tauri/target/release/{exe}" --title "{title} $env:GITHUB_REF_NAME" --generate-notes
"""
def readme(tag,hi):
 bullets="\n".join("- "+x for x in hi.split(";"))
 return f"""# Tommy Memory Cleaner {tag}

Historical release of the project now known as MemTrim.

## Highlights
{bullets}

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
"""
def prep(tag,hi):
 b=W/"TMC"; noup(b); ver(b,tag[1:]); wr(W/"README.md",readme(tag,hi)); shutil.rmtree(W/".github/workflows",ignore_errors=True)
def final():
 old=W/"TMC"; new=W/"MemTrim"; old.rename(new)
 for p in W.rglob("*"):
  if p.is_file() and p.suffix.lower() in {".md",".rs",".toml",".json",".ts",".svelte",".html",".yml",".yaml",".css",".xml",".txt"}:
   try:s=p.read_text(encoding="utf-8")
   except:continue
   s=s.replace("Tommy Memory Cleaner","MemTrim").replace("TommyMemoryCleaner.exe","MemTrim.exe").replace("tommymemorycleaner.exe","memtrim.exe").replace("TommyMemoryCleaner.lnk","MemTrim.lnk").replace("TMC •","MemTrim •").replace('"tmc-ui"','"memtrim-ui"'); wr(p,s)
 p=new/"src-tauri/Cargo.toml"
 if p.exists(): wr(p,re.sub(r'(?m)^name = "TommyMemoryCleaner"$','name = "MemTrim"',p.read_text(encoding="utf-8"),count=1).replace('OriginalFilename = "TommyMemoryCleaner.exe"','OriginalFilename = "MemTrim.exe"'))
 p=new/"src-tauri/tauri.conf.json"
 if p.exists(): o=json.loads(p.read_text(encoding="utf-8")); o["productName"]="MemTrim"; o["version"]="5.0.0"; o.setdefault("bundle",{})["targets"]=[]; o["bundle"].pop("createUpdaterArtifacts",None); o["plugins"]={}; wr(p,json.dumps(o,indent=2,ensure_ascii=False)+"\n")
 noup(new); ver(new,"5.0.0")
 wr(W/".gitignore","target/\n**/target/\ndist/\n**/dist/\nnode_modules/\n.svelte-kit/\n.vite/\n.vscode/\n.idea/\n*.log\n*.tmp\n.env\n.env.*\n*.pfx\n*.p12\n*.exe\n*.dll\n*.pdb\nMemTrim/src-tauri/gen/\n")
 wr(W/"README.md","""# MemTrim

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
""")
 docs={
 "CONTRIBUTING.md":"# Contributing\n\nKeep changes focused. Run frontend checks/build plus cargo fmt --check and cargo check before a pull request. Do not commit binaries, logs, credentials or signing keys.\n",
 "SECURITY.md":"# Security Policy\n\nSecurity fixes target the latest release. Do not post exploit details or sensitive logs publicly. Use GitHub private vulnerability reporting when available; otherwise request a private contact in a minimal issue.\n",
 "SUPPORT.md":"# Support\n\nFor bugs include MemTrim version, Windows version, reproduction steps, expected/actual behavior and sanitized logs. Use the feature-request form for ideas.\n",
 "CODE_OF_CONDUCT.md":"# Code of Conduct\n\nBe respectful, constructive and specific. Harassment, threats, discriminatory abuse, doxxing and deliberate disruption are not acceptable. Maintainers may remove violating contributions and restrict repeated or severe abuse.\n",
 "NOTICE.md":"# Notices\n\nMemTrim was originally Tommy Memory Cleaner. Primary maintainer: @tommy4377. Gabriele R. / @LAMAgalletta0IQ contributed Windows elevation, logging and window-handling work incorporated into v4.\n"}
 for n,s in docs.items(): wr(W/n,s)
 wr(W/".editorconfig","root = true\n\n[*]\ncharset = utf-8\nend_of_line = lf\ninsert_final_newline = true\ntrim_trailing_whitespace = true\n")
 wr(W/".gitattributes","* text=auto eol=lf\n*.bat text eol=crlf\n*.cmd text eol=crlf\n*.png binary\n*.ico binary\n*.cur binary\n")
 wr(W/".github/CODEOWNERS","* @tommy4377\n")
 wr(W/".github/PULL_REQUEST_TEMPLATE.md","## Summary\n\n## Testing\n- [ ] Frontend check/build\n- [ ] cargo fmt --check\n- [ ] cargo check\n- [ ] Windows test when applicable\n")
 wr(W/".github/ISSUE_TEMPLATE/config.yml","blank_issues_enabled: false\ncontact_links: []\n")
 wr(W/".github/ISSUE_TEMPLATE/bug_report.yml",'name: Bug report\ndescription: Report a reproducible problem\ntitle: "[Bug]: "\nlabels: ["bug"]\nbody:\n  - type: textarea\n    id: problem\n    attributes: {label: What happened?}\n    validations: {required: true}\n  - type: textarea\n    id: reproduce\n    attributes: {label: Steps to reproduce}\n    validations: {required: true}\n')
 wr(W/".github/ISSUE_TEMPLATE/feature_request.yml",'name: Feature request\ndescription: Suggest an improvement\ntitle: "[Feature]: "\nlabels: ["enhancement"]\nbody:\n  - type: textarea\n    id: usecase\n    attributes: {label: Problem or use case}\n    validations: {required: true}\n  - type: textarea\n    id: proposal\n    attributes: {label: Proposed solution}\n    validations: {required: true}\n')
 wr(W/".github/dependabot.yml","version: 2\nupdates:\n  - package-ecosystem: npm\n    directory: /MemTrim/ui\n    schedule: {interval: weekly}\n  - package-ecosystem: cargo\n    directory: /MemTrim/src-tauri\n    schedule: {interval: weekly}\n  - package-ecosystem: github-actions\n    directory: /\n    schedule: {interval: weekly}\n")
 wr(W/".github/workflows/ci.yml","name: CI\non:\n  push: {branches: [main]}\n  pull_request: {branches: [main]}\npermissions: {contents: read}\njobs:\n  validate:\n    runs-on: windows-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-node@v4\n        with: {node-version: 20}\n      - working-directory: MemTrim/ui\n        run: npm install\n      - working-directory: MemTrim/ui\n        run: npm run check\n      - working-directory: MemTrim/ui\n        run: npm run build\n      - working-directory: MemTrim/src-tauri\n        run: cargo fmt --check\n      - working-directory: MemTrim/src-tauri\n        run: cargo check\n")
 shutil.rmtree(W/".github/workflows",ignore_errors=True)
 shutil.rmtree(W/".github/scripts",ignore_errors=True)
def tree():
 e={"GIT_INDEX_FILE":str(IDX),"GIT_WORK_TREE":str(W)}; run("git","add","-A",env=e); return run("git","write-tree",env=e,cap=True).stdout.strip()
def commit(t,parent,msg,who):
 n,e,d=who; env={"GIT_AUTHOR_NAME":n,"GIT_AUTHOR_EMAIL":e,"GIT_AUTHOR_DATE":d,"GIT_COMMITTER_NAME":n,"GIT_COMMITTER_EMAIL":e,"GIT_COMMITTER_DATE":d}
 a=["git","commit-tree",t]+(["-p",parent] if parent else [])
 return subprocess.run(a,input=msg+"\n",text=True,capture_output=True,check=True,env={**os.environ,**env}).stdout.strip()
parent=None; tags={}
for src,tag,msg,hi in M:
 load(src); clean(); prep(tag,hi); parent=commit(tree(),parent,msg,meta(src)); tags[tag]=parent
load(M[-1][0]); clean(); final()
parent=commit(tree(),parent,"feat!: rebrand as MemTrim and switch to portable-only distribution",("tommy4377","129632197+tommy4377@users.noreply.github.com",datetime.now(timezone.utc).isoformat())); tags["v5.0.0"]=parent
run("git","update-ref","refs/heads/memtrim-rebuilt",parent)
for tag,sha in tags.items(): run("git","update-ref","refs/tags/"+tag,sha)
Path("rebuild-manifest.json").write_text(json.dumps({"head":parent,"tags":tags},indent=2)+"\n",encoding="utf-8")
