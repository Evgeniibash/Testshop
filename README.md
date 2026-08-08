# Test Shop — учебный стенд для автотестов

Небольшой интернет-магазин для практики UI/API/DB-тестирования.

## 📊 Статус CI/CD

[![CI](https://github.com/Evgeniibash/Testshop/actions/workflows/ci.yml/badge.svg)](https://github.com/Evgeniibash/Testshop/actions/workflows/ci.yml)

## 📈 Allure-отчёт

👉 [Allure Report](https://Evgeniibash.github.io/Testshop/)

---

## Запуск

Требуется Docker + Docker Compose.

    docker compose up -d --build

После запуска:

- Frontend: http://localhost:8080
- API: http://localhost:3000
- Health: http://localhost:3000/api/health
- PostgreSQL: localhost:5432

---

## Тестовый пользователь

| Поле | Значение |
|---|---|
| email | `demo@example.com` |
| password | `demo123` |
| userId | `1` |

---

## API

| Метод | URL |
|---|---|
| GET | `/api/products` |
| GET | `/api/products/:id` |
| POST | `/api/auth/register` |
| POST | `/api/auth/login` |
| GET | `/api/cart/:userId` |
| POST | `/api/cart/:userId/items` |
| PUT | `/api/cart/:userId/items/:itemId` |
| DELETE | `/api/cart/:userId/items/:itemId` |
| POST | `/api/orders` |
| GET | `/api/orders/:id` |

---

## Задания для ученика

1. Проверить health endpoint.
2. Проверить получение списка товаров.
3. Проверить поиск товара.
4. Проверить получение существующего и несуществующего товара.
5. Проверить регистрацию нового пользователя.
6. Проверить повторную регистрацию с тем же email.
7. Проверить login с правильным и неправильным паролем.
8. Добавить товар в корзину.
9. Проверить невозможность добавить отрицательное/нулевое количество.
10. Проверить товар без остатка.
11. Изменить количество товара в корзине.
12. Удалить товар из корзины.
13. Оформить заказ.
14. Проверить очистку корзины после заказа.
15. Проверить уменьшение stock после заказа.
16. Проверить пустую корзину.
17. Проверить несуществующий order ID.
18. Проверить пересчёт total.
19. Проверить SQL-данные напрямую в PostgreSQL.
20. Написать автоматические UI и API тесты.

---

## Полезные данные

| Товар | id | stock |
|---|---|---|
| Budget Phone | 2 | 0 |
| USB-C Cable | 4 | 100 |
| TestBook Pro | 3 | 5 |

---

## Сброс базы

Чтобы заново выполнить `db/init.sql`:

    docker compose down -v
    docker compose up -d --build

⚠️ **Внимание:** `down -v` удаляет данные PostgreSQL.

---

## 📬 Контакты

- GitHub: [Evgeniibash](https://github.com/Evgeniibash)
- Проект: [Testshop](https://github.com/Evgeniibash/Testshop)