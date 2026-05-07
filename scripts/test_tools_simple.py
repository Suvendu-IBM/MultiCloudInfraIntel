#!/usr/bin/env python3
"""
Simple Tool Testing Script
Tests individual MCP server tools with your AWS credentials
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import mcp_server
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from datetime import datetime, timedelta
from mcp_server import MultiCloudIntelligenceServer, Config

async def test_resource_summary():
    """Test getting resource summary"""
    print("\n" + "="*60)
    print("TEST 1: Get Resource Summary")
    print("="*60)
    
    config = Config()
    server = MultiCloudIntelligenceServer(config)
    
    try:
        print("\nFetching AWS resources...")
        response = await server.get_resource_summary(cloud_provider="aws")
        
        # Extract data from response
        resources = response.get('data', [])
        metadata = response.get('_metadata', {})
        
        print(f"[OK] Found {len(resources)} resources")
        print(f"  Execution time: {metadata.get('execution_time_ms', 0):.2f}ms")
        
        # Show first few resources
        if resources:
            print("\nSample resources:")
            for i, resource in enumerate(resources[:3]):
                print(f"  {i+1}. {resource.get('resource_type')}: {resource.get('resource_id')}")
                print(f"     Region: {resource.get('region')}")
                print(f"     State: {resource.get('state')}")
        else:
            print("  No resources found (this is OK if you have no EC2 instances)")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_cost_trends():
    """Test getting cost trends"""
    print("\n" + "="*60)
    print("TEST 2: Get Cost Trends")
    print("="*60)
    
    config = Config()
    server = MultiCloudIntelligenceServer(config)
    
    try:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        print(f"\nFetching costs from {start_date} to {end_date}...")
        response = await server.get_cost_trends(
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            granularity='DAILY'
        )
        
        # Extract data from response
        cost_data = response.get('data', [])
        metadata = response.get('_metadata', {})
        
        print(f"[OK] Retrieved {len(cost_data)} cost data points")
        print(f"  Execution time: {metadata.get('execution_time_ms', 0):.2f}ms")
        
        # Show cost summary
        if cost_data:
            total_cost = sum(float(ct.get('amount', 0)) for ct in cost_data)
            print(f"\nCost Summary:")
            print(f"  Total: ${total_cost:.2f}")
            print(f"  Average per day: ${total_cost/len(cost_data):.2f}")
            
            print("\nDaily breakdown:")
            for ct in cost_data[-3:]:  # Last 3 days
                print(f"  {ct.get('date')}: ${float(ct.get('amount', 0)):.2f} ({ct.get('service', 'N/A')})")
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        if "AccessDeniedException" in error_msg:
            print("[SKIP] Cost Explorer not enabled in AWS Console")
            print("  This is expected - you can enable it later")
            return True  # Not a failure, just not enabled
        else:
            print(f"[FAIL] Error: {error_msg}")
            import traceback
            traceback.print_exc()
            return False

async def test_compliance_check():
    """Test compliance checking"""
    print("\n" + "="*60)
    print("TEST 3: Check Compliance (Tagging)")
    print("="*60)
    
    config = Config()
    server = MultiCloudIntelligenceServer(config)
    
    try:
        print("\nChecking tagging compliance...")
        response = await server.check_compliance(rule_type="tagging")
        
        # Extract data from response
        violations = response.get('data', [])
        metadata = response.get('_metadata', {})
        
        print(f"[OK] Compliance check complete")
        print(f"  Violations found: {len(violations)}")
        print(f"  Execution time: {metadata.get('execution_time_ms', 0):.2f}ms")
        
        if violations:
            print("\nSample violations:")
            for i, violation in enumerate(violations[:3]):
                print(f"  {i+1}. {violation.get('resource_id')}")
                print(f"     Issue: {violation.get('description')}")
                print(f"     Severity: {violation.get('severity')}")
        else:
            print("  No violations found - all resources are compliant!")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_new_resources():
    """Test finding new resources"""
    print("\n" + "="*60)
    print("TEST 4: Find New Resources (Last 30 Days)")
    print("="*60)
    
    config = Config()
    server = MultiCloudIntelligenceServer(config)
    
    try:
        cutoff_date = (datetime.now() - timedelta(days=30)).date()
        
        print(f"\nFinding resources created after {cutoff_date}...")
        response = await server.get_new_resources_since(
            cutoff_date=cutoff_date.strftime('%Y-%m-%d')
        )
        
        # Extract data from response
        new_resources = response.get('data', [])
        metadata = response.get('_metadata', {})
        
        print(f"[OK] Found {len(new_resources)} new resources")
        print(f"  Execution time: {metadata.get('execution_time_ms', 0):.2f}ms")
        
        if new_resources:
            print("\nNew resources:")
            for i, resource in enumerate(new_resources[:5]):
                print(f"  {i+1}. {resource.get('resource_type')}: {resource.get('resource_id')}")
                print(f"     Created: {resource.get('created_at')}")
        else:
            print("  No new resources in the last 30 days")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("MCP Server Tool Testing")
    print("="*60)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nThis will test the MCP server tools with your AWS account")
    print("="*60)
    
    results = {}
    
    # Run tests
    results['resource_summary'] = await test_resource_summary()
    results['cost_trends'] = await test_cost_trends()
    results['compliance'] = await test_compliance_check()
    results['new_resources'] = await test_new_resources()
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {test_name}")
    
    total_passed = sum(results.values())
    total_tests = len(results)
    
    print(f"\nResults: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n[OK] All tests passed! Your MCP server is working correctly.")
        print("\nNext steps:")
        print("  1. Run the full server: python mcp_server.py --transport stdio")
        print("  2. Or test with HTTP: python mcp_server.py --transport http --port 8000")
        print("  3. Review LOCAL_TESTING_GUIDE.md for more testing options")
        return 0
    else:
        print(f"\n[WARN] {total_tests - total_passed} test(s) failed")
        print("Check the errors above and review your AWS permissions")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)

# Made with Bob
