# 🚀 Netflix Ads Data Generation Platform

A comprehensive, production-ready platform for generating realistic Netflix ads data using modern Python technologies. Built with a centralized registry pattern for maintainability and extensibility.

## ✨ **Key Features**

- **🎯 Centralized Registry Pattern** - Single point of access to all models, schemas, and enums
- **🏗️ Modern Architecture** - SQLAlchemy 2.0, Pydantic v2, and comprehensive testing
- **📊 Rich Data Generation** - Realistic Netflix ads data with performance metrics
- **🔧 CLI-Driven Workflows** - Easy-to-use commands for data generation and management
- **🧪 Comprehensive Testing** - 18 tests covering all major functionality
- **📈 Performance Simulation** - Hourly performance data with realistic metrics

## 🏗️ **Architecture Overview**

### **Registry Pattern (`models/registry.py`)**
The heart of the system - a centralized registry that provides unified access to:
- **ORM Models** - SQLAlchemy database models
- **Pydantic Schemas** - Data validation and serialization
- **Enums & Constants** - Domain-specific values and configurations
- **Utility Functions** - Helper functions and validators

```python
from models.registry import registry

# Access anything through the registry
advertiser = registry.Advertiser(name="Netflix")
campaign = registry.CampaignCreate(name="Q4 Campaign")
mime_type = registry.CreativeMimeType.mp4
budget_type = registry.BudgetType.lifetime
```

### **Core Components**
- **`models/orm.py`** - SQLAlchemy ORM models with constraints and relationships
- **`models/schemas.py`** - Pydantic v2 schemas for data validation
- **`models/enums.py`** - Domain enums and configuration constants
- **`services/`** - Business logic and data processing
- **`factories/`** - Data generation using Faker with registry access
- **`cli.py`** - Click-based command-line interface

## 📁 **Directory Structure**

```
generate-ads-data/
├── models/                     # Core domain models
│   ├── registry.py            # 🎯 Centralized registry (NEW!)
│   ├── orm.py                 # SQLAlchemy ORM models
│   ├── schemas.py             # Pydantic validation schemas
│   ├── enums.py               # Domain enums and constants
│   └── __init__.py            # Registry-only exports
├── services/                   # Business logic
│   ├── streamlined_processor.py # Main data generation service
│   ├── generator.py           # ORM payload creation
│   ├── performance.py         # Performance data generation
│   ├── performance_ext.py     # Extended performance metrics
│   └── validators.py          # Cross-field validation
├── factories/                  # Data generation
│   └── faker_providers.py     # Faker providers using registry
├── cli_templates/             # CLI configuration templates
│   ├── examples/              # Netflix ads examples
│   ├── profiles/              # Campaign profiles
│   └── workflows/             # Workflow templates
├── tests/                     # Comprehensive test suite (18 tests)
├── cli.py                     # Main CLI application
├── db_utils.py                # Database utilities
├── run_all.sh                 # 🚀 Complete data generation script
└── Makefile                   # Development and testing commands
```

## 🚀 **Quick Start**

### **1. Setup Environment**
```bash
# Clone and setup
git clone <repository>
cd generate-ads-data

# Install dependencies
make deps
# or manually: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

### **2. Initialize Database**
```bash
make init-db
# or: python cli.py init-db
```

### **3. Generate Complete Dataset**
```bash
# Run the comprehensive data generation script
./run_all.sh

# This creates:
# ✅ 3 Complete Examples (Luxury Auto, Crunchy Snacks, NexBank)
# ✅ 4 Campaign Profiles (High CPM, Mobile, Interactive, Multi-device)
# ✅ Performance data for all campaigns
# ✅ ~12MB SQLite database with realistic Netflix ads data
```

### **4. Individual Commands**
```bash
# Create advertiser
python cli.py create-advertiser --auto

# Create campaign
python cli.py create-campaign --advertiser-id 1 --auto

# Create from profile
python cli.py create-profile --name high_cpm_tv_awareness

# Create from example template
python cli.py create-example --template cli_templates/examples/netflix-ads-examples.yml --example luxury_auto_awareness
```

## 🎯 **Registry Pattern Benefits**

### **Before (Scattered Imports)**
```python
from models.enums import BudgetType, CreativeMimeType
from models.schemas import CreativeCreate
from models.orm import Advertiser, Campaign

# Usage scattered throughout code
BudgetType.lifetime.value
CreativeCreate(...)
Advertiser(...)
```

### **After (Unified Registry)**
```python
from models.registry import registry

