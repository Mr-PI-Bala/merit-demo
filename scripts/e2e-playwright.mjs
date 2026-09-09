#!/usr/bin/env node
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const serveRoot = process.env.MERIT_E2E_ROOT
  ? path.resolve(root, process.env.MERIT_E2E_ROOT)
  : path.join(root, 'dist');
const sync = JSON.parse(fs.readFileSync(path.join(root, 'cfg/merit-sync.json'), 'utf8').replace(/^\uFEFF/, ''));
const consumerId = sync.consumer_id;
const evidenceDir = path.join(root, 'merit-demo docs', 'evidence');
const failures = [];
const routes = [
  { path: '/', label: 'home' },
  { path: '/portal/', label: 'portal' },
  { path: '/portal/ama/', label: 'portal-ama' },
  { path: '/portal/journal/', label: 'portal-journal' },
  { path: '/portal/subs/', label: 'portal-subs' },
  { path: '/play/', label: 'play' },
  { path: '/journal/', label: 'journal' },
  { path: '/ama/', label: 'ama' },
  { path: '/admin/', label: 'admin' },
  { path: '/diag/manifest.json', label: 'diag-manifest' },
];

function contentType(file) {
  if (file.endsWith('.html')) return 'text/html; charset=utf-8';
  if (file.endsWith('.css')) return 'text/css; charset=utf-8';
  if (file.endsWith('.js')) return 'text/javascript; charset=utf-8';
  if (file.endsWith('.json')) return 'application/json; charset=utf-8';
  return 'application/octet-stream';
}

function resolveRoute(urlPath) {
  const clean = decodeURIComponent(urlPath.split('?')[0]).replace(/^\/+/, '');
  const candidates = [];
  if (!clean) candidates.push('portal/index.html', 'index.html');
  else if (clean.endsWith('/')) candidates.push(`${clean}index.html`);
  else candidates.push(clean, `${clean}/index.html`);
  for (const rel of candidates) {
    const full = path.join(serveRoot, rel);
    if (full.startsWith(serveRoot) && fs.existsSync(full) && fs.statSync(full).isFile()) return full;
  }
  return null;
}

function startServer() {
  const server = http.createServer((req, res) => {
    const file = resolveRoute(req.url || '/');
    if (!file) {
      res.writeHead(404, { 'content-type': 'text/plain' });
      res.end('not found');
      return;
    }
    res.writeHead(200, { 'content-type': contentType(file) });
    fs.createReadStream(file).pipe(res);
  });
  return new Promise((resolve) => {
    server.listen(0, '127.0.0.1', () => resolve(server));
  });
}

async function fetchCheck(base) {
  for (const route of routes) {
    try {
      const res = await fetch(`${base}${route.path}`, { signal: AbortSignal.timeout(10000) });
      if (!res.ok) failures.push(`${route.label}: HTTP ${res.status}`);
      else console.log(`OK route ${route.path}`);
    } catch (error) {
      failures.push(`${route.label}: ${error.message}`);
    }
  }
}

