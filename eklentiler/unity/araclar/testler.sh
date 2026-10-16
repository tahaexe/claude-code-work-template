#!/usr/bin/env bash
# unity add-on v1.49 · from the template; "şablonu güncelle" refreshes it and keeps project-specific lines
# Unity tests with this project's editor closed (one editor per project): the project's own Unity version, -batchmode
# -runTests (compiles first, quits by itself), its own -logFile. Never `unity test`: it has no log option, so its editor
# writes the shared %LOCALAPPDATA%\Unity\Editor\Editor.log that the user's own editor uses.
#   bash docs/ai/araclar/testler.sh EditMode|PlayMode [filter]   # filter: Unity's -testFilter (names joined by ';', or a regex)
# Writes Logs/claude/<mode>.xml and Logs/claude/editor-<mode>.log; prints the totals and failed tests, else the log's errors.
# Exit: Unity's (Test Framework 1.6: 0 no failures, also when no test ran; 2 tests failed; 3 run error, e.g. compile errors;
# 4 platform not found; 1 batchmode failure); 124 = timeout (TEST_TIMEOUT, default 1800 s). Editor elsewhere: UNITY_EDITOR_EXE.
# One asset import worker, none on standby (IMPORT_WORKERS, default 1): each worker of the default pool holds ~0.9 GB
# (handbook unity-cli-saha-notlari.md › Headless editor). First open (empty Library/) or a big import: raise IMPORT_WORKERS.
P=$(cd "$(dirname "$0")/../../.." && pwd)
W=$(cygpath -m "$P")
mode=$1
case "$mode" in EditMode|PlayMode) ;; *) sed -n 3,11p "$0"; exit 64;; esac
v=$(sed -n 's/^m_EditorVersion: //p' "$P/ProjectSettings/ProjectVersion.txt" | tr -d '\r')
E="${UNITY_EDITOR_EXE:-/c/Program Files/Unity/Hub/Editor/$v/Editor/Unity.exe}"
[ -f "$E" ] || { echo "no editor at $E (project version $v)"; exit 1; }
m=$(echo "$mode" | tr 'A-Z' 'a-z')
R="Logs/claude/$m.xml"
L="Logs/claude/editor-$m.log"
mkdir -p "$P/Logs/claude"
rm -f "$P/$R"
args=(-batchmode -runTests -projectPath "$W" -testPlatform "$mode" -testResults "$W/$R" -logFile "$W/$L"
      -desiredWorkerCount "${IMPORT_WORKERS:-1}" -standbyWorkerCount 0)
[ -n "$2" ] && args+=(-testFilter "$2")
timeout "${TEST_TIMEOUT:-1800}" "$E" "${args[@]}"
rc=$?
[ $rc -eq 124 ] && echo "timed out after ${TEST_TIMEOUT:-1800} s"
if [ -f "$P/$R" ]; then
  python -I - "$W/$R" "$rc" <<'PY'
import sys, xml.etree.ElementTree as ET
r = ET.parse(sys.argv[1]).getroot()
print(f"exit {sys.argv[2]}: total {r.get('total')}, passed {r.get('passed')}, failed {r.get('failed')}, skipped {r.get('skipped')}")
if r.get('total') == '0':
    print('  no test ran: not a pass (filter?)')
for t in r.iter('test-case'):
    if t.get('result') == 'Failed':
        msg = t.find('failure/message')
        print('  FAILED', t.get('fullname'), '-', ' '.join((msg.text or '').split())[:300] if msg is not None else '')
PY
else
  echo "exit $rc: no results; from the log ($L):"
  grep -m 20 "error CS\|another Unity instance\|Aborting batchmode\|Exiting with code\|Exiting batchmode" "$P/$L"
fi
exit $rc
