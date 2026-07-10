import requests
from config import API_URL

def assess_child(payload):
    r = requests.post(f"{API_URL}/assess-child", json=payload, timeout=30)
    r.raise_for_status()
    return r.json()

def get_model_info():
    r = requests.get(f"{API_URL}/model-info", timeout=10)
    r.raise_for_status()
    return r.json()

def get_dashboard_summary():
    r = requests.get(f"{API_URL}/dashboard-summary", timeout=10)
    r.raise_for_status()
    return r.json()

def get_wellness_distribution():
    r = requests.get(f"{API_URL}/wellness-distribution", timeout=10)
    r.raise_for_status()
    return r.json()

def get_age_group_analysis():
    r = requests.get(f"{API_URL}/age-group-analysis", timeout=10)
    r.raise_for_status()
    return r.json()

def get_health_concerns():
    r = requests.get(f"{API_URL}/health-concerns", timeout=10)
    r.raise_for_status()
    return r.json()

def get_device_analysis():
    r = requests.get(f"{API_URL}/device-analysis", timeout=10)
    r.raise_for_status()
    return r.json()

def get_urban_rural():
    r = requests.get(f"{API_URL}/urban-rural-comparison", timeout=10)
    r.raise_for_status()
    return r.json()
