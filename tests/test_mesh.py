import pytest
from src.network_utils import NetworkAPI

@pytest.fixture
def network_api():
    api = NetworkAPI()
    api.login()  # Login before testing
    return api

def test_enable_mesh_successful(network_api):
    """Test successful mesh enable"""
    assert network_api.enable_mesh() == True

def test_enable_mesh_without_auth(network_api):
    """Test enabling mesh without authentication"""
    network_api.token = None
    assert network_api.enable_mesh() == False

def test_enable_mesh_after_logout(network_api):
    """Test enabling mesh after logout"""
    network_api.logout()
    assert network_api.enable_mesh() == False 