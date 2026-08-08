import requests
import pytest
import time

BASE_URL = "http://localhost:3000/api"

def test_health():
    print("Отправляю запрос на /health")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Получен статус: {response.status_code}")
    
    pytest.assume(response.status_code == 200, "Ожидался статус 200")
    pytest.assume(response.json() == {"status": "ok"}, "Ожидался {'status': 'ok'}")
    print("Health-проверка пройдена")

# ================================================
# ЗАДАНИЕ 2: Список товаров
# ================================================

def test_get_products():
    print("\n🔍 Задание 2: Получение списка товаров")
    
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    
    pytest.assume(response.status_code == 200, "Статус не 200")
    pytest.assume(isinstance(products, list), "Ответ не список")
    pytest.assume(len(products) > 0, "Список товаров пуст")
    pytest.assume("id" in products[0], "В первом товаре нет id")
    pytest.assume("name" in products[0], "В первом товаре нет name")
    
    print(f"📦 Найдено товаров: {len(products)}")
    print("✅ Задание 2 завершено")

# ================================================
# ЗАДАНИЕ 3: Поиск товара
# ================================================

def test_search_product():
    print("\n🔍 Ищу товар по названию 'Phone'...")
    
    response = requests.get(f"{BASE_URL}/products")
    products = response.json()
    
    found = False
    for p in products:
        if "phone" in p["name"].lower():
            found = True
            print(f"✅ Найден товар: {p['name']}")
            break
    
    pytest.assume(found, "Товар с 'phone' не найден")
    print("✅ Задание 3 завершено")

# ================================================
# ЗАДАНИЕ 4: Товар по ID (существующий)
# ================================================

def test_get_product_by_id():
    print("\n🔍 Получаю товар с id=1...")
    
    response = requests.get(f"{BASE_URL}/products/1")
    
    print(f"📡 Статус: {response.status_code}")
    product = response.json()
    print(f"📦 Название: {product.get('name')}")
    
    pytest.assume(response.status_code == 200, "Статус не 200 для id=1")
    pytest.assume("id" in product, "Нет id в товаре")
    pytest.assume("name" in product, "Нет name в товаре")
    
    print("✅ Товар получен")

# ================================================
# ЗАДАНИЕ 5: Несуществующий товар
# ================================================

def test_get_product_not_found():
    print("\n🔍 Пытаюсь получить несуществующий товар (id=999)...")
    
    response = requests.get(f"{BASE_URL}/products/999")
    
    pytest.assume(response.status_code == 404, "Ожидался 404 для несуществующего товара")
    
    print("✅ Задание 5 завершено")

# ================================================
# ЗАДАНИЕ 6: Регистрация нового пользователя
# ================================================

def test_register_new_user():
    print("\n🔍 Задание 6: Регистрация нового пользователя")
    
    import time
    payload = {
        "email": f"newuser_{time.time()}@example.com",
        "password": "newpass123",
        "name": "Test User" 
    }

    
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    
    print(f"📡 Статус: {response.status_code}")
    pytest.assume(response.status_code in [200, 201], "Ожидался 200 или 201")
    pytest.assume("id" in response.json(), "В ответе нет id")
    print("✅ Пользователь создан")

# ================================================
# ЗАДАНИЕ 7: Повторная регистрация
# ================================================

