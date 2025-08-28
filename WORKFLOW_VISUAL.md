# 🚀 Netflix Ads Data Generation - Complete Workflow & Architecture

## **🎯 System Architecture Overview**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🏗️ Netflix Ads Data Generation Platform                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🎯 CENTRALIZED REGISTRY PATTERN                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
┌─────────────────────────┐ ┌─────────────────────────┐ ┌─────────────────────────┐
│ 📊 ORM Registry         │ │ 🎨 Schema Registry      │ │ 🔧 Enum Registry        │
│                         │ │                         │ │                         │
│ • Base                  │ │ • AdvertiserCreate      │ │ • BudgetType            │
│ • EntityBase            │ │ • CampaignCreate        │ │ • CreativeMimeType      │
│ • Advertiser            │ │ • LineItemCreate        │ │ • TargetingKey          │
│ • Campaign              │ │ • CreativeCreate        │ │ • Objective             │
│ • LineItem              │ │ • FrequencyCapSchema    │ │ • QAStatus              │
│ • Creative              │ │ • FlightSchema          │ │ • EntityStatus          │
│ • Flight                │ │ • BudgetSchema          │ │ • CampaignStatus        │
│ • Budget                │ │ • Targeting             │ │ • AdFormat              │
│ • FrequencyCap          │ │                         │ │ • Currency              │
│ • Performance           │ │                         │ │ • DspPartner            │
└─────────────────────────┘ └─────────────────────────┘ └─────────────────────────┘
                    │                   │                   │
                    └───────────────────┼───────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🔄 UNIFIED ACCESS THROUGH REGISTRY                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
┌─────────────────────────┐ ┌─────────────────────────┐ ┌─────────────────────────┐
│ 🎯 registry.Advertiser  │ │ 🎯 registry.Campaign    │ │ 🎯 registry.BudgetType  │
│                         │ │                         │ │                         │
│ registry.CampaignCreate │ │ registry.LineItem       │ │ registry.CreativeMime   │
│ registry.Objective      │ │ registry.Creative       │ │ registry.TargetingKey   │
│ registry.EntityStatus   │ │ registry.Flight         │ │ registry.QAStatus       │
└─────────────────────────┘ └─────────────────────────┘ └─────────────────────────┘
```

## **🚀 Complete Data Generation Workflow (`run_all.sh`)**

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
│ 🚗 luxury_auto_         │ │ 🍿 crunchy_snacks_      │ │ 🏦 nexbank_conversion   │
│ awareness               │ │ consideration           │ │                         │
│                         │ │                         │ │                         │
│ • Advertiser: Luxury    │ │ • Advertiser: Crunchy  │ │ • Advertiser: NexBank   │
│   Auto Co               │ │   Snacks               │ │                         │
│ • Campaign: EV          │ │ • Campaign: New        │ │ • Campaign: App         │
│   Awareness Launch      │ │   Flavor Consideration │ │   Acquisition Q4        │
│ • CPM: $25.00           │ │ • CPM: $20.00          │ │ • CPM: $18.00           │
│ • Budget: $120k         │ │ • Budget: $60k         │ │ • Budget: $40k          │
│ • Format: TV Drama      │ │ • Format: Mobile       │ │ • Format: Mobile/      │
│ • Duration: 30s         │ │   Comedy               │ │   Desktop Business      │
│ • Performance: 480+     │ │ • Duration: 15s        │ │ • Duration: 15s         │
│   rows                  │ │ • Performance: 504+    │ │ • Performance: 432+     │
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
│ • High CPM: $25.00  │ │ • Mobile-focused    │ │ • Interactive       │
│ • Large Budget      │ │ • Comedy/Reality    │ │ • QR Codes          │
│ • TV Drama          │ │ • Short Duration    │ │ • Conversion        │
│ • Premium Content   │ │ • Mobile Targeting  │ │ • Business Docs     │
│ • Performance:      │ │ • Performance:      │ │ • Performance:      │
│   1104+ rows        │ │   936+ rows         │ │   744+ rows         │
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
│ 📊 Database: ads.db     │ │ 📊 Size: ~12MB          │ │ 📊 Contains: Netflix   │
│                         │ │                         │ │   Ads Data              │
│ • SQLite Database       │ │ • Normal Performance   │ │                         │
│ • 7+ Advertisers       │ │ • Extended Performance │ │ • Ready for Modeling    │
│ • 7+ Campaigns         │ │ • ~4,000+ Rows Total   │ │ • Realistic Examples    │
│ • 7+ Line Items        │ │                         │ │ • Performance Metrics   │
│ • 7+ Creatives         │ │                         │ │                         │
└─────────────────────────┘ └─────────────────────────┘ └─────────────────────────┘
                    │                               │                               │
                    └───────────────────────────────┼───────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🎉 COMPLETE: Netflix Ads Data Generated!                │
└─────────────────────────────────────────────────────────────────────────────┘
```

