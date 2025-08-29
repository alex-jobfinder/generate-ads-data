Here’s a **Medium-optimized** version you can paste directly into the editor (clean headings, short paragraphs, scannable bullets, fixed typography, corrected CLI flags, and SQLite-safe SQL):

---

# 🚀 Generate Realistic Netflix Ads Data: A Complete Guide for Data Engineers

*Build a comprehensive ads analytics platform with realistic performance data, smart constraints, and strategic campaign profiles.*

---

## 🎯 Overview

This platform generates **realistic Netflix-style ads data** for testing, development, and analytics. It creates complete entities and metrics, including:

- **Advertisers & Campaigns** with realistic targeting and budgets
- **Performance Metrics** (CTR, CPM, viewability, video completion rates)
- **Extended Analytics** (audience insights, supply funnel efficiency, auction performance)
- **Strategic Campaign Profiles** (Gain vs. Defend Market Share)

**Great for:** 🧪 pipeline testing · 📊 dashboards · 🎓 learning metrics · 🚀 prototyping analytics features

---

## 🛠️ Installation & Setup

**Prerequisites**

- Python 3.10+
- Git
- (Optional) Cursor IDE with SQLite3 Editor for easy browsing

**1) Clone**

```bash
git clone https://github.com/your-username/generate-ads-data.git
cd generate-ads-data
```

**2) Install**

```bash
# Poetry (recommended)
poetry install

# or pip
pip install -r requirements.txt
```

**3) Initialize DB**

```bash
python cli.py init-db
```

**4) (Optional) Cursor SQLite3 Editor**

* Open Cursor → Extensions → search “SQLite3 Editor” by yy0931 → Install
* Benefits: visual schema, query editor, exports

---

## 🚀 Generate the Data

**Quick Start (everything in one go)**

```bash
./run_all.sh
```

This creates:

- **3 examples** (Luxury Auto, Crunchy Snacks, NexBank)
- **4 campaign profiles** (High CPM, Mobile, Interactive, Multi-device)
- **7 strategic profiles** (Gain vs. Defend Market Share)
- **6,000+ performance rows**

**Step-by-Step (granular control)**

**1) Create Examples**

```bash
# Luxury auto awareness
python cli.py create-example \
  --template cli_templates/examples/netflix-ads-examples.yml \
  --example luxury_auto_awareness

# Crunchy snacks consideration
python cli.py create-example \
  --template cli_templates/examples/netflix-ads-examples.yml \
  --example crunchy_snacks_consideration

# NexBank conversion
python cli.py create-example \
  --template cli_templates/examples/netflix-ads-examples.yml \
  --example nexbank_conversion
```

**2) Create Campaign Profiles**

```bash
python cli.py create-profile --name high_cpm_tv_awareness
python cli.py create-profile --name mobile_consideration
python cli.py create-profile --name conversion_interactive
python cli.py create-profile --name multi_device_advanced
```

**3) Create Strategic Profiles**

```bash
# Gain Market Share
python cli.py create-profile --name high_cpm_tv_awareness
python cli.py create-profile --name mobile_consideration
python cli.py create-profile --name conversion_interactive

# Defend Market Share
python cli.py create-profile --name high_cpm_tv_awareness
python cli.py create-profile --name mobile_consideration
python cli.py create-profile --name conversion_interactive
python cli.py create-profile --name multi_device_advanced
```

**What gets generated**

- **Advertiser** (company details)
- **Campaign** (objective, targeting, budget)
- **Line Items** (formats, placements, targeting JSON)
- **Creatives** (video specs, interactive)
- **Performance** (hourly metrics for ≥7 days)
- **Extended Metrics** (viewability, completion, audience, funnel)

---

## 🔍 Query Your Data

**Schema at a glance**

- `advertisers` → `campaigns` (1-many)
- `campaigns` → `line_items`, `creatives`, `performance`, `performance_ext` (1-many)

**Open DB in Cursor**

1. Right-click `ads.db` → Open With → *SQLite3 Editor*
2. Explore tables in sidebar; click to preview schema and rows

**Queries (SQLite-compatible)**

**1) Campaign Overview**

```sql
SELECT
  c.id,
  c.name,
  c.objective,
  c.target_cpm,
  c.budget,
  a.name AS advertiser_name,
  a.industry
FROM campaigns c
JOIN advertisers a ON c.advertiser_id = a.id
ORDER BY c.budget DESC;
```

**2) Performance Summary**

```sql
SELECT
  c.name AS campaign_name,
  COUNT(p.id) AS performance_records,
  AVG(p.ctr) AS avg_ctr,
  AVG(p.cpm) AS avg_cpm,
  SUM(p.impressions) AS total_impressions,
  SUM(p.clicks) AS total_clicks
FROM campaigns c
JOIN performance p ON c.id = p.campaign_id
GROUP BY c.id, c.name
ORDER BY total_impressions DESC;
```

**3) Extended Metrics (viewability, completion, funnel)**

```sql
SELECT
  c.name AS campaign_name,
  AVG(ep.viewability_rate) AS avg_viewability,
  AVG(ep.video_completion_rate) AS avg_completion,
  AVG(ep.effective_cpm) AS avg_effective_cpm,
  AVG(ep.supply_funnel_efficiency) AS avg_funnel_efficiency
FROM campaigns c
JOIN performance_ext ep ON c.id = ep.campaign_id
GROUP BY c.id, c.name
HAVING avg_viewability > 0.7
ORDER BY avg_funnel_efficiency DESC;
```

