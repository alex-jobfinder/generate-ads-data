#!/usr/bin/env python3
"""
🎯 ADVERTISER DEMO SCRIPT - Netflix Ads Data Generator Features
==============================================================

📚 LEARNING GUIDE FOR BEGINNERS:
This script demonstrates how to use Python to automate advertising campaigns.
Think of it like a recipe that shows you how to cook different dishes (campaigns)
using the same kitchen (CLI commands).

🏗️ ARCHITECTURE OVERVIEW:
┌─────────────────────────────────────────────────────────────┐
│                    MAIN SCRIPT                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                main()                               │   │
│  │  ┌─────────────────────────────────────────────┐   │   │
│  │  │  demo_campaign_creation()                   │   │   │
│  │  │  demo_performance_analysis()                │   │   │
│  │  │  demo_budget_optimization()                 │   │   │
│  │  │  demo_creative_testing()                    │   │   │
│  │  │  demo_forecasting()                         │   │   │
│  │  │  demo_export_features()                     │   │   │
│  │  └─────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            run_command()                            │   │
│  │  (Helper function used by all demos)               │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

🎯 WHAT THIS SCRIPT DOES:
- Campaign creation and management (like setting up different types of ads)
- Performance analysis and comparison (like checking which ads work best)
- Budget optimization (like finding the best way to spend your money)
- Creative testing scenarios (like trying different ad designs)

🔧 KEY CONCEPTS FOR BEGINNERS:
1. FUNCTIONS: Reusable blocks of code that do specific tasks
2. COMMAND LINE: Text-based interface to run programs
3. ERROR HANDLING: What to do when things go wrong
4. FILE I/O: Reading from and writing to files
5. MODULAR DESIGN: Breaking big tasks into smaller, manageable pieces
"""

# 📦 IMPORT STATEMENTS - Bringing in tools we need
# ================================================
# Think of imports like getting ingredients from the pantry before cooking

import json          # 📄 For handling JSON data (like reading/writing structured data)
import subprocess    # 🔧 For running command-line programs from Python
import sys           # 🖥️  For system-specific functions (like exiting the program)
import datetime      # 📅 For working with dates and times
from typing import Dict, Any  # 🏷️  For type hints (telling Python what kind of data we expect)

