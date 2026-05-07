#!/usr/bin/env python3
"""
Quick AWS Authentication and Connection Test
Tests AWS credentials and basic resource access before running the full MCP server.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import mcp_server
sys.path.insert(0, str(Path(__file__).parent.parent))

import boto3
from datetime import datetime, timedelta

def test_aws_authentication():
    """Test AWS authentication and basic access"""
    print("=" * 60)
    print("AWS Authentication Test")
    print("=" * 60)
    
    try:
        # Test STS (Security Token Service) - validates credentials
        print("\n1. Testing AWS Credentials...")
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        
        print(f"[OK] AWS Authentication Successful!")
        print(f"  Account ID: {identity['Account']}")
        print(f"  User ARN: {identity['Arn']}")
        print(f"  User ID: {identity['UserId']}")
        
    except Exception as e:
        print(f"[FAIL] AWS Authentication Failed: {str(e)}")
        print("\nPlease configure AWS credentials:")
        print("  Option 1: aws configure")
        print("  Option 2: Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")
        return False
    
    # Test EC2 access
    try:
        print("\n2. Testing EC2 Access...")
        ec2 = boto3.client('ec2', region_name='us-east-1')
        regions = ec2.describe_regions()
        print(f"[OK] EC2 Access Successful! Found {len(regions['Regions'])} regions")
        
        # List instances in default region
        instances = ec2.describe_instances()
        instance_count = sum(len(r['Instances']) for r in instances['Reservations'])
        print(f"  Instances in us-east-1: {instance_count}")
        
    except Exception as e:
        print(f"[FAIL] EC2 Access Failed: {str(e)}")
    
    # Test S3 access
    try:
        print("\n3. Testing S3 Access...")
        s3 = boto3.client('s3')
        buckets = s3.list_buckets()
        print(f"[OK] S3 Access Successful! Found {len(buckets['Buckets'])} buckets")
        
    except Exception as e:
        print(f"[FAIL] S3 Access Failed: {str(e)}")
    
    # Test Cost Explorer access
    try:
        print("\n4. Testing Cost Explorer Access...")
        ce = boto3.client('ce', region_name='us-east-1')
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date.strftime('%Y-%m-%d'),
                'End': end_date.strftime('%Y-%m-%d')
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost']
        )
        
        print(f"[OK] Cost Explorer Access Successful!")
        print(f"  Retrieved {len(response['ResultsByTime'])} days of cost data")
        
        # Show recent costs
        if response['ResultsByTime']:
            latest = response['ResultsByTime'][-1]
            amount = latest['Total']['UnblendedCost']['Amount']
            print(f"  Latest daily cost: ${float(amount):.2f}")
        
    except Exception as e:
        print(f"[FAIL] Cost Explorer Access Failed: {str(e)}")
        print("  Note: Cost Explorer API may need to be enabled in AWS Console")
    
    # Test CloudWatch access
    try:
        print("\n5. Testing CloudWatch Access...")
        cw = boto3.client('cloudwatch', region_name='us-east-1')
        metrics = cw.list_metrics(Namespace='AWS/EC2', MaxRecords=10)
        print(f"[OK] CloudWatch Access Successful!")
        print(f"  Found {len(metrics['Metrics'])} EC2 metrics")
        
    except Exception as e:
        print(f"[FAIL] CloudWatch Access Failed: {str(e)}")
    
    print("\n" + "=" * 60)
    print("AWS Connection Test Complete!")
    print("=" * 60)
    return True

def test_mcp_server_import():
    """Test if MCP server can be imported"""
    print("\n" + "=" * 60)
    print("MCP Server Import Test")
    print("=" * 60)
    
    try:
        print("\nImporting mcp_server module...")
        import mcp_server
        print("[OK] MCP Server module imported successfully!")
        
        # Check if main components exist
        components = [
            'MultiCloudIntelligenceServer',
            'AWSAuthManager',
            'Config',
            'CacheManager'
        ]
        
        for component in components:
            if hasattr(mcp_server, component):
                print(f"  [OK] {component} found")
            else:
                print(f"  [FAIL] {component} not found")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Failed to import MCP server: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Multi-Cloud Infrastructure Intelligence - Pre-Flight Check")
    print("=" * 60)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test AWS
    aws_ok = test_aws_authentication()
    
    # Test MCP Server
    mcp_ok = test_mcp_server_import()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"AWS Authentication: {'[PASS]' if aws_ok else '[FAIL]'}")
    print(f"MCP Server Import: {'[PASS]' if mcp_ok else '[FAIL]'}")
    
    if aws_ok and mcp_ok:
        print("\n[OK] All tests passed! You can now run the MCP server.")
        print("\nNext steps:")
        print("  1. Run server: python mcp_server.py --transport stdio")
        print("  2. Or test with: python tests/validate_tools.py")
        return 0
    else:
        print("\n[FAIL] Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

# Made with Bob