**4) Performance by Objective**

```sql
SELECT
  c.objective,
  COUNT(DISTINCT c.id) AS campaign_count,
  AVG(p.ctr) AS avg_ctr,
  AVG(p.cpm) AS avg_cpm,
  AVG(ep.viewability_rate) AS avg_viewability,
  AVG(ep.video_completion_rate) AS avg_completion
FROM campaigns c
JOIN performance p ON c.id = p.campaign_id
JOIN performance_ext ep ON c.id = ep.campaign_id
GROUP BY c.objective
ORDER BY avg_ctr DESC;
```

**5) Industry Performance**

```sql
SELECT
  a.industry,
  COUNT(DISTINCT c.id) AS campaign_count,
  AVG(p.ctr) AS avg_ctr,
  AVG(p.cpm) AS avg_cpm,
  SUM(p.impressions) AS total_impressions,
  SUM(p.spend) AS total_spend
FROM advertisers a
JOIN campaigns c ON a.id = c.advertiser_id
JOIN performance p ON c.id = p.campaign_id
GROUP BY a.industry
ORDER BY total_spend DESC;
```

**6) Time-Based Trends (last 7 days)**

```sql
SELECT
  date(p.timestamp) AS date,
  CAST(strftime('%H', p.timestamp) AS INTEGER) AS hour,
  AVG(p.ctr) AS avg_ctr,
  AVG(p.cpm) AS avg_cpm,
  SUM(p.impressions) AS total_impressions,
  SUM(p.clicks) AS total_clicks
FROM performance p
WHERE p.timestamp >= datetime('now', '-7 days')
GROUP BY date, hour
ORDER BY date DESC, hour ASC;
```

**7) Audience Insights (JSON targeting)**

```sql
SELECT
  c.name AS campaign_name,
  c.objective,
  json_extract(li.targeting_json, '$.DEVICE') AS target_devices,
  json_extract(li.targeting_json, '$.CONTENT_GENRE') AS target_genres,
  AVG(ep.reach) AS avg_reach,
  AVG(ep.frequency) AS avg_frequency
FROM campaigns c
JOIN line_items li ON c.id = li.campaign_id
JOIN performance_ext ep ON c.id = ep.campaign_id
GROUP BY c.id, c.name, li.targeting_json
ORDER BY avg_reach DESC;
```

> 💡 Tip: SQLite function names are case-insensitive, but `strftime(...)` is preferred over `HOUR(...)`.

---

## 📊 Advanced Analytics Examples

**Supply Funnel Efficiency**

```sql
SELECT
  c.name AS campaign_name,
  AVG(ep.supply_funnel_efficiency) AS funnel_efficiency,
  AVG(ep.auction_win_rate) AS win_rate,
  AVG(ep.fill_rate) AS fill_rate,
  AVG(ep.response_rate) AS response_rate
FROM campaigns c
JOIN performance_ext ep ON c.id = ep.campaign_id
GROUP BY c.id, c.name
HAVING funnel_efficiency > 0.6
ORDER BY funnel_efficiency DESC;
```

**Video Performance Deep-Dive**

```sql
SELECT
  c.name AS campaign_name,
  AVG(ep.video_start_rate) AS start_rate,
  AVG(ep.video_completion_rate) AS completion_rate,
  AVG(ep.video_skip_rate) AS skip_rate,
  AVG(ep.avg_watch_time_seconds) AS avg_watch_time
FROM campaigns c
JOIN performance_ext ep ON c.id = ep.campaign_id
WHERE ep.video_starts > 0
GROUP BY c.id, c.name
ORDER BY completion_rate DESC;
```

---

## 🏗️ Architecture & Design

**Highlights**

- 🔄 **Registry Pattern** for central access to domain components
- 🛡️ **Smart Constraints** so generated data always passes DB checks
- 🧮 **Safe Division** utilities to avoid divide-by-zero
- 🎯 **Strategic Profiles** aligned to business objectives
- 📊 **Realistic Generation** (Faker + business logic + time patterns)

**Schema**

- `advertisers`, `campaigns`, `line_items`, `creatives`, `performance`, `performance_ext`

**Data Quality Guarantees**

- Constraint satisfaction
- Logical metric relationships
- Varied yet consistent campaign behaviors
- Time-series patterns that feel real

---

## 🎉 Conclusion

This platform gives you everything to:

* ✅ Build realistic ads analytics pipelines
* ✅ Prototype dashboards and features with confidence
* ✅ Learn and teach digital ads metrics hands-on
* ✅ Compare performance across objectives and industries

**Next steps**

1. Explore data in the SQLite3 Editor
2. Write custom queries for your use-cases
3. Add new profiles/metrics
4. Integrate with your analytics stack (dbt, Looker, Tableau, etc.)

**Resources**

* 📚 `README.md` — Platform docs
* 🏗️ `WORKFLOW_VISUAL.md` — Architecture overview
* 🧪 `tests/` — Test suite
* 🔧 `python cli.py --help` — CLI commands

---

*Ready to dive in?* Clone the repo, run `./run_all.sh`, and start exploring with the SQLite3 Editor in Cursor. 🚀

**Suggested tags:** `data-engineering`, `analytics`, `sqlite`, `python`, `digital-advertising`
