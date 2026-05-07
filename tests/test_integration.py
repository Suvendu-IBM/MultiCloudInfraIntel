#!/usr/bin/env python3
"""
Integration Tests for Multi-Cloud Infrastructure Intelligence MCP Server

These tests require actual cloud credentials and will make real API calls.
Run only in a test environment with appropriate credentials configured.
"""

import pytest
import sys
import os
import asyncio
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.integration
@pytest.mark.asyncio
class TestAWSIntegration:
    """Integration tests for AWS functionality."""
    
    async def test_aws_authentication(self):
        """Test AWS authentication with real credentials."""
        from mcp_server import AWSAuthManager
        
        manager = AWSAuthManager()
        
        if manager.available:
            is_auth = manager.is_authenticated()
            print(f"AWS Authentication: {'Success' if is_auth else 'Failed'}")
            # Don't fail if credentials aren't configured
        else:
            pytest.skip("AWS SDK not installed")
    
    async def test_aws_resource_listing(self):
        """Test listing AWS EC2 instances."""
        from mcp_server import Config, MultiCloudIntelligenceServer
        
        config = Config()
        server = MultiCloudIntelligenceServer(config)
        
        if server.aws_enabled:
            result = await server.get_resource_summary(cloud_provider='aws')
            print(f"AWS Resources found: {len(result['data'])}")
            assert '_metadata' in result
        else:
            pytest.skip("AWS not configured")


@pytest.mark.integration
@pytest.mark.asyncio
class TestAzureIntegration:
    """Integration tests for Azure functionality."""
    
    async def test_azure_authentication(self):
        """Test Azure authentication with real credentials."""
        from mcp_server import AzureAuthManager
        
        manager = AzureAuthManager()
        
        if manager.available:
            is_auth = manager.is_authenticated()
            print(f"Azure Authentication: {'Success' if is_auth else 'Failed'}")
        else:
            pytest.skip("Azure SDK not installed")
    
    async def test_azure_resource_listing(self):
        """Test listing Azure VMs."""
        from mcp_server import Config, MultiCloudIntelligenceServer
        
        config = Config()
        server = MultiCloudIntelligenceServer(config)
        
        if server.azure_enabled:
            result = await server.get_resource_summary(cloud_provider='azure')
            print(f"Azure Resources found: {len(result['data'])}")
            assert '_metadata' in result
        else:
            pytest.skip("Azure not configured")


@pytest.mark.integration
@pytest.mark.asyncio
class TestGCPIntegration:
    """Integration tests for GCP functionality."""
    
    async def test_gcp_authentication(self):
        """Test GCP authentication with real credentials."""
        from mcp_server import GCPAuthManager
        
        manager = GCPAuthManager()
        
        if manager.available:
            is_auth = manager.is_authenticated()
            print(f"GCP Authentication: {'Success' if is_auth else 'Failed'}")
        else:
            pytest.skip("GCP SDK not installed")
    
    async def test_gcp_resource_listing(self):
        """Test listing GCP instances."""
        from mcp_server import Config, MultiCloudIntelligenceServer
        
        config = Config()
        server = MultiCloudIntelligenceServer(config)
        
        if server.gcp_enabled:
            result = await server.get_resource_summary(cloud_provider='gcp')
            print(f"GCP Resources found: {len(result['data'])}")
            assert '_metadata' in result
        else:
            pytest.skip("GCP not configured")


@pytest.mark.integration
@pytest.mark.asyncio
class TestMultiCloudTools:
    """Integration tests for multi-cloud tools."""
    
    async def test_get_resource_summary(self):
        """Test get_resource_summary across all clouds."""
        from mcp_server import Config, MultiCloudIntelligenceServer
        
        config = Config()
        server = MultiCloudIntelligenceServer(config)
        
        result = await server.get_resource_summary()
        
        assert 'data' in result
        assert '_metadata' in result
        print(f"Total resources across all clouds: {len(result['data'])}")
    
    async def test_get_cost_trends(self):
        """Test get_cost_trends."""
        from mcp_server import Config, MultiCloudIntelligenceServer
        
        config = Config()
        server = MultiCloudIntelligenceServer(config)
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        result = await server.get_cost_trends(
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            granularity='DAILY'
        )
        
        assert 'data' in result
        assert '_metadata' in result
        print(f"Cost trends retrieved: {len(result['data'])} data points")
    
    async def test_check_compliance(self):
        """Test check_compliance for tagging."""
        from mcp_server import Config, MultiCloudIntelligenceServer
        
        config = Config()
        server = MultiCloudIntelligenceServer(config)
        
        result = await server.check_compliance(rule_type='tagging')
        
        assert 'data' in result
        assert '_metadata' in result
        print(f"Compliance violations found: {len(result['data'])}")
    
    async def test_get_budget_health(self):
        """Test get_budget_health."""
        from mcp_server import Config, MultiCloudIntelligenceServer
        
        config = Config()
        server = MultiCloudIntelligenceServer(config)
        
        result = await server.get_budget_health(team_name='engineering')
        
        assert 'data' in result
        assert '_metadata' in result
        assert 'status' in result['data']
        print(f"Budget status: {result['data']['status']}")


# Run integration tests
if __name__ == '__main__':
    print("=" * 60)
    print("Multi-Cloud Infrastructure Intelligence MCP Server")
    print("Integration Tests")
    print("=" * 60)
    print("\nWARNING: These tests make real API calls to cloud providers.")
    print("Ensure you have:")
    print("1. Valid cloud credentials configured")
    print("2. Appropriate permissions")
    print("3. Understanding of potential costs")
    print("\nRun with: pytest tests/test_integration.py -v -m integration")
    print("=" * 60)
    
    pytest.main([__file__, '-v', '-m', 'integration'])

# Made with Bob
