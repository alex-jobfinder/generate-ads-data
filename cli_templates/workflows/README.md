# Workflows Directory

This directory contains **workflow templates and guides** for the streamlined Netflix ads data generation system.

## **What's Here**

### **Core Workflows**
- `field-testing-template.yml` - Test specific fields with auto-generated context
- `database-schema-reference.yml` - Complete database schema with DDL and constraints

### **Documentation**
- `workflow-guide.md` - Complete workflow documentation and examples
- `designs.md` - Design approaches and implementation strategies

## **Workflow Types**

### **1. Field Testing Workflow**
```bash
# Test specific fields while auto-generating realistic context
python cli.py test-fields --template workflows/field-testing-template.yml --focus "campaign.target_cpm,line_items.targeting_json"
```

**Perfect for:**
- Testing different CPM values
- Testing targeting variations
- Testing creative specifications
- Testing budget scenarios

### **2. Database Schema Reference**
Use `database-schema-reference.yml` to understand:
- Table structures and relationships
- Valid enum values and constraints
- Field types and requirements
- Database DDL for reference

## **Field Testing Template Structure**

```yaml
test_scenario: "Test higher CPM and targeting variations for luxury auto awareness"

test_fields:
  campaign:
    target_cpm: 20.00              # Test: Higher CPM than default
    budget: 150000.00                # Test: Larger budget than default
  
  line_items:
    - targeting_json: '{"DEVICE": ["TV"], "CONTENT_GENRE": ["DRAMA", "DOCUMENTARY", "ACTION"]}'

auto_generate:
  advertiser: true                       # Generate realistic advertiser
  campaign_completion: true              # Complete campaign with best practices
  line_item_completion: true             # Complete line items with defaults
  creative_generation: true              # Generate realistic creatives
  performance_data: true                 # Generate performance metrics

smart_defaults:
  advertiser:
    pattern: "luxury_auto"               # Use Luxury Auto Co naming pattern
    industry: "automotive"               # Generate realistic auto industry data
```

## **When to Use**

### **Field Testing Workflow**
Use when you need to:
- **Test specific field variations** without rebuilding everything
- **Validate data constraints** for particular scenarios
- **Debug field-specific issues** with realistic context
- **Experiment with different values** while keeping context

### **Database Schema Reference**
Use when you need to:
- **Understand valid field values** and constraints
- **Reference table structures** and relationships
- **Validate template data** against schema requirements
- **Debug data type issues** and field requirements

## **Benefits**

✅ **Field-specific testing** without rebuilding everything  
✅ **Realistic context** around your test fields  
✅ **Automatic generation** of missing data with faker  
✅ **Smart defaults** based on Netflix ads best practices  
✅ **Schema validation** and constraint checking  
✅ **Consistent patterns** across all workflows  

## **Next Steps**

1. **Try field testing**: Test specific CPM or targeting variations
2. **Reference schema**: Use database schema for validation
3. **Customize workflows**: Adapt templates for your specific needs
4. **Extend patterns**: Create new workflow templates

This workflow approach gives you **targeted testing capabilities** while maintaining realistic Netflix ads data context for effective database modeling and development.
