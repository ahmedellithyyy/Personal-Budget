# Ledger — Personal Finance

A working implementation of the **Ledger** design (`Ledger.dc.html`) from the
"Personal Finance App Design" Claude Design project. It's a single, portable
`index.html` — a personal-finance iOS app with four screens, live charts,
multi-currency display, Excel export, and local persistence.

## Run it locally

```bash
cd Ledger && python3 -m http.server 8817
```

Then visit http://localhost:8817/index.html. It's sized for a phone (402×874),
so a narrow window looks best.

## Put it on your phone

This is a web app, so it installs via **Add to Home Screen** — no App Store.
It becomes an icon that opens full-screen, and (thanks to the bundled service
worker) works offline after the first load.

**Upload the whole `Ledger` folder** (all six files — `index.html`,
`manifest.webmanifest`, `sw.js`, and the three `icon-*.png`) to any HTTPS host.
Two easy options:

**A. Netlify Drop — fastest, no setup**
1. Open https://app.netlify.com/drop on your computer.
2. Drag the `Ledger` folder onto the page. It returns an `https://…netlify.app` URL.
3. Open that URL on your phone → install (below).

**B. GitHub Pages — permanent, on your account**
1. Create a repo, add the six files (keep them at the repo root or in `/docs`).
2. Settings → Pages → deploy from your branch. You get an `https://<you>.github.io/<repo>/` URL.

**Install on the phone**
- **iPhone (Safari):** open the URL → Share → **Add to Home Screen** → Add.
- **Android (Chrome):** open the URL → ⋮ menu → **Install app** / Add to Home screen.

> Note: the app faithfully reproduces the design's iPhone *frame* (bezel,
> notch, fake status bar). On a real phone that shows as a framed card, not an
> edge-to-edge screen. If you'd prefer it fill the whole screen, ask for the
> "full-bleed" build and I'll drop the frame for phone use.

Your data lives in the browser on that device (localStorage). Requires internet
for the very first load; offline after that.

## What's inside

- **Dashboard** — "left this month", overspend warning, month-over-month
  bar chart (per-month / cumulative), budget-vs-actual breakdown, a
  "where the money went" donut, and recent transactions.
- **Budget** — plan per month, roll a previous month's plan forward, income /
  expense / savings groups, add & edit lines.
- **Activity** — searchable, filterable ledger grouped by date with running
  balances and swipe-to-delete.
- **Portfolio** — net worth, allocation donut by asset class, holdings with ROI.
- **Add / edit sheet** — record transactions, budget lines, and holdings
  (units × price for stocks/ETFs/crypto).
- **Currency** — display every figure in SAR / USD / GBP / EUR / AED.
- **Excel export** — download the month as a multi-sheet `.xlsx`.

## How it's built

The app is the design comp rendered by its own runtime, bundled into one file:

- The **template + component logic** are exactly as authored in the design comp
  (`Ledger.dc.html`) — no fidelity was lost in translation.
- `dc-runtime` (`support.js`) interprets the template and auto-loads React.
- The **iOS device frame** (`ios-frame.jsx`) is inlined as `window.IOSDevice`.
- The **Classical design system** tokens/components (`styles.css`) are inlined.

### Added on implementation: persistence

The design seeds sample data in memory. This build adds `localStorage`
persistence (key `ledger.v1`) so your budgets, transactions, holdings, and
chosen currency survive reloads. Clear it to return to the sample data:

```js
localStorage.removeItem('ledger.v1')
```
