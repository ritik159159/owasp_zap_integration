import os
import pytest
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ZAP_ADDRESS = os.getenv("ZAP_ADDRESS", "http://127.0.0.1:8081")
BASE_URL = os.getenv("TARGET", "https://jsonplaceholder.typicode.com")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL.rstrip("/")


@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    if os.getenv("USE_ZAP", "false").lower() == "true":
        s.proxies = {"http": ZAP_ADDRESS, "https": ZAP_ADDRESS}
        s.verify = False  # ZAP uses its own CA; fine in test environments
    token = os.getenv("AUTH_TOKEN")
    if token:
        s.headers["Authorization"] = f"Bearer {token}"
    return s