## Netflix Ads Data — Advertiser Quick Start

This guide is for non‑technical advertisers. In a few clicks you’ll generate realistic sample campaigns and performance data you can explore like a spreadsheet.

```
You click  →  We generate  →  You analyze
     └────────── ads.db (single file database)
```

---

## 1) Install (2 simple options)

Option A — Quick (no new tools)

1) Make sure Python 3.10–3.12 is installed
2) Open a terminal in this folder
3) Run:

```bash
make init-db
# This creates a private environment, installs packages, and initializes ads.db
```

Option B — Poetry (recommended for teams)

1) Install Poetry (once): https://python-poetry.org/docs/#installation
2) Install and initialize:

```bash
poetry install
poetry run python cli.py init-db
# Optional: source ./activate_env.sh to activate the virtualenv in your shell
```

Result in both cases: a fresh local SQLite database file `ads.db` in this folder.

ASCII map of where things land:

```
[Repo Folder]
 ├── cli.py                 # Commands you run
 ├── cli_templates/         # Ready-made profiles & examples
 ├── run_all.sh             # One-click sample data
 └── ads.db                 # Your data (auto-created)
```

---

## 2) Create Aggressive vs Defensive Profiles

Profiles are ready-made campaign setups. You can think of them as “templates with knobs.”

```
                Strategy Map
   ┌───────────────────────────────┐
   │  Gain Market Share (Aggressive)│  →  higher CPM, broad reach, growth
   └───────────────────────────────┘
                 ▲
                 │
                 ▼
   ┌───────────────────────────────┐
   │  Defend Market Share (Defensive)│ →  protect base, efficiency, retention
   └───────────────────────────────┘
```

Quick start: create all examples and profiles

```bash
bash run_all.sh
# Creates 3 complete examples + 4 profiles and fills ads.db with performance data
```

Create specific aggressive profiles (Gain Market Share)

```bash
# High-CPM TV awareness (luxury/expansion)
python cli.py create-profile --name high_cpm_tv_awareness

# Mobile-first consideration at scale
python cli.py create-profile --name mobile_consideration

# Interactive conversion (apps, signups)
python cli.py create-profile --name conversion_interactive
```

Create specific defensive profiles (Defend Market Share)

```bash
# Established brand awareness maintenance
python cli.py create-profile --name high_cpm_tv_awareness

# Customer retention / keep top-of-mind
python cli.py create-profile --name mobile_consideration

# Loyalty or upsell conversions
python cli.py create-profile --name conversion_interactive

# Premium service with precise, multi-device targeting
python cli.py create-profile --name multi_device_advanced
```

Note: “Aggressive vs Defensive” is a strategy lens; under the hood the engine uses the same underlying profiles. You pick which mindset you’re testing.

---

## 3) What A Profile Represents

Each profile bundles sensible defaults so your campaign “just works.”

```
[Advertiser]
    ↓
[Campaign] — objective, budget, target CPM
    ↓
[Line Items] — device & content targeting, pacing, bids
    ↓
[Creatives] — durations, placements, interactive options
    ↓
[Hourly Performance] — impressions, clicks, spend, CTR, CPM…
```

Where they live:

- Profiles file: `cli_templates/profiles/campaign-profiles.yml`
- Examples file: `cli_templates/examples/netflix-ads-examples.yml`

What the key knobs do:

- Target CPM: raises/lowers price pressure and delivery goals
- Budget: how much firepower to spend over the flight
- Device/Content targeting: where your ads appear (TV, Mobile, Desktop; Drama, Comedy, etc.)
- Creative duration/placement: 15s/30s, pre‑roll/mid‑roll
- Performance settings: how much hourly data to generate and with what seed

---

## 4) Modify A Profile (Simple & Safe)

The simplest way to adjust is to edit the YAML profile, then run the command again.

Open `cli_templates/profiles/campaign-profiles.yml` and find the block you want (for example `high_cpm_tv_awareness`). Tweak values like CPM, budget, targeting, and creative duration.

Example edits (conceptual):

```yaml
profiles:
  high_cpm_tv_awareness:
    description: "TV awareness with premium targeting"
    test_values:
      campaign:
        target_cpm: 22.00        # was 20.00
        budget: 200000.00        # was 150000.00
      line_items:
        - targeting_json: '{"DEVICE": ["TV"], "CONTENT_GENRE": ["DRAMA"], "GEO_COUNTRY": ["US"]}'
          bid_cpm: 22.00
      creatives:
        - duration_seconds: 30   # 15 → 30 seconds
```

Then re-run:

```bash
python cli.py create-profile --name high_cpm_tv_awareness
```

Tips:

- Use `--seed 42` to reproduce the same randomization: `python cli.py create-profile --name mobile_consideration --seed 42`
- Keep numbers realistic (e.g., CPMs between 8–30 USD, budgets in the tens of thousands+)
- If you’re unsure, change one knob at a time and re-run

Advanced note: an inline override flag exists (`--test-fields key=value`), but deeper/nested changes are easier and clearer by editing the YAML as shown above.

---

## 5) See Your Results

Everything you create is saved in `ads.db` in this folder.

Ways to explore:

- In VS Code/Cursor: right‑click `ads.db` → “Open with SQLite viewer”
- Or any SQLite app; it’s a standard file

Quick checks (optional):

```sql
-- How many campaigns did I create?
SELECT COUNT(*) FROM campaigns;

-- What were their objectives and CPMs?
SELECT name, objective, target_cpm FROM campaigns ORDER BY created_at DESC;
```

ASCII snapshot of the flow:

```
create-profile  →  ads.db tables filled  →  explore
       └── advertisers
       └── campaigns
       └── line_items
       └── creatives
       └── performance (hourly)
```

---

## 6) Handy Cheatsheet

```bash
# One-and-done: everything
bash run_all.sh

# Fresh database
python cli.py init-db

# Aggressive set (gain share)
python cli.py create-profile --name high_cpm_tv_awareness
python cli.py create-profile --name mobile_consideration
python cli.py create-profile --name conversion_interactive

# Defensive set (defend share)
python cli.py create-profile --name high_cpm_tv_awareness
python cli.py create-profile --name mobile_consideration
python cli.py create-profile --name multi_device_advanced
```

Troubleshooting:

- “Command not found”: ensure you’re in this folder and used `make init-db` or `poetry install`
- “ads.db not found”: run `python cli.py init-db` first, then create profiles
- Want to start over: delete `ads.db` and run `python cli.py init-db`

You’re set — experiment with aggressive vs defensive strategies, nudge the knobs, and see outcomes in minutes.

