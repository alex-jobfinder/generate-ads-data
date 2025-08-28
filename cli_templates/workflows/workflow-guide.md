# Netflix Ads Data Modeling - Complete Workflow Guide

This directory contains **workflow templates and guides** for the streamlined Netflix ads data generation system.

## **What's Here**

### **Core Workflows**
- `field-testing-template.yml` - Test specific fields with auto-generated context
- `database-schema-reference.yml` - Complete database schema with DDL and constraints

### **Documentation**
- `workflow-guide.md` - **This file** - Complete workflow documentation
- `designs.md` - Design approaches and implementation strategies

## **Workflow Types**

### **1. Complete Examples Workflow**
```bash
# Generate complete Netflix ads example with performance data
python cli.py create-example --template examples/netflix-ads-examples.yml --example luxury_auto_awareness
```

**What it does:**
- Creates complete entity hierarchy (advertiser → campaign → line items → creatives)
- Uses smart defaults for missing fields
- Generates performance data automatically
- Returns complete example ready for database modeling

### **2. Field Testing Workflow**
```bash
# Test specific fields while auto-generating realistic context
python cli.py test-fields --template workflows/field-testing-template.yml --focus "campaign.target_cpm,line_items.targeting_json"
```

**What it does:**
- Uses your test field values
- Generates realistic context with faker
- Creates complete Netflix ads example
- Generates performance data
- Focuses on your specific test fields

### **3. Profile-Based Workflow**
```bash
# Use pre-built profiles for common testing scenarios
python cli.py create-profile --name high_cpm_tv_awareness --test-fields "campaign.target_cpm=2000"
```

**What it does:**
- Uses pre-built profile with smart defaults
- Applies your test field overrides
- Auto-generates missing data with faker
- Creates complete example with performance data

## **Template Structure**

### **Examples Template** (`examples/netflix-ads-examples.yml`)
```yaml
examples:
  [example_name]:
    description: "What this example demonstrates"
    strategy: "Campaign strategy notes"
    results: "Expected results"
    
    advertiser: {...}
    campaign: {...}
    line_items: [...]
    performance: {...}
```

### **Field Testing Template** (`workflows/field-testing-template.yml`)
```yaml
test_scenario: "Description of what you're testing"

test_fields:
  campaign: {...}
  line_items: [...]
  creatives: [...]

auto_generate: {...}
smart_defaults: {...}
faker_config: {...}
performance: {...}
```

### **Campaign Profiles Template** (`profiles/campaign-profiles.yml`)
```yaml
profiles:
  [profile_name]:
    description: "Profile description"
    base_template: "base_template_name"
    focus: "Fields this profile focuses on"
    
    test_values: {...}
    faker_auto: [...]
    performance: {...}

base_templates:
  [base_name]: {...}
```

## **Migration from Old Commands**

### **Old Workflow (4+ commands):**
```bash
# 1. Create advertiser
python cli.py create-advertiser --auto

# 2. Create campaign
python cli.py create-campaign --advertiser-id 1 --auto --profile AWARENESS

# 3. Generate performance
python cli.py generate-performance --campaign-id 1 --replace

# 4. Generate extended performance
python cli.py generate-performance-ext --campaign-id 1 --replace
```

### **New Workflow (1 command):**
```bash
# Single command creates everything
python cli.py create-example --template examples/netflix-ads-examples.yml --example luxury_auto_awareness

# Or test specific fields
python cli.py test-fields --template workflows/field-testing-template.yml --focus "campaign.target_cpm"
```

## **Benefits of New Approach**

1. **Single command** instead of 4+ commands
2. **Smart defaults** ensure realistic Netflix ads data
3. **Automatic faker generation** fills in missing pieces
4. **Field-specific testing** without rebuilding everything
5. **Template-driven** for consistency and reusability
6. **Auto-performance** generation when examples are complete
7. **Realistic context** around your test fields

## **Use Cases**

### **Database Modeling**
- Generate realistic Netflix ads data examples
- Test different campaign configurations
- Understand entity relationships
- Model performance patterns

### **Testing & Development**
- Test specific field variations
- Validate data constraints
- Test performance generation
- Debug entity relationships

### **Documentation & Examples**
- Create consistent examples
- Document best practices
- Share campaign patterns
- Train team members

## **Quick Start**

### **1. Create Complete Example**
```bash
python cli.py create-example --template examples/netflix-ads-examples.yml --example luxury_auto_awareness
```

### **2. Test Specific Fields**
```bash
python cli.py test-fields --template workflows/field-testing-template.yml --focus "campaign.target_cpm"
```

### **3. Use Pre-built Profile**
```bash
python cli.py create-profile --name high_cpm_tv_awareness
```

## **Next Steps**

1. **Try the examples**: Start with `luxury_auto_awareness`
2. **Test specific fields**: Use field testing template
3. **Create custom profiles**: Build your own testing scenarios
4. **Extend templates**: Add more examples and patterns

This streamlined approach gives you **realistic Netflix ads data examples** quickly for database modeling, with the ability to test specific fields while everything else is automatically generated with smart defaults and faker data.
