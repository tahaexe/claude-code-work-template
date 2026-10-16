---
title: Browser connection (Claude in Chrome): each account's own Chrome profile
condition: Every project (any task may need the browser).
read_when: Setting up a Claude account's browser profile on a machine; Claude in Chrome not connected, errors or timeouts, no tab opens, a tab "open" that the user can't see, or an unexpected browser is listed.
requires: Google Chrome with the Claude in Chrome extension (Chrome Web Store) signed in with the session's claude.ai account; Claude Code signed in with `/login`.
source: Field notes from a project on Windows 11, 2026-10-08 (Opera GX, Chrome and Edge tried) · Claude Code docs "Use Claude Code with Chrome" (code.claude.com/docs/en/chrome) · user reports anthropics/claude-code#70542, #89302
tech: Claude in Chrome 1.0.99 · Chrome · Windows 11. Recheck when the extension can name browsers or Opera gets full tab groups.
added: 2026-10-08 · distilled by Claude from a project session · 2026-10-08 troubleshooting order (user report: "open" but nothing visible)
---
# Browser connection: each account's own Chrome profile

## Rule (user decision, 2026-10-08)
- Chrome profiles only: no other browser, even one the extension supports.
- Each Claude account works only in its own Chrome profile, named after the account. Never act in another profile or browser (people's profiles, other accounts' profiles, a browser someone else uses), even if it is listed.
- Account name = the claude.ai login email's part before `@` (e.g. `alex`); unsure → ask the user once.
- Machine facts (a profile folder that differs from the name, browsers others use) → the machine's global CLAUDE.md, "Tarayıcı" section.

## Setup (once per account and machine)
1. Claude: `Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList '--profile-directory="<name>"', 'https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn'` → creates the profile (default display name "Chrome'unuz" / "Your Chrome") and opens the extension page in it.
2. User (Claude can't: sign-in, permission grant, `chrome://` pages): skip Chrome sign-in (no Google account needed) → **Add to Chrome → Add extension** → sign the extension in with this Claude account → profile icon → **Customize profile** → name = `<name>`.
3. Claude verifies: `list_connected_browsers` lists it (`inUse: true`), `tabs_context_mcp` with `createIfEmpty` returns a tab group, a test page loads; then close the test tab.

## Daily use
- Only browsers signed in with the session's account are listed, all as generic "Browser N" (positional per reports; a name typed on the Connect screen never reaches Claude Code: #70542, #89302). Several listed → tell them apart by `deviceId`; never pick one yourself (the tool asks the user).
- Profile not running → start it with the step-1 command without the URL. Close only your own tabs (`tabs_close_mcp`); never kill `chrome.exe`: all profiles share one process.
- Two sessions of one account share its profile; each gets its own tab group. Windows: several Claude Code sessions using Chrome at once can hit a named-pipe conflict (EADDRINUSE) → restart the session (docs).

## Troubleshooting (in this order; do each step yourself)
1. **"Open" but the user sees nothing:** the tab is in your own profile's window, not the user's. Bring it forward with the step-1 command without the URL (opens a focused window of your profile) and tell the user that window's profile name and your tab group's name; it may have been behind, minimized, or on another monitor or virtual desktop.
2. **Wrong browser:** `list_connected_browsers`. Several listed, or your tab group isn't in this machine's profile window → the session may be driving the same account's browser on another computer; switch to this machine's (`switch_browser`, the user picks on the Connect screen).
3. **Errors or timeouts** (not connected, calls hang): the desktop app's connector tools, `session_connectors_status` then `reconnect_session_connector` for Claude in Chrome; then `tabs_context_mcp` with `createIfEmpty`, open a test page and ask the user whether they see it.
4. **Still failing:** restart only your profile: close its window (your tabs via `tabs_close_mcp`; tools failing → ask the user to close that one window), then start it with the step-1 command. Extension signed out → the user signs it in there.
5. **Last resort:** a full Chrome restart closes every profile, the user's too → ask the user to do it; never kill `chrome.exe` yourself.

## Pitfalls
- **Opera GX:** connects, but every tab group vanishes at once (`Failed to query tabs: No group with id …`), so no tab opens. The extension groups one new tab and Opera drops the group (its tab grouping, Tab Islands, is incomplete). Not supported; use Chrome.
- **Not listed after the browser starts:** the extension isn't signed in, or uses another account. A profile with another account → make a new profile; never switch its sign-in.
- **`switch_browser`** (Connect screen) runs only with 2+ connected browsers: "No other browsers available to switch to".
- **`chrome://` pages** can't be automated ("Can't interact with browser-internal … URLs"): profile and browser settings are the user's.
- **Diagnose from disk:** extension `%LOCALAPPDATA%\Google\Chrome\User Data\<profile>\Extensions\fcoeoabgfenejglbffodgkkbkcdhcgfn`; native host `HKCU\Software\Google\Chrome\NativeMessagingHosts\com.anthropic.claude_code_browser_extension`; profiles and display names: `User Data\Local State` → `profile.info_cache`.
