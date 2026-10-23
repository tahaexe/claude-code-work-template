#!/usr/bin/env node
// Capture a seek(t) page frame by frame in the installed Google Chrome, headless, over the DevTools
// protocol: Node 22+ has WebSocket and fetch built in, so no npm package and no Playwright
// (template 1.60, from a studio trial of 2026-10-22: 45 frames at 1080x1920 in 11-13 s, ~750 MB peak).
//
//   node kare-yakala.mjs <page.html> <out folder> [--frames 45] [--fps 30] [--size 1080x1920] [--chrome <path>]
//   node kare-yakala.mjs --dene      self-test: a tiny page captured twice in a temporary folder (removed after)
//
// The page defines window.seek(t) (it may be async) that draws the frame at t seconds from t alone: no CSS
// transitions, timers or state carried between frames. Frame n is captured after seek(n / fps) resolves;
// frames go to <out>/0000.png, 0001.png … with transparency where the page has none of its own background.
// The browser: --chrome, else the CHROME environment variable, else Chrome's usual install path.
// Prints one JSON line (frames, size, timings, folder). Exit: 0 done · 1 capture failed · 2 usage error.
import { spawn } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const sleep = (ms) => new Promise((done) => setTimeout(done, ms));

function findChrome(given) {
  if (given) return given;
  if (process.env.CHROME) return process.env.CHROME;
  const places = [];
  if (process.platform === "win32") {
    for (const base of [process.env.PROGRAMFILES, process.env["PROGRAMFILES(X86)"], process.env.LOCALAPPDATA]) {
      if (base) places.push(join(base, "Google", "Chrome", "Application", "chrome.exe"));
    }
  } else if (process.platform === "darwin") {
    places.push("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome");
  } else {
    places.push("/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium", "/usr/bin/chromium-browser");
  }
  return places.find((place) => existsSync(place));
}

async function capture({ page, out, frames, fps, width, height, chromePath }) {
  if (typeof WebSocket !== "function" || typeof fetch !== "function") {
    throw new Error("Node 22 or newer is needed (built-in WebSocket and fetch)");
  }
  const chrome = findChrome(chromePath);
  if (!chrome || !existsSync(chrome)) throw new Error("Google Chrome not found: pass --chrome <path> or set CHROME");
  mkdirSync(out, { recursive: true });
  const profile = mkdtempSync(join(tmpdir(), "kare-yakala-"));
  const t0 = Date.now();
  const browser = spawn(chrome, ["--headless=new", "--remote-debugging-port=0", `--user-data-dir=${profile}`,
    "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "--force-device-scale-factor=1",
    "--mute-audio", "about:blank"], { stdio: "ignore" });
  let ws;
  try {
    let port;
    for (let i = 0; i < 150 && !port; i++) {
      try { port = readFileSync(join(profile, "DevToolsActivePort"), "utf8").split("\n")[0].trim(); } catch { await sleep(100); }
    }
    if (!port) throw new Error("Chrome didn't open its DevTools port within 15 s");
    let target;
    for (let i = 0; i < 100 && !target; i++) {
      try {
        const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
        target = list.find((item) => item.type === "page");
      } catch { /* not ready yet */ }
      if (!target) await sleep(100);
    }
    if (!target) throw new Error("no page in the headless Chrome");
    ws = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise((done, fail) => { ws.onopen = done; ws.onerror = () => fail(new Error("DevTools connection failed")); });
    let id = 0;
    const waiting = new Map();
    const events = new Set();
    ws.onmessage = (message) => {
      const data = JSON.parse(message.data);
      if (data.id && waiting.has(data.id)) {
        const call = waiting.get(data.id);
        waiting.delete(data.id);
        if (data.error) call.fail(new Error(`${call.method}: ${data.error.message}`)); else call.done(data.result);
      } else if (data.method) {
        events.add(data.method);
      }
    };
    const send = (method, params = {}) => new Promise((done, fail) => {
      const call = ++id;
      waiting.set(call, { method, done, fail });
      ws.send(JSON.stringify({ id: call, method, params }));
    });
    await send("Page.enable");
    await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: false });
    await send("Emulation.setDefaultBackgroundColorOverride", { color: { r: 0, g: 0, b: 0, a: 0 } });
    events.clear();
    await send("Page.navigate", { url: pathToFileURL(resolve(page)).href });
    for (let i = 0; i < 400 && !events.has("Page.loadEventFired"); i++) await sleep(50);
    const ready = await send("Runtime.evaluate", {
      expression: "document.fonts.ready.then(() => typeof window.seek)", awaitPromise: true, returnByValue: true });
    if (ready.result.value !== "function") throw new Error("the page defines no window.seek(t)");
    const tLoad = Date.now();
    for (let n = 0; n < frames; n++) {
      const step = await send("Runtime.evaluate", {
        expression: `Promise.resolve(window.seek(${n} / ${fps}))`, awaitPromise: true, returnByValue: true });
      if (step.exceptionDetails) {
        throw new Error(`seek failed at frame ${n}: ${JSON.stringify(step.exceptionDetails).slice(0, 300)}`);
      }
      const shot = await send("Page.captureScreenshot", { format: "png", fromSurface: true });
      writeFileSync(join(out, `${String(n).padStart(4, "0")}.png`), Buffer.from(shot.data, "base64"));
    }
    const tEnd = Date.now();
    try { await Promise.race([send("Browser.close"), sleep(2000)]); } catch { /* closing anyway */ }
    return { frames, fps, size: `${width}x${height}`, start_ms: tLoad - t0, capture_ms: tEnd - tLoad, out: resolve(out) };
  } finally {
    try { ws?.close(); } catch { /* already closed */ }
    await new Promise((done) => { if (browser.exitCode !== null) done(); else { browser.once("exit", done); setTimeout(done, 3000); } });
    if (browser.exitCode === null) browser.kill();
    for (let i = 0; i < 10; i++) {
      try { rmSync(profile, { recursive: true, force: true }); break; } catch { await sleep(300); }
    }
  }
}