# Everything through one interface
registry.BudgetType.lifetime.value
registry.CreativeCreate(...)
registry.Advertiser(...)
```

### **Key Advantages**
- **🔄 Single Source of Truth** - All domain components in one place
- **🔧 Easy Maintenance** - Change enums/schemas, affects everything automatically
- **🧹 Clean Imports** - One import statement instead of multiple
- **📈 Future-Proof** - Easy to add new properties or change implementations
- **🧪 Better Testing** - Centralized access makes mocking and testing easier

## 📊 **Data Generation Capabilities**

### **Complete Examples**
- **Luxury Auto Awareness** - High-budget TV campaigns with premium targeting
- **Crunchy Snacks Consideration** - Mobile-focused campaigns with broad reach
- **NexBank Conversion** - Performance-driven campaigns with interactive elements

### **Campaign Profiles**
- **High CPM TV Awareness** - Premium content, large budgets, TV targeting
- **Mobile Consideration** - Mobile-first, comedy/reality content, short duration
- **Conversion Interactive** - Interactive elements, QR codes, business targeting
- **Multi-Device Advanced** - Cross-platform campaigns with advanced targeting

### **Performance Data**
- **Hourly Metrics** - Impressions, clicks, conversions, spend
- **Realistic Ranges** - Based on industry benchmarks and Netflix data
- **Extended Metrics** - Viewability, completion rates, engagement metrics

## 🧪 **Testing & Quality**

### **Test Coverage (18 Tests)**
```bash
make test  # Run all tests
make test-one FILE=tests/test_flows_v1.py  # Run specific test file
```

**Test Categories:**
- **CLI & Configuration** - Command execution, environment overrides
- **Data Flows** - End-to-end advertiser and campaign creation
- **ORM Persistence** - Database operations and constraints
- **Schema Validation** - Pydantic schemas and data integrity
- **Performance Metrics** - Data generation and realistic ranges
- **Targeting & Formats** - Ad formats and targeting validation

### **Quality Assurance**
- **Type Hints** - Full type annotation throughout
- **Pydantic Validation** - Runtime data validation
- **SQLAlchemy Constraints** - Database-level integrity
- **Comprehensive Testing** - 100% test coverage of core functionality

## 🔧 **Development & Customization**

### **Adding New Enums**
```python
# 1. Add to models/enums.py
class NewEnum(Enum):
    VALUE1 = "VALUE1"
    VALUE2 = "VALUE2"

# 2. Add to models/registry.py EnumRegistry
NewEnum = NewEnum

# 3. Add direct access property (optional)
@property
def NewEnum(self):
    return self.enums.NewEnum
```

### **Adding New Models**
```python
# 1. Add to models/orm.py
class NewModel(EntityBase):
    # ... model definition

# 2. Add to models/registry.py ORMRegistry
NewModel = NewModel

# 3. Add direct access property
@property
def NewModel(self):
    return self.orm.NewModel
```

### **Creating New Profiles**
```python
# Add to cli_templates/profiles/
new_profile:
  name: "New Profile"
  objective: "AWARENESS"
  # ... other configuration
```

## 📈 **Performance & Scalability**

- **Database Size** - ~12MB for complete dataset
- **Generation Speed** - Complete dataset in ~15 seconds
- **Memory Usage** - Efficient streaming for large datasets
- **Scalability** - Easy to extend for more campaigns and data

## 🚀 **Future Enhancements**

- **🎯 Advanced Targeting** - More sophisticated targeting algorithms
- **📊 Real-time Metrics** - Live performance data simulation
- **🌐 Multi-platform** - Support for other streaming platforms
- **🤖 AI Integration** - ML-powered content and targeting optimization
- **📱 Mobile App** - Native mobile interface for data management
- **☁️ Cloud Deployment** - Docker containers and cloud deployment

## 🤝 **Contributing**

1. **Fork** the repository
2. **Create** a feature branch
3. **Follow** the registry pattern for new components
4. **Add tests** for new functionality
5. **Submit** a pull request

## 📄 **License**

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎉 **Acknowledgments**

- **Netflix** for the streaming platform inspiration
- **SQLAlchemy** team for the excellent ORM
- **Pydantic** team for data validation
- **Faker** team for realistic data generation

---

**Ready to generate Netflix ads data?** 🚀

```bash
./run_all.sh  # Generate complete dataset
```

**Questions or issues?** Check the tests or open an issue!
