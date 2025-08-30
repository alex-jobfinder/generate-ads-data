# 🎯 Advertiser Quick Reference Card

## 🚀 Essential Commands

### Campaign Creation
```bash
# Quick start - create everything
./run_all.sh

# Create specific campaign types
python cli.py create-profile --name high_cpm_tv_awareness      # Aggressive luxury
python cli.py create-profile --name mobile_consideration      # Defensive mobile
python cli.py create-profile --name conversion_interactive    # Interactive conversion
python cli.py create-profile --name multi_device_advanced     # Multi-device tech
```

### Campaign Management
```bash
# List all campaigns
python cli.py list-campaigns --format table

# Export campaign data
python cli.py export-campaign --id 1 --format csv

# Check system status
python cli.py status
```

## 🎭 Strategy Profiles

### 🚀 AGGRESSIVE (Gain Market Share)
- **High CPM TV**: `high_cpm_tv_awareness`
- **Mobile Gaming**: `mobile_consideration` 
- **Startup Push**: `conversion_interactive`

**Use for**: New markets, product launches, brand awareness

### 🛡️ DEFENSIVE (Defend Market Share)
- **Customer Retention**: `mobile_consideration`
- **Loyalty Programs**: `conversion_interactive`
- **Premium Services**: `multi_device_advanced`

**Use for**: Retention, maintenance, budget optimization

## 📊 Analysis & Optimization

### Performance Comparison
```bash
# Compare two campaigns
python cli.py compare-campaigns --campaign1 1 --campaign2 2

# Compare by objective
python cli.py compare-by-objective --objective AWARENESS
```

### Budget Optimization
```bash
# Find optimal CPM
python cli.py optimize-cpm --budget 50000 --objective AWARENESS

# Project ROI
python cli.py project-roi --campaign-id 1 --scenarios 3
```

### Creative Testing
```bash
# Test creative formats
python cli.py test-creative --format STANDARD_VIDEO --duration 15

# A/B test targeting
python cli.py ab-test --variant-a mobile_only --variant-b multi_device
```

## 🔮 Forecasting & Trends

```bash
# Performance forecast
python cli.py forecast --campaign-id 1 --days 30

# Seasonal analysis
python cli.py seasonal-trends --campaign-id 1 --period 90
```

## 🎨 Customization

### Override Default Values
```bash
# Custom budget and CPM
python cli.py create-profile --name high_cpm_tv_awareness \
  --test-fields "campaign.budget=75000,campaign.target_cpm=22.50"

# Custom targeting
python cli.py create-profile --name mobile_consideration \
  --test-fields "line_items.targeting_json={\"AGE_RANGE\":[\"18-24\"]}"
```

## 📈 Key Metrics Explained

- **CPM**: Cost per 1,000 impressions
- **CTR**: Click-through rate (% of clicks)
- **Conversion Rate**: % of clicks that convert
- **ROI**: Return on investment (revenue/spend)
- **Brand Lift**: Increase in brand awareness

## 🚨 Troubleshooting

```bash
# Database issues
python cli.py init-db

# Permission problems
chmod +x run_all.sh

# Missing dependencies
pip install -r requirements.txt
```

## 📞 Getting Help

```bash
# View all commands
python cli.py --help

# Command-specific help
python cli.py create-profile --help

# Run demo
python advertiser_demo.py
```

---

**💡 Pro Tips:**
1. Start with `./run_all.sh` to see everything in action
2. Use table format for quick overview: `--format table`
3. Export data for external analysis: `--format csv`
4. Test different scenarios with `--test-fields`
5. Compare campaigns to find best performers

**🎯 Success Path:**
1. **Create** → Run `./run_all.sh`
2. **Analyze** → Use comparison commands
3. **Optimize** → Adjust CPM and targeting
4. **Scale** → Export data for larger analysis

---

*Keep this card handy for quick reference! 🚀📺*
