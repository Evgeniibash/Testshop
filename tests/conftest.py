import pytest
import requests
import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os

BASE_URL = "http://localhost:3000/api"
FRONTEND_URL = "http://localhost:8080"

DB_CONFIG = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "postgres"
}

def clean_database():
    """Очищает базу данных только для API-тестов"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("TRUNCATE cart_items, orders, users, products RESTART IDENTITY CASCADE;")
        conn.commit()
        conn.close()
        print("🧹 База данных очищена")
    except Exception as e:
        print(f"⚠️ Ошибка очистки БД: {e}")

@pytest.fixture(autouse=True)
def clean_db():
    """Очищает базу перед каждым тестом"""
    clean_database()
    yield

@pytest.fixture
def api_client():
    return requests.Session()

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()