# 🎯 Netflix Ads Data Generator - Advertiser's Guide

> **For Non-Technical Advertisers**: This tool helps you create realistic Netflix advertising campaigns to test different strategies, understand performance patterns, and optimize your ad spend.

## 🚀 Quick Start (5 Minutes)

### 1. Install the Tool
```bash
# Download and setup
git clone <your-repo-url>
cd generate-ads-data

# Install dependencies (one-time setup)
python -m pip install -r requirements.txt
# OR if you have Poetry:
poetry install
```

### 2. Create Your First Campaign
```bash
# Create a luxury auto awareness campaign
python cli.py create-profile --name high_cpm_tv_awareness

# Create a mobile consideration campaign  
python cli.py create-profile --name mobile_consideration
```

### 3. View Results
```bash
# Check what was created
python cli.py list-campaigns --format table

# Export campaign data
python cli.py export-campaign --id 1 --format csv
```

---

## 🎭 Campaign Strategy Profiles

### 🚀 **AGGRESSIVE PROFILES** (Gain Market Share)
*High-risk, high-reward campaigns focused on expansion and growth*

```
┌─────────────────────────────────────────────────────────────┐
│                    🚀 AGGRESSIVE STRATEGY                  │
├─────────────────────────────────────────────────────────────┤
│  Objective: GAIN MARKET SHARE                              │
│  Risk Level: HIGH                                          │
│  Expected ROI: 3x-5x (if successful)                      │
│  Budget Allocation: 70% Awareness, 20% Consideration      │
│                                                             │
│  📊 Campaign Mix:                                          │
│  • High CPM TV ($20-25)                                   │
│  • Premium Content Genres                                  │
│  • Broad Geographic Reach                                  │
│  • Interactive Creatives                                   │
└─────────────────────────────────────────────────────────────┘
```

**Use When:**
- Entering new markets
- Launching new products
- Competing with established brands
- Need rapid brand awareness

**Profile Commands:**
```bash
# High-budget luxury awareness
python cli.py create-profile --name high_cpm_tv_awareness

# Mobile gaming expansion
python cli.py create-profile --name mobile_consideration

# Startup conversion push
python cli.py create-profile --name conversion_interactive
```

---

### 🛡️ **DEFENSIVE PROFILES** (Defend Market Share)
*Protective campaigns focused on retention and customer loyalty*

```
┌─────────────────────────────────────────────────────────────┐
│                    🛡️ DEFENSIVE STRATEGY                  │
├─────────────────────────────────────────────────────────────┤
│  Objective: DEFEND MARKET SHARE                            │
│  Risk Level: LOW                                           │
│  Expected ROI: 1.5x-2x (stable)                           │
│  Budget Allocation: 40% Retention, 40% Loyalty, 20% New   │
│                                                             │
│  📊 Campaign Mix:                                          │
│  • Moderate CPM ($12-18)                                  │
│  • Niche Content Targeting                                 │
│  • Loyal Customer Segments                                 │
│  • Performance-Focused                                     │
└─────────────────────────────────────────────────────────────┘
```

**Use When:**
- Protecting existing market position
- Customer retention campaigns
- Seasonal maintenance
- Budget optimization

**Profile Commands:**
```bash
# Customer retention focus
python cli.py create-profile --name mobile_consideration

# Loyalty program conversion
python cli.py create-profile --name conversion_interactive

# Premium service maintenance
python cli.py create-profile --name multi_device_advanced
```

---

## 📊 Campaign Performance Visualization

### Hourly Performance Pattern
```
Performance Over 24 Hours
┌─────────────────────────────────────────────────────────────┐
│  CPM: $18.50  |  CTR: 2.4%  |  Conversion: 0.8%         │
├─────────────────────────────────────────────────────────────┤
│  6AM  9AM  12PM  3PM  6PM  9PM  12AM                     │
│  📈   📈   📊   📊   📈   📈   📉                        │
│  Low  Peak Peak Peak Peak Peak Low                        │
│                                                             │
│  🎯 Peak Hours: 9AM-9PM (High Engagement)                │
│  💤 Off Hours: 12AM-6AM (Lower CPM)                      │
└─────────────────────────────────────────────────────────────┘
```

### Campaign Objective Performance
```
┌─────────────────────────────────────────────────────────────┐
│                    CAMPAIGN PERFORMANCE                    │
├─────────────────────────────────────────────────────────────┤
│  🎯 AWARENESS:                                             │
│  • Reach: 2.4M impressions                                │
│  • CPM: $18.50                                            │
│  • Brand Lift: +23%                                       │
│                                                             │
│  💭 CONSIDERATION:                                         │
│  • CTR: 2.4%                                              │
│  • Engagement: 18.7%                                      │
│  • Video Completion: 67%                                  │
│                                                             │
│  🚀 CONVERSION:                                            │
│  • Conversion Rate: 0.8%                                  │
│  • Cost per Action: $2.31                                 │
│  • ROI: 3.2x                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Useful Advertiser Features

### 1. **Campaign Comparison Tool**
```bash
# Compare two campaigns side-by-side
python cli.py compare-campaigns --campaign1 1 --campaign2 2

