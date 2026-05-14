# Claw Command Deck — Desktop App

Secure, chromeless desktop wrapper for [claw.outtatime.dev](https://claw.outtatime.dev). Built with Tauri 2 (Rust + system WebView).

## Security

- **No Chromium bundled** — uses macOS WebKit (WKWebView)
- **Navigation locked** to `claw.outtatime.dev` and Manus OAuth domains only
- **No dev tools** in release builds
- **No file system access** — minimal Tauri permissions (`core:default` only)
- **CSP enforced** — only loads resources from allowed origins
- **Tiny binary** (~5MB vs Electron's ~150MB)

## Install

Download the latest `.dmg` from [Releases](../../releases), open it, drag to Applications.

## Build locally

Requires Rust and Xcode Command Line Tools.

```bash
cargo install tauri-cli --version "^2"
cargo tauri build
```

The `.dmg` will be in `src-tauri/target/release/bundle/dmg/`.

## CI/CD

Push to `main` builds both Apple Silicon and Intel `.dmg` files via GitHub Actions. Tag with `v*` to create a release.

```bash
git tag v1.0.0
git push origin v1.0.0
```
