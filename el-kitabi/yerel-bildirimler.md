---
title: "Local notifications for a game's daily reason to return (Unity, Android 13+ and iOS)"
condition: "Mobile game (Android or iOS) with a daily puzzle, daily reward or timed event, or about to add one; not games for children (Apple Kids, Play Families)."
read_when: "Adding a reminder for a daily puzzle, reward or event; asking for the notification permission; a notifications switch in settings; a store or player complaint about notifications."
requires: "Unity Mobile Notifications 2.4.x (`com.unity.mobile.notifications`; Android SDK 33+, Xcode with the iOS 15.2+ SDK)"
source: "Android Developers 'Notification runtime permission' · Apple 'Asking permission to use notifications' (provisional authorization) · App Review Guidelines 4.5.3, 4.5.4 · Unity Mobile Notifications 2.4 manual and its Android page (PermissionRequest, channel importance, exact alarms) · Play Console Help 9888170 (exact alarm permissions) · vendor data: Airship 2026 benchmarks (2026-03-31), Pushwoosh 2025 · the studio's notifications research 2026-10-18"
tech: "Unity 6000.3, Mobile Notifications 2.4.x, Android 13+ and iOS"
added: "2026-10-18 · template 1.53 · the studio's notifications research for the session manager (follow-up of its daily reward and streak research)"
---
# Local notifications

## Principles
- Local notifications only: no server, nothing leaves the phone. A remote push token is a device identifier, so it would change the privacy declarations; a daily reminder doesn't need one.
- They only announce a reason the game already has (today's puzzle, a ready reward, an event's start). Click rates are low (hyper-casual ~0.8-1.1%: Pushwoosh 2025, vendor), so they never carry retention alone; no current public measurement shows how much a granted permission lifts a game's retention (the often-quoted figures are from 2013).
- The game works fully without them (App Review 4.5.4; Android asks the same).

## Asking for the permission
- Android 13+ (`POST_NOTIFICATIONS`): notifications start off on new installs. iOS shows its system dialog once; later requests don't ask again.
- Never at first launch. Ask once the value is clear, after the first daily reward or the first daily puzzle, through our own invitation ("Shall we tell you when tomorrow's puzzle is ready?"); only after a "yes" the system dialog. A rationale screen only when `shouldShowRequestPermissionRationale()` is true.
- A "no" is never asked again. A Settings "Notifications" switch opens the system settings when the permission is off. Check `areNotificationsEnabled()` before scheduling.
- Unity: on Android 13+ request with `PermissionRequest` inside a coroutine. iOS provisional authorization (no dialog; quiet delivery to Notification Centre with Keep / Turn Off buttons) exists, but "Keep" still delivers quietly (the research's reading of Apple's page; not re-verified), so it doesn't replace the real permission.

## Content and frequency
- Concrete and in the game's voice ("Today's puzzle is ready: 6 fields, 6 bees"); never guilt ("your streak will break": hedef-katmanlari-ve-geri-donus.md).
- No promotions: promotional or marketing pushes need explicit in-app opt-in consent and an in-app opt-out (4.5.4); spam is banned (4.5.3).
- At most one a day; none on a day already played; three ignored in a row → every three days, nothing after seven; opening the game resets the count. Android shows players each app's daily notification count. The cap lives in code, not in a setting.
- Time: near the player's usual session hour, else 19:00; never 22:00-09:00.

## Implementation (Mobile Notifications 2.4.x)
- One channel ("Daily", `Importance.Default`): a channel's importance can't change after it is created (only the player changes it).
- Inexact scheduling; a reminder needs no exact alarm, so declare neither permission. `USE_EXACT_ALARM` is only for alarm, timer and calendar apps (Google Play policy, Play Console Help 9888170); `SCHEDULE_EXACT_ALARM` is not pre-granted to new installs on Android 14+ for apps targeting API 33+ (the player must allow it).
- On every launch and pause: cancel what's pending and schedule the next one. Scheduled notifications survive a reboot.

## Verification
- Android 13+ fresh install: no dialog before the first daily reward; a denial keeps the game fully usable; at most one a day; none after a day already played. iOS: the dialog only after the invitation.
- Measure (Firebase, no personal data): `notification_invite` (shown, accepted, declined), `notification_permission` (granted, denied), `notification_open`; compare D7 of players who granted with those who didn't (self-selected: direction, not cause).