# Compare by objective type
python cli.py compare-by-objective --objective AWARENESS --top-n 5
```

### 2. **Budget Optimization**
```bash
# Find optimal CPM for your budget
python cli.py optimize-cpm --budget 50000 --objective AWARENESS

# Calculate ROI projections
python cli.py project-roi --campaign-id 1 --scenarios 3 --optimistic
```

### 3. **Creative Testing**
```bash
# Test different creative formats
python cli.py test-creative --format STANDARD_VIDEO --duration 15 --interactive

# A/B test targeting strategies
python cli.py ab-test --variant-a "mobile_only" --variant-b "multi_device" --test-duration 14
```

### 4. **Performance Forecasting**
```bash
# Predict campaign performance
python cli.py forecast --campaign-id 1 --days 30 --include-seasonal

# Seasonal trend analysis
python cli.py seasonal-trends --campaign-id 1 --period 90
```

---

## 📋 Complete Campaign Creation

### Run All Examples (Recommended for First Time)
```bash
# This creates everything you need
./run_all.sh

# What gets created:
# ✅ 3 Complete Examples (Luxury Auto, Crunchy Snacks, NexBank)
# ✅ 4 Campaign Profiles (High CPM, Mobile, Interactive, Multi-device)
# ✅ 3 Aggressive Profiles (Gain Market Share)
# ✅ 4 Defensive Profiles (Defend Market Share)
# ✅ Performance data for all campaigns
```

### Manual Campaign Creation
```bash
# Step 1: Create advertiser
python cli.py create-advertiser --auto

# Step 2: Create campaign with specific profile
python cli.py create-profile --name high_cpm_tv_awareness

# Step 3: Generate performance data
python cli.py generate-performance --campaign-id 1
```

---

## 🎨 Customizing Your Campaigns

### Modify Campaign Parameters
```bash
# Override specific values (note: budget field not available in current schema)
python cli.py create-profile --name high_cpm_tv_awareness \
  --test-fields "campaign.target_cpm=2250"

# Test different targeting
python cli.py create-profile --name mobile_consideration \
  --test-fields "line_items.targeting_json={\"AGE_RANGE\":[\"18-24\"]}"
```

### Create Custom Scenarios
```bash
# Test specific business scenarios
python cli.py test-scenario --name "holiday_promotion"

# Test field combinations
python cli.py test-fields --template "your_template.yml" \
  --focus "campaign.target_cpm,line_items.targeting_json"
```

---

## 📊 Understanding Your Data

### Database Structure
```
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE OVERVIEW                       │
├─────────────────────────────────────────────────────────────┤
│  📁 advertisers/           - Company & brand information  │
│  📁 campaigns/             - Campaign settings & objectives│
│  📁 line_items/            - Targeting & bidding strategies│
│  📁 creatives/             - Ad creative specifications   │
│  📁 campaign_performance/  - Hourly performance metrics   │
│  📁 campaign_performance_extended - Extended performance  │
│  📁 budgets/               - Budget allocation data       │
│  📁 flights/               - Campaign flight dates        │
│  📁 frequency_caps/        - Frequency limiting rules     │
└─────────────────────────────────────────────────────────────┘
```

### Key Metrics Explained
- **CPM (Cost Per Mille)**: Cost per 1,000 impressions
- **CTR (Click-Through Rate)**: Percentage of clicks per impression
- **Conversion Rate**: Percentage of clicks that result in desired action
- **ROI (Return on Investment)**: Revenue generated per dollar spent
- **Brand Lift**: Increase in brand awareness/consideration

### Current Database Status
```bash
# Check your database health and data counts
python cli.py status

# Expected output shows:
# - Database size and health
# - Campaign counts by type
# - System information
```

---

## 🚀 Interactive Demo & Testing

### Run the Complete Demo
```bash
# See all features in action
python advertiser_demo.py

# This demonstrates:
# ✅ Campaign creation and management
# ✅ Performance analysis and comparison
# ✅ Budget optimization and ROI projection
# ✅ Creative testing and A/B testing
# ✅ Performance forecasting and trends
# ✅ Data export and reporting
```

### Test Individual Features
```bash
# Test campaign listing
python cli.py list-campaigns --format table
python cli.py list-campaigns --format csv
python cli.py list-campaigns --format json

