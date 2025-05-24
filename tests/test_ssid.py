import pytest
from src.network_utils import NetworkAPI

@pytest.fixture
def network_api():
    api = NetworkAPI()
    api.login()  # Login before testing
    return api

def test_change_ssid_successful(network_api):
    """Test successful SSID change"""
    new_ssid = "Test_Network_SSID"
    assert network_api.change_ssid(new_ssid) == True

def test_change_ssid_empty(network_api):
    """Test changing SSID to empty string"""
    assert network_api.change_ssid("") == False

def test_change_ssid_special_chars(network_api):
    """Test changing SSID with special characters"""
    new_ssid = "Test_Network_SSID_!@#$%^&*()"
    assert network_api.change_ssid(new_ssid) == True

def test_change_ssid_without_auth(network_api):
    """Test changing SSID without authentication"""
    network_api.token = None
    assert network_api.change_ssid("Test_SSID") == False 