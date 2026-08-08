# Test Shop — учебный стенд для автотестов

Небольшой интернет-магазин для практики UI/API/DB-тестирования.

## 📊 Статус CI/CD

[![CI](https://github.com/Evgeniibash/Testshop/actions/workflows/ci.yml/badge.svg)](https://github.com/Evgeniibash/Testshop/actions/workflows/ci.yml)

## 📈 Allure-отчёт

👉 [Allure Report](https://Evgeniibash.github.io/Testshop/)

---

## Запуск

Требуется Docker + Docker Compose.

```bash
docker compose up -d --build
После запуска:

Frontend: http://localhost:8080
API: http://localhost:3000
Health: http://localhost:3000/api/health
PostgreSQL: localhost:5432
Тестовый пользователь

Поле    Значение
email   demo@example.com
password    demo123
userId  1
API

Метод   URL
GET /api/products
GET /api/products/:id
POST    /api/auth/register
POST    /api/auth/login
GET /api/cart/:userId
POST    /api/cart/:userId/items
PUT /api/cart/:userId/items/:itemId
DELETE  /api/cart/:userId/items/:itemId
POST    /api/orders
GET /api/orders/:id
Задания для ученика

Проверить health endpoint.
Проверить получение списка товаров.
Проверить поиск товара.
Проверить получение существующего и несуществующего товара.
Проверить регистрацию нового пользователя.
Проверить повторную регистрацию с тем же email.
Проверить login с правильным и неправильным паролем.
Добавить товар в корзину.
Проверить невозможность добавить отрицательное/нулевое количество.
Проверить товар без остатка.
Изменить количество товара в корзине.
Удалить товар из корзины.
Оформить заказ.
Проверить очистку корзины после заказа.
Проверить уменьшение stock после заказа.
Проверить пустую корзину.
Проверить несуществующий order ID.
Проверить пересчёт total.
Проверить SQL-данные напрямую в PostgreSQL.
Написать автоматические UI и API тесты.
Полезные данные

Товар   id  stock
Budget Phone    2   0
USB-C Cable 4   100
TestBook Pro    3   5
Сброс базы

Чтобы заново выполнить db/init.sql:

bash
Копировать
Скачать
docker compose down -v
docker compose up -d --build
⚠️ Внимание: down -v удаляет данные PostgreSQL.

📬 Контакты

GitHub: Evgeniibash
Проект: Testshop