async function browserCheck(base) {
  let chromium;
  try {
    ({ chromium } = await import('playwright'));
  } catch (error) {
    console.log(`SKIP Playwright screenshots: ${error.message}`);
    return;
  }

  fs.mkdirSync(evidenceDir, { recursive: true });
  const browser = await chromium.launch({
    executablePath: process.env.PLAYWRIGHT_EXECUTABLE_PATH || undefined,
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
  for (const route of routes.filter((r) => !r.path.endsWith('.json'))) {
    await page.goto(`${base}${route.path}`, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(evidenceDir, `${route.label}-desktop.png`), fullPage: true });
    console.log(`OK screenshot ${route.label}-desktop.png`);
  }
  await page.goto(`${base}/play/`, { waitUntil: 'networkidle' });
  const hello = page.locator('#meritutils-hello-status');
  if ((await hello.getAttribute('data-provider-ready')) !== 'true') {
    failures.push('Hello World: hosted merit_workbench package did not initialize');
  } else {
    console.log('OK Hello World hosted meritutils package');
  }
  const runtimeState = await hello.getAttribute('data-runtime-state');
  if (runtimeState !== 'hosted-ready') {
    failures.push(`Hosted Ready: expected data-runtime-state=hosted-ready, got ${runtimeState}`);
  } else {
    console.log('OK Hosted Ready runtime state');
  }
  const mounted = page.locator('[data-workbench-mounted="true"], .merit-workbench-root');
  if ((await mounted.count()) < 1) {
    failures.push('Workbench mount: no mounted workbench root found');
  } else {
    console.log('OK workbench mounted');
  }
  if ((await page.locator('text=Register free').count()) < 1) {
    failures.push('Play: Register free link missing');
  } else {
    console.log('OK Register free present');
  }
  await page.goto(`${base}/portal/subs/`, { waitUntil: 'networkidle' });
  const registerHref = await page.locator('#register-link').getAttribute('href');
  if (!registerHref || !registerHref.includes(`/store/${consumerId}/register`)) {
    failures.push(`Portal subscription CTA: expected /store/${consumerId}/register, got ${registerHref || '(missing)'}`);
  } else {
    console.log('OK portal subscription CTA uses consumer registration path');
  }
  await page.setViewportSize({ width: 390, height: 844 });
  for (const route of ['/portal/', '/play/', '/journal/', '/ama/']) {
    const label = route.replaceAll('/', '') || 'home';
    await page.goto(`${base}${route}`, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(evidenceDir, `${label}-mobile.png`), fullPage: true });
    console.log(`OK screenshot ${label}-mobile.png`);
  }
  const localPage = await browser.newPage({ viewport: { width: 1024, height: 900 } });
  await localPage.route(/https:\/\/merit-prod\.vercel\.app\/api\//, (route) => route.abort());
  await localPage.goto(`${base}/journal/`, { waitUntil: 'networkidle' });
  await localPage.locator('#journal-status[data-state="local"]').waitFor({ timeout: 10000 });
  await localPage.locator('#entry').fill('A local-first journal check.');
  await localPage.locator('#save').click();
  await localPage.getByText('A local-first journal check.').waitFor({ timeout: 10000 });
  if ((await localPage.locator('#list').textContent()).includes('A local-first journal check.') !== true) {
    failures.push('Journal local fallback: saved text did not render after provider outage');
  } else {
    console.log('OK Journal local fallback save');
  }
  await localPage.goto(`${base}/ama/`, { waitUntil: 'networkidle' });
  await localPage.locator('#ama-status.local').waitFor({ timeout: 10000 });
  await localPage.locator('#question').fill('A local-first AMA check.');
  await localPage.locator('#ask').click();
  await localPage.getByText('A local-first AMA check.').waitFor({ timeout: 10000 });
  const localAmaText = await localPage.locator('#board').textContent();
  if (localAmaText.includes('A local-first AMA check.') !== true) {
    failures.push('AMA local fallback: saved question did not render after provider outage');
  } else {
    console.log('OK AMA local fallback post');
  }
  await localPage.close();
  await browser.close();
}

async function providerCheck() {
  const checks = [
    ['https://merit-prod.vercel.app/api/health', 'merit-prod health', true],
    ['https://merit-prod.vercel.app/pkg/meritutils/registry.json', 'meritutils registry', true],
    ['https://merit-prod.vercel.app/api/meritsubs/api/v1/health', 'meritsubs health', true],
    [sync.meritstore_register_url, `${consumerId} hosted register path`, true],
  ];
  for (const [url, label, required] of checks) {
    try {
      const res = await fetch(url, { redirect: 'manual', signal: AbortSignal.timeout(30000) });
      if (label.includes('hosted register path')) {
        const expected = new URL(url).pathname;
        const location = res.headers.get('location');
        if (res.status >= 300 && res.status < 400) {
          failures.push(`${label}: redirected to ${location || '(missing location)'}; expected provider to serve ${expected}`);
        } else if (!res.ok) {
          failures.push(`${label}: HTTP ${res.status}; expected provider to serve ${expected}`);
        } else {
          console.log(`OK provider ${label}`);
        }
      } else if (!res.ok && required) failures.push(`${label}: HTTP ${res.status}`);
      else if (!res.ok) console.log(`WARN provider ${label}: HTTP ${res.status}`);
      else console.log(`OK provider ${label}`);
    } catch (error) {
      if (required) failures.push(`${label}: ${error.message}`);
      else console.log(`WARN provider ${label}: ${error.message}`);
    }
  }
}

console.log(`=== ${consumerId} Playwright e2e ===`);
const server = await startServer();
const address = server.address();
const base = `http://127.0.0.1:${address.port}`;
try {
  await fetchCheck(base);
  await browserCheck(base);
  await providerCheck();
} finally {
  await new Promise((resolve) => server.close(resolve));
}

if (failures.length) {
  console.error(`E2E FAILED:\n${failures.map((f) => `  - ${f}`).join('\n')}`);
  process.exit(1);
}

console.log(`E2E OK: ${consumerId} routes, provider links, Hello World, screenshots`);
