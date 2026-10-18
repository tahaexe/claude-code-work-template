---
title: "Game feel: UI motion, reduce motion, feedback and haptics"
condition: "Unity game project with player-facing UI or touch input (every studio game; haptics for Android and iOS)."
read_when: "Feel or juice work: popup and celebration timings, tap feedback, vibration; adding the reduce-motion switch; choosing a haptics library."
requires: "—"
source: "Android Developers: ValueAnimator, Settings.Global, haptic feedback guide (HapticFeedbackConstants) · Apple HIG (motion, Reduce Motion, playing haptics) · Material 3 motion tokens · WCAG 2.2 2.3.2 · Unity 6000.3 scripting reference (AccessibilitySettings, Handheld.Vibrate) · the studio's UI market review and unity-uzmani review, 2026-10-18"
tech: "Unity 6000.3; Android View.performHapticFeedback, iOS UIFeedbackGenerator"
added: "2026-10-18 · template 1.52 · the motion and feedback rules of the studio's UI quality guide (market research for the session manager)"
---
# Game feel

## UI motion
- Popups (settings, offers) open in 0.2-0.3 s ease-out (OutCubic, or OutBack ≤ 10% overshoot) with a 0.9 → 1 scale and fade; result panels appear at once or within 0.15 s and move their content instead (arayuz-kalitesi.md §3 Win); close 0.12-0.2 s ease-in; press 0.08-0.12 s; screen transitions ≤ 0.4 s.
- For reference, Material 3's tokens: short 50-200 ms, medium 250-400, long 450-600; entering curve emphasized-decelerate cubic-bezier(0.05, 0.7, 0.1, 1), leaving emphasized-accelerate (0.3, 0, 0.8, 0.15).
- UI tweens run on unscaled time (pause sets timeScale 0). Every celebration is skippable by a tap. Idle motion stays subtle (≤ 3% scale, ≥ 1.5 s period).

## Reduce motion
- A "Reduce motion / Hareketi azalt" switch in every game; its first-launch default follows the OS, re-read on `OnApplicationFocus(true)` until the player touches the switch. Unity 6000.3 has no API for it (`AccessibilitySettings` has only font scale, bold text, captions).
- iOS: a small `Assets/Plugins/iOS/*.mm` calling `UIAccessibilityIsReduceMotionEnabled()` (Unity copies it into the Xcode project even when we export on Windows; Apple's Apple.Accessibility plugin needs a Mac build step, so not for us).
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

## Feedback and haptics
- Every tap answers in the same frame and with a sound; key moments add a haptic (light on a tap result, success on a win, warning on a fail) behind its own switch; sounds share loudness; the UI click ≤ 0.1 s.
- **Haptics API:** iOS `UIImpactFeedbackGenerator` / `UINotificationFeedbackGenerator` (success, warning, error) through a small .mm; Android `View.performHapticFeedback(HapticFeedbackConstants.*)` on the UI thread (no VIBRATE permission, follows the system touch-feedback setting; CONFIRM and REJECT need API 30, fall back to CONTEXT_CLICK or VIRTUAL_KEY).
- Never `Handheld.Vibrate()`: a long buzz of OS-chosen length that adds the VIBRATE permission. Nice Vibrations is no longer free (part of Feel) and its open-source repo is archived.
