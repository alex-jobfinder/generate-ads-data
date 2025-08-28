#!/bin/bash

# Run All Netflix Ads Examples - Shell Script Version
# This script creates all examples and profiles to generate comprehensive Netflix ads data

echo "🚀 Starting Netflix Ads Data Generation - All Examples"
echo "============================================================"

# Function to run command and show result
run_cmd() {
    local description="$1"
    local cmd="$2"
    
    echo ""
    echo "🔄 $description"
    echo "Command: $cmd"
    
    if eval "$cmd"; then
        echo "✅ Success: $description"
    else
        echo "❌ Error: $description"
    fi
    
    echo "---"
    sleep 1
}

# Step 1: Create all examples
echo ""
echo "📊 STEP 1: Creating Complete Examples"
echo "----------------------------------------"

run_cmd "Creating luxury_auto_awareness example" \
    "python cli.py create-example --template cli_templates/examples/netflix-ads-examples.yml --example luxury_auto_awareness"

run_cmd "Creating crunchy_snacks_consideration example" \
    "python cli.py create-example --template cli_templates/examples/netflix-ads-examples.yml --example crunchy_snacks_consideration"

run_cmd "Creating nexbank_conversion example" \
    "python cli.py create-example --template cli_templates/examples/netflix-ads-examples.yml --example nexbank_conversion"

# Step 2: Create all profiles
echo ""
echo "📊 STEP 2: Creating Campaign Profiles"
echo "----------------------------------------"

run_cmd "Creating high_cpm_tv_awareness profile" \
    "python cli.py create-profile --name high_cpm_tv_awareness"

run_cmd "Creating mobile_consideration profile" \
    "python cli.py create-profile --name mobile_consideration"

run_cmd "Creating conversion_interactive profile" \
    "python cli.py create-profile --name conversion_interactive"

run_cmd "Creating multi_device_advanced profile" \
    "python cli.py create-profile --name multi_device_advanced"

# Step 3: Summary
echo ""
echo "📊 STEP 3: Generation Summary"
echo "----------------------------------------"
echo "✅ All examples and profiles processed!"
echo "📁 Total Examples: 3"
echo "📁 Total Profiles: 4"

# Step 4: Database check
echo ""
echo "📊 STEP 4: Database Status Check"
echo "----------------------------------------"
if [ -f "ads.db" ]; then
    size=$(du -h ads.db | cut -f1)
    echo "📊 Database: ads.db ($size)"
    echo "📊 Database contains generated Netflix ads data"
else
    echo "❌ Database: ads.db not found"
fi

echo ""
echo "🎉 Netflix Ads Data Generation Complete!"
echo "============================================================"
echo ""
echo "🎯 What was created:"
echo "   • 3 Complete Examples (Luxury Auto, Crunchy Snacks, NexBank)"
echo "   • 4 Campaign Profiles (High CPM, Mobile, Interactive, Multi-device)"
echo "   • Performance data for all campaigns"
echo "   • Realistic Netflix ads data for database modeling"
echo ""
echo "📊 Check ads.db for all generated data!"
