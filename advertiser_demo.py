#!/usr/bin/env python3
"""
Advertiser Demo Script - Showcases Netflix Ads Data Generator Features

This script demonstrates the key advertiser features:
- Campaign creation and management
- Performance analysis and comparison
- Budget optimization
- Creative testing scenarios
"""

import json
import subprocess
import sys
import datetime
from typing import Dict, Any

def run_command(cmd: str, description: str) -> Dict[str, Any]:
    """Run a CLI command and return the result."""
    print(f"\n🔄 {description}")
    print(f"Command: {cmd}")
    
    try:
        result = subprocess.run(cmd.split(), capture_output=True, text=True, check=True)
        print("✅ Success!")
        
        # Append output to file
        with open("advertiser_demo_output.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"🔄 {description}\n")
            f.write(f"Command: {cmd}\n")
            f.write(f"✅ Success!\n")
            f.write(f"Output:\n{result.stdout}\n")
            f.write(f"{'='*80}\n")
        
        return {"success": True, "output": result.stdout, "error": None}
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        
        # Append error to file
        with open("advertiser_demo_output.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"🔄 {description}\n")
            f.write(f"Command: {cmd}\n")
            f.write(f"❌ Error: {e}\n")
            if e.stdout:
                f.write(f"STDOUT: {e.stdout}\n")
            if e.stderr:
                f.write(f"STDERR: {e.stderr}\n")
            f.write(f"{'='*80}\n")
        
        return {"success": False, "output": e.stdout, "error": e.stderr}

def demo_campaign_creation():
    """Demonstrate campaign creation with different profiles."""
    print("\n" + "="*60)
    print("🎯 DEMO: Campaign Creation & Management")
    print("="*60)
    
    # Create aggressive profile
    run_command(
        "python cli.py create-profile --name high_cpm_tv_awareness",
        "Creating aggressive luxury auto awareness campaign"
    )
    
    # Create defensive profile
    run_command(
        "python cli.py create-profile --name mobile_consideration",
        "Creating defensive mobile consideration campaign"
    )
    
    # List all campaigns
    run_command(
        "python cli.py list-campaigns --format table",
        "Listing all campaigns in table format"
    )

def demo_performance_analysis():
    """Demonstrate performance analysis features."""
    print("\n" + "="*60)
    print("📊 DEMO: Performance Analysis & Comparison")
    print("="*60)
    
    # Check system status
    run_command(
        "python cli.py status",
        "Checking system and database status"
    )
    
    # Compare campaigns by objective
    run_command(
        "python cli.py compare-by-objective --objective AWARENESS --top-n 3",
        "Comparing awareness campaigns"
    )

def demo_budget_optimization():
    """Demonstrate budget optimization features."""
    print("\n" + "="*60)
    print("💰 DEMO: Budget Optimization & ROI Projection")
    print("="*60)
    
    # Optimize CPM for different objectives
    run_command(
        "python cli.py optimize-cpm --budget 50000 --objective AWARENESS",
        "Optimizing CPM for $50K awareness campaign"
    )
    
    run_command(
        "python cli.py optimize-cpm --budget 75000 --objective CONVERSION",
        "Optimizing CPM for $75K conversion campaign"
    )
    
    # Project ROI (assuming campaign ID 1 exists)
    run_command(
        "python cli.py project-roi --campaign-id 1 --scenarios 3 --optimistic",
        "Projecting ROI for campaign 1 with optimistic scenario"
    )

def demo_creative_testing():
    """Demonstrate creative testing features."""
    print("\n" + "="*60)
    print("🎨 DEMO: Creative Testing & A/B Testing")
    print("="*60)
    
    # Test different creative formats
    run_command(
        "python cli.py test-creative --format STANDARD_VIDEO --duration 15 --interactive",
        "Testing 15-second interactive video creative"
    )
    
    run_command(
        "python cli.py test-creative --format STANDARD_VIDEO --duration 30",
        "Testing 30-second standard video creative"
    )
    
    # Set up A/B testing
    run_command(
        "python cli.py ab-test --variant-a mobile_only --variant-b multi_device --test-duration 14",
        "Setting up A/B test: mobile vs multi-device targeting"
    )

def demo_forecasting():
    """Demonstrate forecasting and trend analysis."""
    print("\n" + "="*60)
    print("🔮 DEMO: Performance Forecasting & Trends")
    print("="*60)
    
    # Forecast performance (assuming campaign ID 1 exists)
    run_command(
        "python cli.py forecast --campaign-id 1 --days 30 --include-seasonal",
        "Forecasting 30-day performance with seasonal adjustments"
    )
    
    # Analyze seasonal trends
    run_command(
        "python cli.py seasonal-trends --campaign-id 1 --period 90",
        "Analyzing 90-day seasonal trends for campaign 1"
    )

def demo_export_features():
    """Demonstrate data export features."""
    print("\n" + "="*60)
    print("📤 DEMO: Data Export & Reporting")
    print("="*60)
    
    # Export campaign data (assuming campaign ID 1 exists)
    run_command(
        "python cli.py export-campaign --id 1 --format json --include-performance",
        "Exporting campaign 1 data in JSON format with performance"
    )
    
    # List campaigns in CSV format
    run_command(
        "python cli.py list-campaigns --format csv",
        "Exporting campaign list in CSV format"
    )

def main():
    """Run the complete advertiser demo."""
    print("🎯 Netflix Ads Data Generator - Advertiser Demo")
    print("="*60)
    print("This demo showcases all the advertiser-centric features")
    print("including campaign creation, analysis, optimization, and testing.")
    print("="*60)
    
    # Clear/create the output file
    with open("advertiser_demo_output.txt", "w", encoding="utf-8") as f:
        f.write("🎯 Netflix Ads Data Generator - Advertiser Demo Output\n")
        f.write("="*80 + "\n")
        f.write("This file contains the complete output from all demo commands\n")
        f.write("Generated on: " + str(datetime.datetime.now()) + "\n")
        f.write("="*80 + "\n\n")
    
    try:
        # Run all demo sections
        demo_campaign_creation()
        demo_performance_analysis()
        demo_budget_optimization()
        demo_creative_testing()
        demo_forecasting()
        demo_export_features()
        
        print("\n" + "="*60)
        print("🎉 DEMO COMPLETE!")
        print("="*60)
        print("You've now seen all the key advertiser features:")
        print("✅ Campaign creation with aggressive/defensive profiles")
        print("✅ Performance analysis and comparison")
        print("✅ Budget optimization and ROI projection")
        print("✅ Creative testing and A/B testing")
        print("✅ Performance forecasting and trend analysis")
        print("✅ Data export and reporting")
        print("\nNext steps:")
        print("1. Run './run_all.sh' to create comprehensive test data")
        print("2. Experiment with different campaign profiles")
        print("3. Use the CLI commands to analyze and optimize campaigns")
        print("4. Export data for external analysis tools")
        
        # Append summary to output file
        with open("advertiser_demo_output.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{'='*80}\n")
            f.write("🎉 DEMO COMPLETE!\n")
            f.write("="*80 + "\n")
            f.write("You've now seen all the key advertiser features:\n")
            f.write("✅ Campaign creation with aggressive/defensive profiles\n")
            f.write("✅ Performance analysis and comparison\n")
            f.write("✅ Budget optimization and ROI projection\n")
            f.write("✅ Creative testing and A/B testing\n")
            f.write("✅ Performance forecasting and trend analysis\n")
            f.write("✅ Data export and reporting\n")
            f.write(f"\nDemo completed at: {datetime.datetime.now()}\n")
            f.write(f"{'='*80}\n")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
