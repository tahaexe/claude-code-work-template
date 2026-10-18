---
title: "Game feel: response timing, UI motion, reduce motion, haptics, screen shake"
condition: "Unity game project with player-facing UI or touch input (every studio game; haptics for Android and iOS)."
read_when: "Feel or juice work: tap feedback, popup and celebration timings, vibration, screen shake, sound timing; adding the reduce-motion switch; measuring tap-to-response latency; choosing a haptics library."
requires: "—"
source: "Kaaresoja, Brewster & Lantz 2014 (ACM TAP, touchscreen feedback latency) · Android Developers: Haptics design principles and Haptic feedback (2026-10-06), HapticFeedbackConstants, ValueAnimator, Settings.Global, Frame Pacing · Apple HIG (motion, Reduce Motion, Playing haptics) · Material 3 motion tokens · WCAG 2.2 2.3.2 · Unity 6.3: Handheld.Vibrate, Audio Manager, AndroidApplication.InvokeOnUIThread; Input System 1.18 timing; UUM-3745 · screen shake after Squirrel Eiserloh's GDC talk (Bevy's 2D example) · Singhal & Schneider, CHI 2021 · the studio's UI market review and its game-feel and touch-latency research, 2026-10-18 · interruptible motion: idea from nextlevelbuilder/ui-ux-pro-max-skill (read 2026-10-18), rewritten"
tech: "Unity 6000.3; Android View.performHapticFeedback, iOS UIFeedbackGenerator"
added: "2026-10-18 · template 1.52 · the motion and feedback rules of the studio's UI quality guide · template 1.53: the studio's game-feel and touch-latency research, interruptible motion"
---
# Game feel

