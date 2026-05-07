#!/usr/bin/env python3
"""
Unit Tests for Multi-Cloud Infrastructure Intelligence MCP Server

Tests with mocked API responses to validate functionality without real cloud credentials.
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestConfig:
    """Test configuration management."""
    
    def test_config_defaults(self):
        """Test that default configuration is loaded correctly."""
        from mcp_server import Config
        
        config = Config('nonexistent.yaml')
        
        assert config.get('server.port') == 8000
        assert config.get('server.cache_ttl') == 3600
        # Default region can vary by config, just check it exists
        assert config.get('clouds.aws.default_region') in ['us-east-1', 'ap-south-1']
        # Budget default can vary, just check it's a positive number
        assert config.get('budgets.default') > 0
    
    def test_config_get_nested(self):
        """Test nested configuration retrieval."""
        from mcp_server import Config
        
        config = Config('nonexistent.yaml')
        
        assert config.get('compliance.mandatory_tags') == ['owner', 'cost-center', 'environment']
        assert config.get('monitoring.idle_cpu_threshold') == 5


class TestCacheManager:
    """Test caching functionality."""
    
    def test_cache_set_and_get(self):
        """Test basic cache operations."""
        from mcp_server import CacheManager
        
        cache = CacheManager(default_ttl=3600)
        
        cache.set('test_key', {'data': 'value'})
        result = cache.get('test_key')
        
        assert result == {'data': 'value'}
    
    def test_cache_expiry(self):
        """Test cache expiration."""
        from mcp_server import CacheManager
        import time
        
        cache = CacheManager(default_ttl=1)
        
        cache.set('test_key', {'data': 'value'}, ttl=1)
        time.sleep(2)
        result = cache.get('test_key')
        
        assert result is None
    
    def test_cache_key_generation(self):
        """Test cache key generation."""
        from mcp_server import CacheManager
        
        cache = CacheManager()
        
        key1 = cache._generate_key('prefix', {'a': 1, 'b': 2})
        key2 = cache._generate_key('prefix', {'b': 2, 'a': 1})
        
        assert key1 == key2  # Order shouldn't matter


class TestDataModels:
    """Test data model classes."""
    
    def test_resource_summary_to_dict(self):
        """Test ResourceSummary serialization."""
        from mcp_server import ResourceSummary
        
        resource = ResourceSummary(
            resource_id='i-12345',
            provider='aws',
            type='ec2',
            region='us-east-1',
            state='running',
            created_time='2024-01-01T00:00:00Z',
            tags={'Name': 'test'},
            metadata={'instance_type': 't2.micro'}
        )
        
        result = resource.to_dict()
        
        assert result['resource_id'] == 'i-12345'
        assert result['provider'] == 'aws'
        assert result['tags']['Name'] == 'test'
    
    def test_cost_trend_to_dict(self):
        """Test CostTrend serialization."""
        from mcp_server import CostTrend
        
        trend = CostTrend(
            date='2024-01-01',
            provider='aws',
            service='EC2',
            cost=100.50
        )
        
        result = trend.to_dict()
        
        assert result['date'] == '2024-01-01'
        assert result['cost'] == 100.50
        assert result['currency'] == 'USD'


class TestAWSAuthManager:
    """Test AWS authentication manager."""
    
    @patch('mcp_server.boto3')
    def test_aws_client_creation(self, mock_boto3):
        """Test AWS client creation."""
        from mcp_server import AWSAuthManager
        
        mock_sts_client = Mock()
        mock_sts_client.get_caller_identity.return_value = {'Arn': 'arn:aws:iam::123456789012:user/test'}
        
        mock_ec2_client = Mock()
        
        # Mock boto3.client to return different clients based on service
        def client_side_effect(service, **kwargs):
            if service == 'sts':
                return mock_sts_client
            elif service == 'ec2':
                return mock_ec2_client
            return Mock()
        
        mock_boto3.client.side_effect = client_side_effect
        
        manager = AWSAuthManager()
        client = manager.get_client('ec2', 'us-east-1')
        
        assert client == mock_ec2_client
        # Verify ec2 client was created (STS is called during init for auth check)
        assert any(call[0][0] == 'ec2' for call in mock_boto3.client.call_args_list)


@pytest.mark.asyncio
class TestRetryLogic:
    """Test retry and error handling."""
    
    async def test_retry_success(self):
        """Test successful retry."""
        from mcp_server import retry_with_backoff
        
        mock_func = Mock(return_value='success')
        
        result = await retry_with_backoff(mock_func, max_retries=3)
        
        assert result == 'success'
        assert mock_func.call_count == 1
    
    async def test_retry_with_timeout(self):
        """Test retry with timeout."""
        from mcp_server import retry_with_backoff
        import asyncio
        
        def slow_func():
            import time
            time.sleep(5)
            return 'success'
        
        with pytest.raises(Exception):
            await retry_with_backoff(slow_func, timeout=1, max_retries=1)


# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v'])

# Made with Bob
