import pytest
import requests
import psycopg2
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

BASE_URL = "http://localhost:3000/api"
FRONTEND_URL = "http://localhost:8080"

# Настройки БД для локального запуска и для CI
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "shop")
DB_PASSWORD = os.getenv("DB_PASSWORD", "shop")
DB_NAME = os.getenv("DB_NAME", "shop")

DB_CONFIG = {
    "host": DB_HOST,
    "database": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD
}

def clean_database():
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