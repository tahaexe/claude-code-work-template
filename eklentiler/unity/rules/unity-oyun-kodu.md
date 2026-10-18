---
paths:
  - "Assets/**/*.cs"
---
# Unity C# and gameplay code rules
<!-- unity add-on v1.53 · paths fitted to the project at install; if the project follows a different but consistent convention, follow it -->

## Architecture
- Composition over deep MonoBehaviour inheritance; interfaces for shared behaviour (`IDamageable`, `IInteractable`).
- Separate data from behaviour: data in ScriptableObjects (items, abilities, settings, event channels), behaviour in MonoBehaviours.
- No hard-coded game values (damage, speed, durations…); they come from ScriptableObjects or config data.
- Systems talk via events (C# events, ScriptableObject event channels, UnityEvent); gameplay code never references UI code directly.
- No static singletons for game state; pass dependencies via the Inspector or explicit setup (follow the project's service locator or DI if it has one).
- **Services:** game-wide services (save, audio, input, ads, IAP, analytics, scene loading) are plain C# classes behind interfaces (`ISaveService`), created in one composition root (bootstrap scene or entry point) and handed to consumers (constructor, `Init(...)` or the project's locator/DI); gameplay code never `new`s them or reaches them through a static singleton. Default: a hand-written composition root, no package; a DI container (e.g. VContainer) only by plan, recorded in `hafiza/kararlar.md`.
- **SOLID:** one responsibility per class (no do-everything `GameManager`); dependencies point one way (gameplay → services, never services → gameplay or UI); extend with new classes or ScriptableObjects instead of growing switches; interfaces only where they pay off (services, several implementations, test fakes); hot paths may trade abstraction for speed.
- **Migrating old code:** one system per plan step: put the singleton behind an interface, register it at the composition root, move its call sites, then remove the static access; verify with tests and Play mode.
- State machines define states and transitions explicitly.
- Each system has a clear interface; logic is separate from presentation so it can be tested.
- Each code folder has its own `.asmdef`.
- DOTS/ECS may fit performance-critical systems with thousands of entities; justify it in the plan and record it in `hafiza/kararlar.md`.

## C# standards
- No `Find()`, `FindObjectOfType()`, `SendMessage()` in production code; inject references or use events.
- Cache component references in `Awake()`; no `GetComponent<>()` in `Update()`.
- Inspector fields are `[SerializeField] private`; no public fields. Use `[Header]` and `[Tooltip]`.
- Renaming a serialized field: add `[FormerlySerializedAs("oldName")]`, or scene and prefab values are lost.
- Every time-based calculation uses `Time.deltaTime` (`Time.fixedDeltaTime` in physics); frame-rate independent.
- Naming: public members `PascalCase`, private fields `_camelCase`, locals `camelCase`. Prefer `readonly` and `const`.
- Check destroyed Unity objects with `== null`; `is null` and `?.` bypass Unity's null check.

## Errors
- **No silent failures:** players lose progress and money to them. No empty `catch` and no catch that hides the failure behind a default value. A save that fails to read or parse keeps its file and backup (move it aside), never overwritten with defaults. IAP, ad and network failures are logged with context (operation, product or placement id, exception) and leave the player a way on (retry, close, a message), never a button that silently does nothing.
- `async void` only at event entry points (UI callbacks, Unity messages), with a try/catch inside; everything below returns `Awaitable` or `Task` and is awaited, so its exception reaches a handler.

## Memory and performance
- No allocations in hot paths (`Update`, physics callbacks): string concatenation, new lists, LINQ, boxing.
- `StringBuilder` for strings in loops; `NonAlloc` versions such as `Physics.RaycastNonAlloc`.
- Pool frequently created objects (`ObjectPool<T>`).
- No empty `Update()`; prefer events, coroutines or the Job System.
- Stop coroutines when their owner is destroyed; use `DontDestroyOnLoad` sparingly; set Script Execution Order for systems that depend on init order.
- Mark non-moving objects `static` (batching).
- Performance doubt: don't guess, measure in the Profiler (GC.Alloc column).

## Input
- New Input System and `.inputactions` assets; no legacy `Input.GetKey()` (if the project uses the legacy system, ask before switching).
- Keyboard+mouse, gamepad and (on mobile) touch together; `performed` / `canceled` callbacks instead of polling.