def run_command(cmd: str, description: str) -> Dict[str, Any]:
    """
    🔧 HELPER FUNCTION: Execute Command Line Commands
    
    📖 WHAT IT DOES:
    This function is like a universal remote control that can run any command
    on your computer's command line (terminal) and tell you what happened.
    
    🔄 VISUAL FLOW:
    ┌─────────────────────────────────────────────────────────────┐
    │                    run_command()                            │
    │                                                             │
    │  Input: "python cli.py status"                             │
    │         ↓                                                   │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │  subprocess.run() - Runs the command               │   │
    │  │                                                     │   │
    │  │  ┌─────────────────┐    ┌─────────────────────────┐ │   │
    │  │  │   SUCCESS       │    │      FAILURE            │ │   │
    │  │  │                 │    │                         │ │   │
    │  │  │ ✅ Print Success│    │ ❌ Print Error          │ │   │
    │  │  │ 📝 Log to File  │    │ 📝 Log Error to File    │ │   │
    │  │  │ 🔄 Return Result│    │ 🔄 Return Error Info    │ │   │
    │  │  └─────────────────┘    └─────────────────────────┘ │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │  Output: {"success": True/False, "output": "...", ...}     │
    └─────────────────────────────────────────────────────────────┘
    
    📝 PARAMETERS:
    - cmd (str): The command to run (like "python cli.py status")
    - description (str): Human-readable description of what we're doing
    
    🔄 RETURNS:
    Dictionary with success status, output, and any errors
    
    💡 LEARNING NOTES:
    - subprocess.run() is how Python talks to your computer's command line
    - try/except is how we handle errors gracefully
    - File I/O (with open()) lets us save results for later review
    """
    print(f"\n🔄 {description}")
    print(f"Command: {cmd}")
    
    try:
        # 🚀 EXECUTE THE COMMAND
        # subprocess.run() is like typing the command in your terminal
        result = subprocess.run(cmd.split(), capture_output=True, text=True, check=True)
        print("✅ Success!")
        
        # 📝 LOG SUCCESS TO FILE
        # This creates a permanent record of what happened
        with open("advertiser_demo_output.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"🔄 {description}\n")
            f.write(f"Command: {cmd}\n")
            f.write(f"✅ Success!\n")
            f.write(f"Output:\n{result.stdout}\n")
            f.write(f"{'='*80}\n")
        
        return {"success": True, "output": result.stdout, "error": None}
        
    except subprocess.CalledProcessError as e:
        # ❌ HANDLE ERRORS GRACEFULLY
        # If the command fails, we don't want the whole program to crash
        print(f"❌ Error: {e}")
        
        # 📝 LOG ERROR TO FILE
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
    """
    🎯 DEMO 1: Campaign Creation & Management
    
    📖 WHAT IT DOES:
    Shows how to create different types of advertising campaigns.
    Think of this like setting up different types of stores in a mall.
    
    🏪 CAMPAIGN TYPES WE'LL CREATE:
    ┌─────────────────────────────────────────────────────────────┐
    │                    CAMPAIGN TYPES                           │
    │                                                             │
    │  🚗 AGGRESSIVE CAMPAIGN (High CPM TV Awareness)            │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ • High budget, premium placement                    │   │
    │  │ • Targets luxury car buyers                         │   │
    │  │ • Uses expensive TV time slots                      │   │
    │  │ • Goal: Brand awareness                             │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │  📱 DEFENSIVE CAMPAIGN (Mobile Consideration)              │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ • Lower budget, targeted placement                  │   │
    │  │ • Targets mobile users                              │   │
    │  │ • Uses cost-effective mobile ads                    │   │
    │  │ • Goal: Drive consideration/purchases               │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │  📋 LIST ALL CAMPAIGNS                                     │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ • Shows all campaigns in a nice table format        │   │
    │  │ • Helps you see what you've created                 │   │
    │  └─────────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────┘
    
    💡 LEARNING NOTES:
    - Campaigns are like different strategies for reaching customers
    - Aggressive = spend more money for bigger impact
    - Defensive = spend less money but be more targeted
    - Always list your campaigns to see what you've created
    """
    print("\n" + "="*60)
    print("🎯 DEMO: Campaign Creation & Management")
    print("="*60)
    
    # 🚗 CREATE AGGRESSIVE PROFILE
    # This is like opening a luxury car dealership
    run_command(
        "python cli.py create-profile --name high_cpm_tv_awareness",
        "Creating aggressive luxury auto awareness campaign"
    )
    
    # 📱 CREATE DEFENSIVE PROFILE  
    # This is like opening a mobile phone kiosk
    run_command(
        "python cli.py create-profile --name mobile_consideration",
        "Creating defensive mobile consideration campaign"
    )
    
    # 📋 LIST ALL CAMPAIGNS
    # This is like getting a directory of all your stores
    run_command(
        "python cli.py list-campaigns --format table",
        "Listing all campaigns in table format"
    )

def demo_performance_analysis():
    """
    📊 DEMO 2: Performance Analysis & Comparison
    
    📖 WHAT IT DOES:
    Shows how to analyze how well your campaigns are performing.
    Think of this like checking your store's sales reports.
    
    🔍 ANALYSIS WORKFLOW:
    ┌─────────────────────────────────────────────────────────────┐
    │                PERFORMANCE ANALYSIS                         │
    │                                                             │
    │  🏥 SYSTEM HEALTH CHECK                                    │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ • Check if database is working                      │   │
    │  │ • Verify all systems are online                     │   │
    │  │ • Like checking if your cash register works         │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │  📈 CAMPAIGN COMPARISON                                    │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ • Compare campaigns with same goal (AWARENESS)      │   │
    │  │ • Show top 3 performers                             │   │
    │  │ • Like comparing which stores sell the most         │   │
    │  └─────────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────┘
    
    💡 LEARNING NOTES:
    - Always check system health before analyzing data
    - Compare campaigns with similar objectives for fair comparison
    - Focus on top performers to learn what works
    """
    print("\n" + "="*60)
    print("📊 DEMO: Performance Analysis & Comparison")
    print("="*60)
    
    # 🏥 CHECK SYSTEM STATUS
    # Like checking if your computer and database are working properly
    run_command(
        "python cli.py status",
        "Checking system and database status"
    )
    
    # 📈 COMPARE CAMPAIGNS BY OBJECTIVE
    # Like comparing which stores in your mall are doing best
    run_command(
        "python cli.py compare-by-objective --objective AWARENESS --top-n 3",
        "Comparing awareness campaigns"
    )

def demo_budget_optimization():
    """
    💰 DEMO 3: Budget Optimization & ROI Projection
    
    📖 WHAT IT DOES:
    Shows how to optimize your advertising budget for maximum return.
    Think of this like figuring out how to spend your marketing budget
    to get the most customers.
    
    🎯 OPTIMIZATION STRATEGY:
    ┌─────────────────────────────────────────────────────────────┐
    │                BUDGET OPTIMIZATION                          │
    │                                                             │
    │  💵 BUDGET ALLOCATION                                      │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ $50K AWARENESS CAMPAIGN                             │   │
    │  │ • Optimize for brand visibility                     │   │
    │  │ • Higher CPM for premium placement                  │   │
    │  │ • Like buying billboard space                       │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │  🎯 CONVERSION FOCUS                                       │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ $75K CONVERSION CAMPAIGN                            │   │
    │  │ • Optimize for actual purchases                     │   │
    │  │ • Lower CPM, higher targeting                       │   │
    │  │ • Like targeted online ads                          │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │  🔮 ROI PROJECTION                                         │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ • Predict future returns                            │   │
    │  │ • Multiple scenarios (optimistic, realistic, etc.)  │   │
    │  │ • Like financial forecasting                        │   │
    │  └─────────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────┘
    
    💡 LEARNING NOTES:
    - Different objectives need different budget strategies
    - Awareness = spend more per impression for visibility
    - Conversion = spend less per impression but target better
    - Always project ROI to make informed decisions
    """
    print("\n" + "="*60)
    print("💰 DEMO: Budget Optimization & ROI Projection")
    print("="*60)
    
    # 💵 OPTIMIZE CPM FOR AWARENESS
    # Like buying expensive but visible billboard space
    run_command(
        "python cli.py optimize-cpm --budget 50000 --objective AWARENESS",
        "Optimizing CPM for $50K awareness campaign"
    )
    
    # 🎯 OPTIMIZE CPM FOR CONVERSION
    # Like buying targeted online ads that convert better
    run_command(
        "python cli.py optimize-cpm --budget 75000 --objective CONVERSION",
        "Optimizing CPM for $75K conversion campaign"
    )
    
    # 🔮 PROJECT ROI
    # Like predicting how much money you'll make from your investment
    run_command(
        "python cli.py project-roi --campaign-id 1 --scenarios 3 --optimistic",
        "Projecting ROI for campaign 1 with optimistic scenario"
    )

def demo_creative_testing():
    """
    🎨 DEMO 4: Creative Testing & A/B Testing
    
    📖 WHAT IT DOES:
    Shows how to test different ad designs and strategies to see what works best.
    Think of this like trying different store layouts to see which one
    attracts more customers.
    
    🧪 TESTING METHODOLOGY:
    ┌─────────────────────────────────────────────────────────────┐
    │                CREATIVE TESTING                             │
    │                                                             │
    │  🎬 VIDEO FORMAT TESTING                                   │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ 15-Second Interactive Video                         │   │
    │  │ • Shorter, more engaging                            │   │
    │  │ • Interactive elements                              │   │
    │  │ • Like a quick, fun commercial                      │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │  📺 STANDARD VIDEO TESTING                                 │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ 30-Second Standard Video                            │   │
    │  │ • Traditional format                                │   │
    │  │ • More time for storytelling                        │   │
    │  │ • Like a traditional TV commercial                  │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │  🔬 A/B TESTING                                            │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ Mobile Only vs Multi-Device                         │   │
    │  │ • Test different targeting strategies               │   │
    │  │ • 14-day test duration                              │   │
    │  │ • Like testing store location A vs location B       │   │
    │  └─────────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────┘
    
    💡 LEARNING NOTES:
    - Always test different creative formats
    - Shorter videos can be more engaging
    - A/B testing helps you make data-driven decisions
    - Test duration should be long enough for statistical significance
    """
    print("\n" + "="*60)
    print("🎨 DEMO: Creative Testing & A/B Testing")
    print("="*60)
    
    # 🎬 TEST INTERACTIVE VIDEO
    # Like testing a fun, engaging commercial
    run_command(
        "python cli.py test-creative --format STANDARD_VIDEO --duration 15 --interactive",
        "Testing 15-second interactive video creative"
    )
    
    # 📺 TEST STANDARD VIDEO
    # Like testing a traditional commercial
    run_command(
        "python cli.py test-creative --format STANDARD_VIDEO --duration 30",
        "Testing 30-second standard video creative"
    )
    
    # 🔬 SET UP A/B TEST
    # Like testing two different store layouts
    run_command(
        "python cli.py ab-test --variant-a mobile_only --variant-b multi_device --test-duration 14",
        "Setting up A/B test: mobile vs multi-device targeting"
    )

def demo_forecasting():
    """
    🔮 DEMO 5: Performance Forecasting & Trends
    
    📖 WHAT IT DOES:
    Shows how to predict future campaign performance based on historical data.
    Think of this like weather forecasting, but for your advertising campaigns.
    
    📈 FORECASTING WORKFLOW:
    ┌─────────────────────────────────────────────────────────────┐
    │                PERFORMANCE FORECASTING                      │
    │                                                             │
    │  🔮 30-DAY FORECAST                                        │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ • Predict next 30 days of performance               │   │
    │  │ • Include seasonal adjustments                      │   │
    │  │ • Like predicting next month's sales                │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │  📊 SEASONAL TREND ANALYSIS                                │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ • Analyze 90-day seasonal patterns                  │   │
    │  │ • Identify peak and low periods                     │   │
    │  │ • Like understanding holiday shopping patterns      │   │
    │  └─────────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────┘
    
    💡 LEARNING NOTES:
    - Forecasting helps with budget planning
    - Seasonal adjustments account for time-based patterns
    - Longer trend analysis gives better insights
    - Use forecasts to optimize campaign timing
    """
    print("\n" + "="*60)
    print("🔮 DEMO: Performance Forecasting & Trends")
    print("="*60)
    
    # 🔮 FORECAST PERFORMANCE
    # Like predicting next month's weather
    run_command(
        "python cli.py forecast --campaign-id 1 --days 30 --include-seasonal",
        "Forecasting 30-day performance with seasonal adjustments"
    )
    
    # 📊 ANALYZE SEASONAL TRENDS
    # Like understanding holiday shopping patterns
    run_command(
        "python cli.py seasonal-trends --campaign-id 1 --period 90",
        "Analyzing 90-day seasonal trends for campaign 1"
    )

def demo_export_features():
    """
    📤 DEMO 6: Data Export & Reporting
    
    📖 WHAT IT DOES:
    Shows how to export campaign data for external analysis and reporting.
    Think of this like creating reports for your boss or saving data
    for later analysis in Excel or other tools.
    
    📊 EXPORT WORKFLOW:
    ┌─────────────────────────────────────────────────────────────┐
    │                DATA EXPORT & REPORTING                      │
    │                                                             │
    │  📄 JSON EXPORT                                            │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ • Export campaign data in JSON format               │   │
    │  │ • Include performance metrics                       │   │
    │  │ • Like saving data for programmers                  │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │  📊 CSV EXPORT                                             │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ • Export campaign list in CSV format                │   │
    │  │ • Easy to open in Excel or Google Sheets            │   │
    │  │ • Like creating a spreadsheet for your boss         │   │
    │  └─────────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────┘
    
    💡 LEARNING NOTES:
    - JSON is good for programmers and APIs
    - CSV is good for spreadsheets and business users
    - Always include performance data in exports
    - Export data regularly for backup and analysis
    """
    print("\n" + "="*60)
    print("📤 DEMO: Data Export & Reporting")
    print("="*60)
    
    # 📄 EXPORT CAMPAIGN DATA
    # Like creating a detailed report for your boss
    run_command(
        "python cli.py export-campaign --id 1 --format json --include-performance",
        "Exporting campaign 1 data in JSON format with performance"
    )
    
    # 📊 EXPORT CAMPAIGN LIST
    # Like creating a simple spreadsheet
    run_command(
        "python cli.py list-campaigns --format csv",
        "Exporting campaign list in CSV format"
    )

def main():
    """
    🎭 MAIN FUNCTION: The Master Controller
    
    📖 WHAT IT DOES:
    This is the main function that orchestrates the entire demo.
    Think of it like a conductor leading an orchestra - it coordinates
    all the different sections to create a beautiful performance.
    
    🎬 DEMO ORCHESTRATION:
    ┌─────────────────────────────────────────────────────────────┐
    │                    MAIN FUNCTION                            │
    │                                                             │
    │  🎬 SETUP PHASE                                            │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ • Print welcome message                             │   │
    │  │ • Create output file for logging                    │   │
    │  │ • Like setting up the stage before a show           │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │  🎭 DEMO EXECUTION                                         │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ 1. demo_campaign_creation()                         │   │
    │  │ 2. demo_performance_analysis()                      │   │
    │  │ 3. demo_budget_optimization()                       │   │
    │  │ 4. demo_creative_testing()                          │   │
    │  │ 5. demo_forecasting()                               │   │
    │  │ 6. demo_export_features()                           │   │
    │  │ • Like running through all the acts of a play       │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │  🎉 WRAP-UP PHASE                                          │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ • Print completion summary                           │   │
    │  │ • Save final results to file                        │   │
    │  │ • Like taking a bow at the end of the show          │   │
    │  └─────────────────────────────────────────────────────┘   │
    │                                                             │
    │  🛡️ ERROR HANDLING                                         │
    │  ┌─────────────────────────────────────────────────────┐   │
    │  │ • Handle user interruption (Ctrl+C)                 │   │
    │  │ • Handle unexpected errors                          │   │
    │  │ • Like having a safety net during the performance   │   │
    │  └─────────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────┘
    
    💡 LEARNING NOTES:
    - Main functions coordinate all other functions
    - Always handle errors gracefully
    - Log everything for debugging and review
    - Provide clear feedback to users
    """
    print("🎯 Netflix Ads Data Generator - Advertiser Demo")
    print("="*60)
    print("This demo showcases all the advertiser-centric features")
    print("including campaign creation, analysis, optimization, and testing.")
    print("="*60)
    
    # 📝 SETUP OUTPUT FILE
    # Create a log file to record everything that happens
    with open("advertiser_demo_output.txt", "w", encoding="utf-8") as f:
        f.write("🎯 Netflix Ads Data Generator - Advertiser Demo Output\n")
        f.write("="*80 + "\n")
        f.write("This file contains the complete output from all demo commands\n")
        f.write("Generated on: " + str(datetime.datetime.now()) + "\n")
        f.write("="*80 + "\n\n")
    
    try:
        # 🎭 RUN ALL DEMO SECTIONS
        # Execute each demo in sequence
        demo_campaign_creation()      # Create different campaign types
        demo_performance_analysis()   # Analyze how campaigns are doing
        demo_budget_optimization()    # Optimize spending for best results
        demo_creative_testing()       # Test different ad designs
        demo_forecasting()            # Predict future performance
        demo_export_features()        # Export data for external use
        
        # 🎉 DEMO COMPLETION
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
        
        # 📝 SAVE FINAL SUMMARY
        # Append the completion summary to our log file
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
        # ⏹️ USER INTERRUPTION
        # Handle when user presses Ctrl+C to stop the demo
        print("\n\n⏹️ Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        # ❌ UNEXPECTED ERROR
        # Handle any other errors that might occur
        print(f"\n\n❌ Demo failed with error: {e}")
        sys.exit(1)

# 🚀 PROGRAM ENTRY POINT
# ======================
# This is where Python starts executing the program
# Think of it like the "Start" button on a machine

if __name__ == "__main__":
    """
    🎯 PROGRAM ENTRY POINT
    
    📖 WHAT THIS DOES:
    This special Python construct ensures that main() only runs when
    the script is executed directly (not when imported as a module).
    
    🔍 HOW IT WORKS:
    - When you run: python advertiser_demo_README.py
    - Python sets __name__ to "__main__"
    - This triggers the main() function to run
    
    💡 LEARNING NOTES:
    - This is a Python best practice
    - Allows the script to be both runnable and importable
    - Prevents accidental execution when importing
    """
    main()
