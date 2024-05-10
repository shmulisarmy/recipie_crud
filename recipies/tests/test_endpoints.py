import pytest
import requests

BASE_URL = "http://127.0.0.1:8000/recipies"


def test_get_recipies():
    url = f"{BASE_URL}"
    response = requests.get(url)
    assert response.status_code == 200



def test_get_recipies_by_time():
    url = f"{BASE_URL}/time_to_make?min_time=1&max_time=20"
    response = requests.get(url)
    assert response.status_code == 200