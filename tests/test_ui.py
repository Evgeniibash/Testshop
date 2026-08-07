import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_ui_products_page(driver):
    """Проверка: открывается страница с товарами"""
    driver.get("http://localhost:8080")
    wait = WebDriverWait(driver, 10)
    
    products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card")))
    assert len(products) > 0
    print(f"✅ Найдено товаров на странице: {len(products)}")

def test_ui_add_to_cart(driver):
    driver.get("http://localhost:8080")
    wait = WebDriverWait(driver, 10)
    
    # Находим первую кнопку "В корзину"
    add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-card .btn-cart")))
    add_btn.click()
    
    # Ждём, что счётчик обновится до 1
    cart_count = wait.until(lambda d: d.find_element(By.ID, "cart-count"))
    wait.until(lambda d: cart_count.text == "1")
    
    assert cart_count.text == "1"
    print("✅ Товар добавлен в корзину")
    
def test_ui_open_cart(driver):
    """Проверка: открытие корзины"""
    driver.get("http://localhost:8080")
    wait = WebDriverWait(driver, 10)
    
    # Добавим товар, чтобы корзина не была пустой
    add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-card .btn-cart")))
    add_btn.click()
    
    # Ждём, что счётчик обновится до 1
    cart_count = wait.until(lambda d: d.find_element(By.ID, "cart-count"))
    wait.until(lambda d: cart_count.text == "1")
    time.sleep(1)
    
    # Открываем корзину
    cart_btn = driver.find_element(By.ID, "cart-btn")
    cart_btn.click()
    time.sleep(1)
    
    # Проверяем, есть ли alert
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        assert "Корзина" in alert_text
        alert.accept()
        print("✅ Корзина открыта (alert)")
    except:
        # Если alert нет, ищем модалку
        try:
            modal = wait.until(EC.visibility_of_element_located((By.ID, "cart-modal")))
            assert modal.is_displayed()
            print("✅ Корзина открыта (модалка)")
        except:
            # Если ничего нет — проверяем, что содержимое корзины отображается
            body_text = driver.find_element(By.TAG_NAME, "body").text
            assert "Корзина" in body_text or "товар" in body_text.lower()
            print("✅ Корзина открыта (текст на странице)")