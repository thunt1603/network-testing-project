import pytest
from src.network_utils import NetworkAPI

@pytest.fixture
def network_api():
    api = NetworkAPI()
    api.login()  # Login before testing
    return api

def test_ping_successful(network_api):
    """Test successful ping to a host"""
    result = network_api.ping("8.8.8.8")
    assert result is not None
    assert "response_time" in result
    assert result["response_time"] > 0

def test_ping_invalid_host(network_api):
    """Test ping to an invalid host"""
    result = network_api.ping("invalid.host")
    assert result is None

def test_ping_without_auth(network_api):
    """Test ping without authentication"""
    network_api.token = None
    result = network_api.ping("8.8.8.8")
    assert result is None 