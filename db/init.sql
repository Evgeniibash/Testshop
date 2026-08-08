-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Таблица категорий
CREATE TABLE IF NOT EXISTS categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL
);

-- Таблица товаров
CREATE TABLE IF NOT EXISTS products (
  id SERIAL PRIMARY KEY,
  category_id INT REFERENCES categories(id),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  price NUMERIC(10,2) NOT NULL CHECK (price >= 0),
  stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
  active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Таблица корзин
CREATE TABLE IF NOT EXISTS carts (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Таблица элементов корзины
CREATE TABLE IF NOT EXISTS cart_items (
  id SERIAL PRIMARY KEY,
  cart_id INT NOT NULL REFERENCES carts(id) ON DELETE CASCADE,
  product_id INT NOT NULL REFERENCES products(id),
  quantity INT NOT NULL CHECK (quantity > 0),
  UNIQUE(cart_id, product_id)
);

-- Таблица заказов
CREATE TABLE IF NOT EXISTS orders (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id),
  status VARCHAR(30) NOT NULL DEFAULT 'pending',
  total NUMERIC(10,2) NOT NULL DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Таблица элементов заказа
CREATE TABLE IF NOT EXISTS order_items (
  id SERIAL PRIMARY KEY,
  order_id INT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id INT NOT NULL REFERENCES products(id),
  quantity INT NOT NULL CHECK (quantity > 0),
  price NUMERIC(10,2) NOT NULL
);

-- Вставка категорий
INSERT INTO categories (name) VALUES
('Смартфоны'), ('Ноутбуки'), ('Аксессуары');

-- Вставка товаров
INSERT INTO products (category_id, name, description, price, stock) VALUES
(1, 'TestPhone X', 'Тестовый смартфон', 699.99, 10),
(1, 'Budget Phone', 'Недорогой смартфон', 199.99, 0),
(2, 'TestBook Pro', 'Тестовый ноутбук', 1299.00, 5),
(3, 'USB-C Cable', 'Кабель USB-C', 19.99, 100),
(3, 'Wireless Mouse', 'Беспроводная мышь', 39.90, 25);

-- Вставка пользователя
INSERT INTO users (email, password, name)
VALUES ('demo@example.com', 'demo123', 'Demo User');

-- Вставка корзины для пользователя
INSERT INTO carts (user_id) VALUES (1);
