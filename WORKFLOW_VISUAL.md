# 🚀 Netflix Ads Data Generation - Workflow Visual

## **ASCII Workflow Diagram for `run_all.sh`**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🚀 START: Netflix Ads Data Generation                    │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    📊 STEP 1: Creating Complete Examples                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
┌─────────────────────────┐ ┌─────────────────────────┐ ┌─────────────────────────┐
│ 🚗 luxury_auto_awareness │ │ 🍿 crunchy_snacks_     │ │ 🏦 nexbank_conversion   │
│                         │ │ consideration           │ │                         │
│ • Advertiser: Luxury    │ │ • Advertiser: Crunchy  │ │ • Advertiser: NexBank   │
│   Auto Co               │ │   Snacks               │ │                         │
│ • Campaign: EV          │ │ • Campaign: New        │ │ • Campaign: App         │
│   Awareness Launch      │ │   Flavor Consideration │ │   Acquisition Q4        │
│ • CPM: $15.50           │ │ • CPM: $12.75          │ │ • CPM: $18.25           │
│ • Budget: $120k         │ │ • Budget: $60k         │ │ • Budget: $40k          │
│ • Format: TV Drama      │ │ • Format: Mobile       │ │ • Format: Mobile/      │
│ • Duration: 30s         │ │   Comedy               │ │   Desktop Business      │
│ • Performance: 480+     │ │ • Duration: 15s        │ │ • Duration: 15s         │
│   rows                  │ │ • Performance: 696+    │ │ • Performance: 1248+    │
└─────────────────────────┘ │   rows                  │ │   rows                  │
                    │       └─────────────────────────┘ └─────────────────────────┘
                    │                   │                   │
                    └───────────────────┼───────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    📊 STEP 2: Creating Campaign Profiles                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        │                               │                               │
        ▼                               ▼                               ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│ 📺 high_cpm_tv_     │ │ 📱 mobile_          │ │ 🎯 conversion_      │
│ awareness           │ │ consideration       │ │ interactive         │
│                     │ │                     │ │                     │
│ • High CPM: $20.00  │ │ • Mobile-focused    │ │ • Interactive       │
│ • Large Budget      │ │ • Comedy/Reality    │ │ • QR Codes          │
│ • TV Drama          │ │ • Short Duration    │ │ • Conversion        │
│ • Premium Content   │ │ • Mobile Targeting  │ │ • Business Docs     │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘
        │                               │                               │
        └───────────────────────────────┼───────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    📊 STEP 3: Generation Summary                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
┌─────────────────────────┐ ┌─────────────────────────┐ ┌─────────────────────────┐
│ ✅ Successful: 7        │ │ 📁 Total Examples: 3    │ │ 📁 Total Profiles: 4    │
│                         │ │                         │ │                         │
│ • 3 Examples           │ │ • Luxury Auto           │ │ • High CPM TV           │
│ • 4 Profiles           │ │ • Crunchy Snacks        │ │ • Mobile                │
│ • All Performance      │ │ • NexBank               │ │ • Interactive           │
│   Generated            │ │                         │ │ • Multi-Device          │
└─────────────────────────┘ └─────────────────────────┘ └─────────────────────────┘
                    │                               │                               │
                    └───────────────────────────────┼───────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    📊 STEP 4: Database Status Check                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
┌─────────────────────────┐ ┌─────────────────────────┐ ┌─────────────────────────┐
│ 📊 Database: ads.db     │ │ 📊 Size: ~3-4MB         │ │ 📊 Contains: Netflix   │
│                         │ │                         │ │   Ads Data              │
│ • SQLite Database       │ │ • Normal Performance   │ │                         │
│ • 7 Advertisers        │ │ • Extended Performance │ │ • Ready for Modeling    │
│ • 7 Campaigns          │ │ • ~3,000+ Rows Total   │ │ • Realistic Examples    │
│ • 7 Line Items         │ │                         │ │ • Performance Metrics   │
│ • 7 Creatives          │ │                         │ │                         │
└─────────────────────────┘ └─────────────────────────┘ └─────────────────────────┘
                    │                               │                               │
                    └───────────────────────────────┼───────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🎉 COMPLETE: Netflix Ads Data Generated!                │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            🎯 What You Can Do Next                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        │                               │                               │
        ▼                               ▼                               ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│ 🔍 Explore Data     │ │ 📊 Test Queries     │ │ 🎨 Customize        │
│                     │ │                     │ │                     │
│ • Use SQLite        │ │ • Try Joins         │ │ • Modify Templates  │
│ • Query Tables      │ │ • Test Filters      │ │ • Add Examples      │
│ • Analyze Results   │ │ • Performance       │ │ • Create Profiles   │
│                     │ │   Analysis          │ │                     │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

## **🔄 Workflow Steps Breakdown**

### **Step 1: Complete Examples (3)**
```
luxury_auto_awareness → Crunchy Snacks → NexBank
     ↓                        ↓              ↓
  TV Drama              Mobile Comedy    Mobile Business
  $15.50 CPM           $12.75 CPM      $18.25 CPM
  $120k Budget         $60k Budget     $40k Budget
  30s Duration         15s Duration    15s Duration
```

### **Step 2: Campaign Profiles (4)**
```
High CPM TV → Mobile → Interactive → Multi-Device
     ↓         ↓          ↓            ↓
  $20 CPM   Mobile    QR Codes    Advanced
  Premium   Comedy    Business    Targeting
  Drama     Reality   Conversion  Multi-Platform
```

### **Step 3: Data Generation**
```
Examples + Profiles → Performance Data → Database
      ↓                    ↓              ↓
   7 Campaigns        ~3,000 Rows     ~3-4MB
   7 Advertisers     Normal + Ext     SQLite
   7 Line Items      Hourly Metrics   Ready
   7 Creatives       Realistic Data  for Use
```

## **⚡ Command Flow**

```bash
# The script runs these commands in sequence:
for example in luxury_auto_awareness crunchy_snacks_consideration nexbank_conversion; do
    python cli.py create-example --template examples/netflix-ads-examples.yml --example $example
done

for profile in high_cpm_tv_awareness mobile_consideration conversion_interactive multi_device_advanced; do
    python cli.py create-profile --name $profile
done
```

## **🎯 Result: Complete Netflix Ads Dataset**

- **7 Advertisers** with realistic names and industries
- **7 Campaigns** with different objectives and configurations  
- **7 Line Items** with various ad formats and targeting
- **7 Creatives** with different specifications and durations
- **Performance Data** for all campaigns with realistic metrics
- **Database Ready** for modeling, testing, and development

This workflow gives you **comprehensive Netflix ads data examples** quickly for database modeling! 🚀