async function dene(chromePath) {
  const folder = mkdtempSync(join(tmpdir(), "kare-yakala-dene-"));
  const checks = [];
  const report = (name, ok) => { checks.push(Boolean(ok)); console.log(`  ${ok ? "ok  " : "FAIL"} ${name}`); };
  try {
    const page = join(folder, "sayfa.html");
    writeFileSync(page, "<!doctype html><html><head><style>html,body{margin:0;background:transparent}</style></head>"
      + "<body><canvas id=c width=64 height=64></canvas><script>const g=document.getElementById('c').getContext('2d');"
      + "window.seek=async t=>{g.clearRect(0,0,64,64);g.fillStyle='#e33';g.fillRect(Math.round(t*120)%48,20,16,16);};"
      + "</script></body></html>");
    const one = await capture({ page, out: join(folder, "a"), frames: 3, fps: 10, width: 64, height: 64, chromePath });
    await capture({ page, out: join(folder, "b"), frames: 3, fps: 10, width: 64, height: 64, chromePath });
    const read = (run, n) => readFileSync(join(folder, run, `000${n}.png`));
    report("three frames written", [0, 1, 2].every((n) => existsSync(join(folder, "a", `000${n}.png`))));
    report("the same t gives the same pixels on a second run", [0, 1, 2].every((n) => read("a", n).equals(read("b", n))));
    report("frames at different t differ", !read("a", 0).equals(read("a", 1)) && !read("a", 1).equals(read("a", 2)));
    report("PNG with an alpha channel (colour type 6)", read("a", 0)[25] === 6);
    console.log(JSON.stringify(one));
  } catch (error) {
    report(`capture ran (${error.message})`, false);
  } finally {
    rmSync(folder, { recursive: true, force: true });
  }
  console.log(`dene: ${checks.filter(Boolean).length}/${checks.length} ok`);
  return checks.length && checks.every(Boolean) ? 0 : 1;
}

async function main() {
  const args = process.argv.slice(2);
  const options = { frames: 45, fps: 30, size: "1080x1920", chrome: undefined };
  const positional = [];
  let selfTest = false;
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--dene") selfTest = true;
    else if (["--frames", "--fps", "--size", "--chrome"].includes(arg)) options[arg.slice(2)] = args[++i];
    else if (arg.startsWith("--")) { console.error(`unknown option ${arg}`); return 2; }
    else positional.push(arg);
  }
  if (selfTest) return dene(options.chrome);
  const [page, out] = positional;
  const frames = Number(options.frames), fps = Number(options.fps);
  const size = /^(\d+)x(\d+)$/.exec(String(options.size));
  if (!page || !out || !existsSync(page) || !(frames > 0) || !(fps > 0) || !size) {
    console.error("usage: node kare-yakala.mjs <page.html> <out folder> [--frames 45] [--fps 30] [--size 1080x1920] [--chrome <path>]");
    return 2;
  }
  try {
    const result = await capture({ page, out, frames, fps, width: Number(size[1]), height: Number(size[2]), chromePath: options.chrome });
    console.log(JSON.stringify(result));
    return 0;
  } catch (error) {
    console.error(`capture failed: ${error.message}`);
    return 1;
  }
}

process.exitCode = await main();