## 1. Response timing
- **Budgets after touch-down** (Kaaresoja et al. 2014, virtual buttons on a phone): haptic 5-50 ms, audio 20-70 ms, visual 30-85 ms; quality drops past ~70-100 ms (haptic, audio) and ~100-150 ms (visual), 300 ms is worst. Out-of-sync haptics feel broken (Android's haptics principles). Measure touch to first changed pixel or sound with a 240 fps phone camera; emulators can't.
- **First response in the touch-down frame** (press squash, click sound, light haptic), even when the rules resolve on later ticks.
- **Input System:** "Process Events in Dynamic Update" when the lowest latency matters (Input System manual › Timing).
- **Android frame queue:** with frame pacing off, a full display queue (buffer stuffing) adds a frame of latency; Swappy (Optimized Frame Pacing) removes it (Android's Frame Pacing pages; not re-verified). Decide OFP on a phone with latency and smoothness measured together (unity-proje-ayarlari.md: OFP also snaps the target to refresh-rate divisors and crashed on an emulator).
- **Audio:** Unity 2023.1+ plays through AAudio on Android 8.1+ (not re-verified). Measure before shrinking the DSP buffer: "Best Latency" crackled on some devices on the older path (UUM-3745). 1024 samples at 48 kHz ≈ 21 ms per buffer, and a service that schedules one buffer ahead doubles it.

## 2. UI motion
- Popups (settings, offers) open in 0.2-0.3 s ease-out (OutCubic, or OutBack ≤ 10% overshoot) with a 0.9 → 1 scale and fade; result panels appear at once or within 0.15 s and move their content instead (arayuz-kalitesi.md §3 Win); close 0.12-0.2 s ease-in; press 0.08-0.12 s; screen transitions ≤ 0.4 s.
- For reference, Material 3's tokens: short 50-200 ms, medium 250-400, long 450-600; entering curve emphasized-decelerate cubic-bezier(0.05, 0.7, 0.1, 1), leaving emphasized-accelerate (0.3, 0, 0.8, 0.15).
- UI tweens run on unscaled time (pause sets timeScale 0); a fixed-step video capture doesn't move them (store-listing-optimization.md › Preview video). Every celebration is skippable by a tap. Idle motion stays subtle (≤ 3% scale, ≥ 1.5 s period).
- **Interruptible, never blocking:** a tap or back ends a UI tween at once (`Complete()`), input stays live during decorative motion, and the new state is set when the change starts, never in the tween's completion callback: a killed or skipped tween must not leave a half-state.
- **More juice is not better:** big feedback for success, soft for failure; vary sounds. Haptic embellishment beat none, but more did no better than less (Singhal & Schneider, CHI 2021: 38 players, six Breakout variants; figures not re-verified).

## 3. Reduce motion
- A "Reduce motion / Hareketi azalt" switch in every game; its first-launch default follows the OS, re-read on `OnApplicationFocus(true)` until the player touches the switch. Unity 6000.3 has no API for it (`AccessibilitySettings` has only font scale, bold text, captions).
- iOS: a small `Assets/Plugins/iOS/*.mm` calling `UIAccessibilityIsReduceMotionEnabled()` (Unity copies it into the Xcode project even when we export on Windows; Apple's Apple.Accessibility plugin needs a Mac build step, so not for us: app-store-game-center.md).
- Android: `ValueAnimator.areAnimatorsEnabled()` on API 26+ (Android's "Remove animations" sets the animator scale to 0; battery saver can too), `Settings.Global` `animator_duration_scale == 0` below that (reader below).
- When on: fades instead of scale or slide, no shake, parallax, spinning or confetti storms, idle loops stop, counters jump to the final value. Never more than 3 flashes in any second (WCAG 2.3.2).
  ```csharp
  public static bool OsReduceMotion() {   // API names verified 2026-10-18; adapt, then test on a device
  #if UNITY_ANDROID && !UNITY_EDITOR
      int sdk; using (var v = new AndroidJavaClass("android.os.Build$VERSION")) sdk = v.GetStatic<int>("SDK_INT");
      if (sdk >= 26) { using var va = new AndroidJavaClass("android.animation.ValueAnimator"); return !va.CallStatic<bool>("areAnimatorsEnabled"); }
      using var cr = UnityEngine.Android.AndroidApplication.currentActivity.Call<AndroidJavaObject>("getContentResolver");
      using var g = new AndroidJavaClass("android.provider.Settings$Global");
      return g.CallStatic<float>("getFloat", cr, "animator_duration_scale", 1f) == 0f;
  #elif UNITY_IOS && !UNITY_EDITOR
      return _SG_IsReduceMotionEnabled();   // [DllImport("__Internal")] static extern bool _SG_IsReduceMotionEnabled();
  #else
      return false;
  #endif
  }
  // Assets/Plugins/iOS/SGMotion.mm: #import <UIKit/UIKit.h>
  //   extern "C" bool _SG_IsReduceMotionEnabled(void) { return UIAccessibilityIsReduceMotionEnabled(); }
  ```

## 4. Feedback and haptics
- Every tap answers in the same frame and with a sound; key moments add a haptic (light on a tap result, success on a win, warning on a fail) behind its own switch; sounds share loudness; the UI click ≤ 0.1 s.
- Haptics are optional (own switch), short, tied to discrete events and rate-limited; the game works without them.
- **iOS:** `UIImpactFeedbackGenerator`, `UINotificationFeedbackGenerator` (success, warning, error) and `UISelectionFeedbackGenerator` through a small .mm, each only for its documented meaning; `prepare()` ahead of the moment; never the same pattern for opposite outcomes (a failure's haptic never ends a won level).
- **Android:** `View.performHapticFeedback(HapticFeedbackConstants.*)` on the UI thread (no VIBRATE permission, follows the system touch-feedback setting; CONFIRM and REJECT need API 30, fall back to CONTEXT_CLICK or VIRTUAL_KEY); `AndroidApplication.InvokeOnUIThread` reaches the UI thread without a Java file (measure its cost). Clear, not buzzy: no haptic beats a buzzy one, a key tick lasts ~10-20 ms; no legacy `createOneShot`/`vibrate(long)`.
- Never `Handheld.Vibrate()`: a long buzz of OS-chosen length that adds the VIBRATE permission. Nice Vibrations is no longer free (part of the paid Feel) and its open-source repo is archived: write the small bridge above.

## 5. Screen shake
- One trauma value 0-1 that decays on its own (e.g. 0.5 a second); offset = smooth 1D noise × trauma² × cap (squared feels better than linear; separate noise offsets for translation and rotation).
- Add it to the rendered camera only and undo it next frame: game logic never sees the shake. Off under reduce motion.