## **🔧 Registry Pattern Implementation**

### **Registry Structure (`models/registry.py`)**

```python
class Registry:
    """Main registry class providing unified access to all domain components."""
    
    def __init__(self):
        self.enums = EnumRegistry()      # All enums and constants
        self.orm = ORMRegistry()         # All SQLAlchemy models
        self.schemas = SchemaRegistry()  # All Pydantic schemas
        self.utils = UtilityRegistry()   # All utility functions
    
    # Direct access properties for convenience
    @property
    def BudgetType(self):
        return self.enums.BudgetType
    
    @property
    def CreativeMimeType(self):
        return self.enums.CreativeMimeType
    
    @property
    def Advertiser(self):
        return self.orm.Advertiser
    
    @property
    def CampaignCreate(self):
        return self.schemas.CampaignCreate
```

### **Usage Examples**

```python
# Before (scattered imports)
from models.enums import BudgetType, CreativeMimeType
from models.schemas import CreativeCreate
from models.orm import Advertiser

# After (unified registry)
from models.registry import registry

# Access everything through registry
budget_type = registry.BudgetType.lifetime.value
mime_type = registry.CreativeMimeType.mp4
creative = registry.CreativeCreate(asset_url="...", mime_type=mime_type)
advertiser = registry.Advertiser(name="Netflix")
```

## **📊 Data Generation Architecture**

### **Service Layer (`services/`)**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🔄 Data Generation Flow                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
┌─────────────────────────┐ ┌─────────────────────────┐ ┌─────────────────────────┐
│ 📊 streamlined_         │ │ 🎨 generator.py          │ │ 📈 performance.py       │
│ processor.py            │ │                         │ │                         │
│                         │ │                         │ │                         │
│ • Main orchestration    │ │ • Pydantic → ORM        │ │ • Hourly metrics        │
│ • Example creation      │ │ • Payload creation      │ • Realistic ranges       │
│ • Profile processing    │ │ • Data transformation   │ • Performance simulation │
│ • Performance gen       │ │ • Registry integration  │ • Extended metrics       │
└─────────────────────────┘ └─────────────────────────┘ └─────────────────────────┘
```

### **Factory Layer (`factories/`)**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🏭 Faker Providers with Registry                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
┌─────────────────────────┐ ┌─────────────────────────┐ ┌─────────────────────────┐
│ 🎲 fake_budget_and_cpm  │ │ 🎯 fake_targeting_v2    │ │ 🎨 make_profile_       │
│                         │ │                         │ │ creative                │
│                         │ │                         │ │                         │
│ • Uses registry.        │ │ • Uses registry.        │ │ • Uses registry.        │
│   PricingDefaults       │ │   TargetingKey          │ │   CreativeMimeType      │
│ • Uses registry.        │ │ • Uses registry.        │ │ • Uses registry.        │
│   BudgetType            │ │   TargetingDefaults     │ │   CreativeDefaults      │
└─────────────────────────┘ └─────────────────────────┘ └─────────────────────────┘
```

## **🧪 Testing Architecture (18 Tests)**

### **Test Coverage Matrix**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🧪 Comprehensive Test Suite                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        │                               │                               │
        ▼                               ▼                               ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│ 🔧 CLI & Config     │ │ 📊 Data Flows       │ │ 🗄️ ORM Persistence  │
│                     │ │                     │ │                     │
│ • Command execution │ │ • End-to-end flows  │ │ • Database ops      │
│ • Environment vars  │ │ • Advertiser creation│ │ • Constraints       │
│ • Exit codes        │ │ • Campaign creation │ │ • Relationships     │
│ • JSON outputs      │ │ • Registry usage    │ │ • Timestamps        │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘
        │                               │                               │
        └───────────────────────────────┼───────────────────────────────┘
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        │                               │                               │
        ▼                               ▼                               ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│ ✅ Schema Validation│ │ 📈 Performance       │ │ 🎯 Targeting &      │