def test_register_duplicate_email():
    print("\n🔍 Задание 7: Повторная регистрация с тем же email")
    
    payload = {
        "email": "newuser@example.com",
        "password": "newpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    
    print(f"📡 Статус: {response.status_code}")
    pytest.assume(response.status_code == 400, "Ожидался статус 400")
    print("✅ Дубликат не пропущен")

# ================================================
# ЗАДАНИЕ 8: Логин
# ================================================

def test_login_success():
    print("\n🔍 Задание 7: Логин с правильным паролем")
    
    payload = {
        "email": "demo@example.com",
        "password": "demo123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    
    print(f"📡 Статус: {response.status_code}")
    print(f"📦 Ответ: {response.json()}")
    
    pytest.assume(response.status_code == 200, "Ожидался статус 200")
    
    data = response.json()
    
    # Проверяем, что в ответе есть пользователь
    pytest.assume("user" in data, "В ответе нет объекта user")
    pytest.assume(data["user"]["email"] == "demo@example.com", "Email не совпадает")
    pytest.assume(data["user"]["id"] == 1, "ID пользователя не 1")
    
    print("✅ Вход выполнен, пользователь получен")

# ================================================
# ЗАДАНИЕ 9: Логин с неправильным паролем
# ================================================

def test_login_fail():
    print("\n🔍 Задание 9: Логин с неправильным паролем")
    
    payload = {
        "email": "demo@example.com",
        "password": "wrongpassword"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=payload)
    
    print(f"📡 Статус: {response.status_code}")
    pytest.assume(response.status_code == 401, "Ожидался статус 401")
    print("✅ Неверный пароль отклонён")



# ==================== 10. КОРЗИНА ====================
def test_add_to_cart():
    print("\n🔍 Задание 10: Добавление товара в корзину")
    requests.delete(f"{BASE_URL}/cart/1/items/1")
    payload = {"productId": 1, "quantity": 2}
    response = requests.post(f"{BASE_URL}/cart/1/items", json=payload)
    print(f"📡 Статус: {response.status_code}")
    pytest.assume(response.status_code in [200, 201], "Ожидался 200 или 201")
    cart = response.json()
    pytest.assume(len(cart.get("items", [])) > 0, "Корзина пуста")
    print("✅ Товар добавлен")

def test_add_negative_quantity():
    print("\n🔍 Задание 11: Отрицательное количество")
    payload = {"productId": 1, "quantity": -1}
    response = requests.post(f"{BASE_URL}/cart/1/items", json=payload)
    print(f"📡 Статус: {response.status_code}")
    pytest.assume(response.status_code == 400, "Ожидался 400")
    print("✅ Отклонено")

def test_add_out_of_stock():
    print("\n🔍 Задание 12: Товар без остатка")
    payload = {"productId": 2, "quantity": 1}
    response = requests.post(f"{BASE_URL}/cart/1/items", json=payload)
    print(f"📡 Статус: {response.status_code}")
    pytest.assume(response.status_code == 409, "Ожидался 409")
    print("✅ Не добавлен")

def test_update_cart_item():
    print("\n🔍 Задание 13: Изменение количества")
    
    # Очищаем корзину перед тестом
    requests.delete(f"{BASE_URL}/cart/1/items/1")
    
    # Добавляем товар в корзину
    add_response = requests.post(f"{BASE_URL}/cart/1/items", json={"productId": 1, "quantity": 1})
    print(f"📡 Добавление: {add_response.status_code}")
    
    # Получаем ID элемента корзины
    add_data = add_response.json()
    if "items" in add_data and add_data["items"]:
        item_id = add_data["items"][-1]["id"]
    else:
        item_id = 1
    
    # Обновляем количество
    response = requests.put(f"{BASE_URL}/cart/1/items/{item_id}", json={"quantity": 5})
    print(f"📡 Обновление: {response.status_code}")
    
    pytest.assume(response.status_code in [200, 201], "Ожидался 200 или 201")
    print("✅ Обновлено")

def test_delete_cart_item():
    print("\n🔍 Задание 14: Удаление товара из корзины")
    requests.post(f"{BASE_URL}/cart/1/items", json={"productId": 1, "quantity": 1})
    response = requests.delete(f"{BASE_URL}/cart/1/items/1")
    print(f"📡 Статус: {response.status_code}")
    pytest.assume(response.status_code == 204, "Ожидался 204")
    print("✅ Удалено")

# ==================== 15. ЗАКАЗЫ ====================
def test_create_order():
    print("\n🔍 Задание 15: Оформление заказа")
    

    requests.delete(f"{BASE_URL}/cart/1/items/1")
    

    add_response = requests.post(f"{BASE_URL}/cart/1/items", json={"productId": 1, "quantity": 2})
    print(f"📡 Добавление в корзину: {add_response.status_code}")
    
    # Оформляем заказ
    response = requests.post(f"{BASE_URL}/orders", json={"userId": 1})
    print(f"📡 Статус заказа: {response.status_code}")
    print(f"📦 Ответ: {response.json()}")
    

    pytest.assume(response.status_code in [200, 201, 409], "Ожидался 200, 201 или 409")
    
    if response.status_code == 409:
        print("✅ Заказ уже существует (это нормально)")
    else:

        data = response.json()
        has_id = "id" in data or "orderId" in data or "order_id" in data
        pytest.assume(has_id, "Нет id заказа")
        print("✅ Заказ оформлен")

def test_cart_cleared_after_order():
    print("\n🔍 Задание 16: Корзина очищается после заказа")
    requests.post(f"{BASE_URL}/cart/1/items", json={"productId": 1, "quantity": 1})
    requests.post(f"{BASE_URL}/orders", json={"userId": 1})
    response = requests.get(f"{BASE_URL}/cart/1")
    cart = response.json()
    pytest.assume(len(cart["items"]) == 0, "Корзина не очистилась")
    print("✅ Корзина пуста")

def test_stock_decreased_after_order():
    print("\n🔍 Задание 17: Stock уменьшается после заказа")
    response = requests.get(f"{BASE_URL}/products/3")
    stock_before = response.json()["stock"]
    requests.post(f"{BASE_URL}/cart/1/items", json={"productId": 3, "quantity": 1})
    requests.post(f"{BASE_URL}/orders", json={"userId": 1})
    response = requests.get(f"{BASE_URL}/products/3")
    stock_after = response.json()["stock"]
    pytest.assume(stock_after == stock_before - 1, "Stock не уменьшился")
    print("✅ Stock уменьшен")

def test_empty_cart():
    print("\n🔍 Задание 18: Пустая корзина")
    requests.delete(f"{BASE_URL}/cart/1/items/1")
    response = requests.get(f"{BASE_URL}/cart/1")
    cart = response.json()
    pytest.assume(len(cart["items"]) == 0, "Корзина не пуста")
    print("✅ Корзина пуста")

def test_order_not_found():
    print("\n🔍 Задание 19: Несуществующий заказ")
    response = requests.get(f"{BASE_URL}/orders/999")
    print(f"📡 Статус: {response.status_code}")
    pytest.assume(response.status_code == 404, "Ожидался 404")
    print("✅ 404 получен")

def test_total_recalculation():
    print("\n🔍 Задание 20: Пересчёт total")
    requests.delete(f"{BASE_URL}/cart/1/items/1")
    requests.post(f"{BASE_URL}/cart/1/items", json={"productId": 1, "quantity": 2})
    requests.post(f"{BASE_URL}/cart/1/items", json={"productId": 4, "quantity": 1})
    response = requests.get(f"{BASE_URL}/cart/1")
    cart = response.json()
    print(f"📦 Ответ: {cart}")
    
    expected_total = 0
    for item in cart["items"]:
        price = float(item["price"])
        quantity = item["quantity"]
        expected_total += price * quantity
    
    print(f"💰 Ожидаемый total: {expected_total}")
    print(f"💰 Фактический total: {cart['total']}")
    pytest.assume(cart["total"] == expected_total, "Total не совпадает")
    print("✅ Total пересчитан")

