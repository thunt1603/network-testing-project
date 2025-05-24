import pytest
from src.network_utils import NetworkAPI

@pytest.fixture
def network_api():
    return NetworkAPI()

def test_successful_login(network_api):
    """Test successful login"""
    assert network_api.login() == True
    assert network_api.token is not None

def test_failed_login(network_api):
    """Test failed login"""
    # Temporarily modify credentials to test failure
    original_username = network_api.username
    network_api.username = "wrong_username"
    
    assert network_api.login() == False
    assert network_api.token is None
    
    # Restore original credentials
    network_api.username = original_username

def test_logout(network_api):
    """Test logout functionality"""
    # First login
    network_api.login()
    assert network_api.token is not None
    
    # Then logout
    assert network_api.logout() == True
    assert network_api.token is None 