│                     │ │ Metrics             │ │ Formats             │
│                     │ │                     │ │                     │
│ • Pydantic schemas  │ │ • Data generation   │ │ • Ad formats        │
│ • Data integrity    │ │ • Realistic ranges  │ │ • Targeting keys    │
│ • Validation rules  │ │ • Extended metrics  │ │ • Enum validation   │
│ • Type checking     │ │ • Performance tests │ │ • Whitelist tests   │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

## **🚀 Command Flow & Usage**

### **Complete Data Generation**

```bash
# Generate everything in one command
./run_all.sh

# This runs:
# 1. 3 Complete Examples (luxury_auto_awareness, crunchy_snacks_consideration, nexbank_conversion)
# 2. 4 Campaign Profiles (high_cpm_tv_awareness, mobile_consideration, conversion_interactive, multi_device_advanced)
# 3. Performance data generation for all campaigns
# 4. Database status check and summary
```

### **Individual Commands**

```bash
# Database management
python cli.py init-db

# Create entities
python cli.py create-advertiser --auto
python cli.py create-campaign --advertiser-id 1 --auto

# Create from profiles
python cli.py create-profile --name high_cpm_tv_awareness

# Create from examples
python cli.py create-example --template cli_templates/examples/netflix-ads-examples.yml --example luxury_auto_awareness
```

### **Development Commands**

```bash
# Testing
make test                    # Run all 18 tests
make test-one FILE=tests/test_flows_v1.py

# Development
make deps                    # Setup virtual environment
make init-db                 # Initialize database
make clean                   # Clean artifacts
```

## **📈 Performance & Scalability**

### **Current Metrics**

- **Database Size**: ~12MB for complete dataset
- **Generation Speed**: Complete dataset in ~15 seconds
- **Test Coverage**: 18 tests, 100% core functionality
- **Memory Usage**: Efficient streaming for large datasets
- **Registry Access**: O(1) access to all components

### **Scalability Features**

- **Modular Architecture**: Easy to add new models, schemas, enums
- **Registry Pattern**: Centralized access reduces coupling
- **Template System**: YAML-based configuration for easy extension
- **Performance Simulation**: Configurable data generation parameters
- **Database Optimization**: Proper indexing and constraints

## **🔮 Future Enhancements**

### **Short Term (1-3 months)**

- **🎯 Advanced Targeting**: More sophisticated targeting algorithms
- **📊 Real-time Metrics**: Live performance data simulation
- **🌐 Multi-platform**: Support for other streaming platforms

### **Medium Term (3-6 months)**

- **🤖 AI Integration**: ML-powered content and targeting optimization
- **📱 Mobile App**: Native mobile interface for data management
- **☁️ Cloud Deployment**: Docker containers and cloud deployment

### **Long Term (6+ months)**

- **🔗 API Layer**: RESTful API for external integrations
- **📊 Analytics Dashboard**: Web-based data visualization
- **🔄 Real-time Sync**: Live data synchronization capabilities

## **🎯 Registry Pattern Benefits**

### **Before Refactoring**

- **Scattered imports** across multiple files
- **Hard to maintain** when changing enums/schemas
- **Inconsistent access** patterns
- **Difficult testing** with multiple dependencies

### **After Refactoring**

- **🔄 Single Source of Truth** - All domain components in one place
- **🔧 Easy Maintenance** - Change enums/schemas, affects everything automatically
- **🧹 Clean Imports** - One import statement instead of multiple
- **📈 Future-Proof** - Easy to add new properties or change implementations
- **🧪 Better Testing** - Centralized access makes mocking and testing easier

## **🏆 Success Metrics**

- **✅ All 18 tests passing**
- **✅ Registry pattern fully implemented**
- **✅ Complete data generation working**
- **✅ Performance data realistic and comprehensive**
- **✅ Architecture clean and maintainable**
- **✅ Documentation comprehensive and up-to-date**

---

**🎉 Ready to generate Netflix ads data?** 

```bash
./run_all.sh  # Generate complete dataset
```

**🚀 The registry pattern makes this platform powerful, maintainable, and ready for the future!**
