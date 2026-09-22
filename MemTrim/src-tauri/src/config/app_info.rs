// Application metadata constants - centralized for consistency
pub const APP_NAME: &str = "MemTrim";
pub const COMPANY_NAME: &str = "MemTrim";
// Single source of truth: the version in Cargo.toml (keep tauri.conf.json in
// sync — the bundler/installer reads its own `version` field).
pub const VERSION: &str = env!("CARGO_PKG_VERSION");
pub const VERSION_FULL: &str = concat!(env!("CARGO_PKG_VERSION"), ".0");
pub const FILE_DESCRIPTION: &str = "Advanced Memory Optimization Tool for Windows";
pub const COPYRIGHT: &str = "© 2025-2026 tommy4377";

// Get application version in different formats
pub fn get_version() -> &'static str {
    VERSION
}

pub fn get_version_full() -> &'static str {
    VERSION_FULL
}

pub fn get_app_name() -> &'static str {
    APP_NAME
}

pub fn get_company_name() -> &'static str {
    COMPANY_NAME
}

pub fn get_copyright() -> &'static str {
    COPYRIGHT
}