# Test campaign comparison
python cli.py compare-campaigns --campaign1 1 --campaign2 2

# Test data export
python cli.py export-campaign --id 1 --format json --include-performance
```

---

## 🔧 Troubleshooting & Common Issues

### Database Issues
```bash
# Database not found or corrupted
python cli.py init-db

# Database exists but no data
./run_all.sh

# Check database health
python cli.py status
```

### Permission Issues
```bash
# Make scripts executable
chmod +x run_all.sh
chmod +x advertiser_demo.py

# Check file permissions
ls -la *.sh *.py
```

### Missing Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Or use Poetry
poetry install

# Check Python version (requires 3.10+)
python --version
```

### Command Failures
```bash
# Get help for any command
python cli.py --help
python cli.py create-profile --help

# Check if database has data
python cli.py list-campaigns --format table

# Verify campaign exists before using ID
python cli.py export-campaign --id 1 --format json
```

---

## 📈 Real-World Usage Examples

### Example 1: Launching a New Product
```bash
# 1. Create aggressive awareness campaign
python cli.py create-profile --name high_cpm_tv_awareness

# 2. Check campaign performance
python cli.py list-campaigns --format table

# 3. Compare with existing campaigns
python cli.py compare-by-objective --objective AWARENESS

# 4. Export data for analysis
python cli.py export-campaign --id 1 --format csv
```

### Example 2: Optimizing Existing Campaigns
```bash
# 1. List all campaigns
python cli.py list-campaigns --format table

# 2. Compare similar campaigns
python cli.py compare-campaigns --campaign1 1 --campaign2 2

# 3. Optimize CPM for budget
python cli.py optimize-cpm --budget 75000 --objective CONVERSION

# 4. Project ROI improvements
python cli.py project-roi --campaign-id 1 --scenarios 3
```

### Example 3: A/B Testing Strategy
```bash
# 1. Create test variants
python cli.py create-profile --name mobile_consideration
python cli.py create-profile --name mobile_consideration

# 2. Set up A/B test
python cli.py ab-test --variant-a "mobile_only" --variant-b "multi_device"

# 3. Monitor performance
python cli.py compare-campaigns --campaign1 1 --campaign2 2

# 4. Export results
python cli.py export-campaign --id 1 --format json
```

---

## 🎯 Getting Help & Support

### Built-in Help System
```bash
# General help
python cli.py --help

# Command-specific help
python cli.py create-profile --help
python cli.py list-campaigns --help
python cli.py compare-campaigns --help
```

### System Diagnostics
```bash
# Check system status
python cli.py status

# Verify database connectivity
python cli.py list-campaigns --format table

# Test data export
python cli.py export-campaign --id 1 --format json
```

### Documentation & Examples
- **Quick Reference**: `ADVERTISER_QUICK_REFERENCE.md`
- **Demo Script**: `advertiser_demo.py`
- **CLI Templates**: `cli_templates/` folder
- **Examples**: `cli_templates/examples/` folder

---

## 🚀 Next Steps & Best Practices

### 1. **Start Simple**
```bash
# Run the complete demo first
python advertiser_demo.py

# Then create your own campaigns
./run_all.sh
```

### 2. **Experiment & Learn**
- Try different campaign profiles
- Compare performance across objectives
- Test various CPM levels
- Export data for external analysis

### 3. **Scale & Optimize**
- Use comparison tools to find best performers
- Optimize CPM based on budget constraints
- Forecast performance for planning
- A/B test creative and targeting strategies

### 4. **Data-Driven Decisions**
- Export campaign data to Excel/Google Sheets
- Use performance metrics for budget allocation
- Compare seasonal trends across campaigns
- Track ROI improvements over time

---

## 📞 Support & Community

- **Documentation**: Check the `docs/` folder for detailed guides
- **Examples**: Review `cli_templates/` for campaign templates
- **Issues**: Report problems in the project repository
- **Demo**: Run `python advertiser_demo.py` for interactive learning

---

## 🎉 Success Checklist

Before you start advertising, ensure you have:
- ✅ [ ] Tool installed and dependencies resolved
- ✅ [ ] Database initialized with sample data
- ✅ [ ] Run demo script to understand features
- ✅ [ ] Created test campaigns with different profiles
- ✅ [ ] Exported and analyzed campaign data
- ✅ [ ] Compared performance across objectives
- ✅ [ ] Optimized CPM for your budget
- ✅ [ ] Set up A/B testing scenarios

---

*Happy Campaign Testing! 🚀📺*

**💡 Pro Tip**: Start with `python advertiser_demo.py` to see everything in action before diving into your own campaigns!