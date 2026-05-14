// Claw Command Deck — Secure Desktop Wrapper
// Only loads claw.outtatime.dev. No dev tools, no arbitrary navigation.

#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    tauri::Builder::default()
        .setup(|_app| {
            Ok(())
        })
        .on_navigation(|_webview, url| {
            // Only allow navigation to the Claw domain and Manus OAuth
            let allowed_origins = [
                "https://claw.outtatime.dev",
                "https://clawassist-bqyvbier.manus.space",
                "https://api.manus.im",
                "https://manus.im",
            ];
            let url_str = url.as_str();
            allowed_origins.iter().any(|origin| url_str.starts_with(origin))
        })
        .run(tauri::generate_context!())
        .expect("error while running Claw Command Deck");
}
