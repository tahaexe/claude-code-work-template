---
paths:
  - "Assets/**/Tests/**"
---
# Unity test rules
<!-- unity add-on v1.54 · paths fitted to the project at install -->

- **When:** only in the pre-release test stage (`docs/ai/BAKIM.md`; handbook `yayin-oncesi-test-listesi.md`): every existing suite once. Never per step or at plan closure; while developing the error check is the verification. Existing tests are never deleted.
- **Location:** tests live under `Assets/` (Unity compiles only `Assets/` and `Packages/`), e.g. `Assets/Tests/EditMode/` and `Assets/Tests/PlayMode/`, each with its own test `.asmdef`. The EditMode test assembly includes only the Editor platform; the tested game code must also be in an `.asmdef`.
- **Prerequisite:** without `com.unity.test-framework` in `Packages/manifest.json` tests don't run or even hang. Count the result as "not verified" and propose adding the package.
- **Running:** via the Commands table, with a timeout: editor open → Pipeline's `run_tests`; closed → `bash docs/ai/araclar/testler.sh EditMode|PlayMode [filter]` (`-runTests` with its own log; never `unity test`: no log option, its editor writes the shared `Editor.log` the user's own editor uses). Confirm compiling has finished first (`unity recompile` waits for it); a test started mid-compile can hang. A timeout or a test that never ran is not "passed".
- **Result:** read the runner's exit code first (Unity's own; Test Framework 1.6 source, the docs define none): 0 no test failed · 2 tests failed (real failure) · 3 run error (e.g. compile errors) · 4 test platform not found · 124 timeout · other: the editor failed (batchmode exits 1). Passed = 0 with a total above 0 (no test ran also exits 0); every other result but 2 is "not verified": fix the environment, filter or compile, don't touch the test code. Don't read the whole report file; the runner prints the totals and failed tests.
- **EditMode / PlayMode:** pure logic in EditMode (fast); scenes, physics, coroutines or time in PlayMode.
- **Name:** `System_Scenario_ExpectedResult` (e.g. `Health_TakeDamageWithArmor_ReducesDamage`).
- **Structure:** clear Arrange / Act / Assert sections; exact assertions (`Assert.AreEqual(75, health.Current)`, not a loose "less than 100").
- **Independence:** unit tests don't depend on files, network, real time or shared mutable state; replace external dependencies with fakes; tests are fast and deterministic.
- **Data and cleanup:** test data inside the test or a separate fixture. PlayMode and integration tests destroy what they create in `TearDown`.
- **Performance tests:** state the acceptance threshold explicitly and fail when it is exceeded.
- **Red in the stage:** a game bug is fixed before the release; a stale or flaky test is updated, or disabled (`[Ignore("reason")]`) with a line in `docs/ai/hafiza/teknik-borc.md`; never loosened to hide a bug (`docs/ai/BAKIM.md`).
- **New tests:** only in the pre-release test stage, where a bug would cost players or money: save and relaunch (older save files too), purchases, ads, rewards and time (an injected clock), every level through the real controller (solver or bot), ad and navigation flows. A test for a fixed bug is **seen failing without the fix first** (revert it locally), then passes with it. A test never seen failing isn't known to test anything.
