# 👑 King James Empire — Build Command Center

Live dashboard for tracking all 6 KJLE empire products.

## Setup (5 minutes)

### 1. Create the GitHub repo
- Open GitHub Desktop
- Click **File → New repository**
- Name: `empire-dashboard`
- Local path: wherever you want (Desktop is fine)
- Click **Create Repository**

### 2. Add the files
Copy both files into the new repo folder:
- `empire-command-center.html`
- `empire-state.json`

In GitHub Desktop you'll see both files appear. Commit message: `Initial empire dashboard` → click **Commit to main** → **Push origin**.

### 3. Enable GitHub Pages
- Go to github.com → your `empire-dashboard` repo
- Click **Settings** tab
- Left sidebar: click **Pages**
- Under "Branch" select `main` → folder `/root` → click **Save**
- Wait ~60 seconds. Your URL will be: `https://jharriGH.github.io/empire-dashboard/empire-command-center.html`

Bookmark that URL. Done.

---

## Updating the dashboard

**Option A — Upload MDs to Claude (recommended)**
1. Come back to this chat
2. Upload your updated build card MDs
3. Claude reads them and gives you a fresh `empire-state.json`
4. Copy the JSON into your local file
5. GitHub Desktop: commit + push
6. Refresh browser — done in ~2 minutes

**Option B — Edit empire-state.json directly**
Open `empire-state.json` in VS Code or any text editor.
The structure is straightforward — find the project and update:
- `pct` — completion percentage (0-100)
- `statusLabel` — display text
- `status` — one of: live, prelaunch, testing, building, active
- `nextActions` — array, first item shows on card
- `phases` — set `s` to: complete, active, punch, pending
- `bugs` — array of strings, empty array = clean
- `prelaunch` — checklist items for Pre-Launch tab

Commit + push → refresh browser.

---

## Files

| File | Purpose |
|---|---|
| `empire-command-center.html` | The dashboard — never needs to change |
| `empire-state.json` | All the data — this is what you update |
| `README.md` | This file |

The HTML fetches `empire-state.json` on every page load. You only ever edit the JSON.

---

## Local preview (optional)

If you want to preview before pushing:
```
cd empire-dashboard
npx serve .
```
Then open `http://localhost:3000/empire-command-center.html`

(The dashboard uses `fetch()` so it won't work if you just double-click the HTML file locally — it needs a server. GitHub Pages handles this automatically.)
