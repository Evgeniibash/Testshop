const express = require("express");
const cors = require("cors");
const { Pool } = require("pg");

const app = express();
app.use(cors());
app.use(express.json());

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

app.get("/api/health", async (req, res) => {
  try {
    await pool.query("SELECT 1");
    res.json({ status: "ok" });
  } catch (e) {
    res.status(503).json({ status: "error" });
  }
});

app.get("/api/products", async (req, res) => {
  const { category, q } = req.query;
  const values = [];
  const conditions = ["p.active = true"];
  if (category) {
    values.push(category);
    conditions.push(`c.name = $${values.length}`);
  }
  if (q) {
    values.push(`%${q}%`);
    conditions.push(`(p.name ILIKE $${values.length} OR p.description ILIKE $${values.length})`);
  }
  const sql = `
    SELECT p.id, p.name, p.description, p.price, p.stock,
           c.id AS category_id, c.name AS category
    FROM products p
    LEFT JOIN categories c ON c.id = p.category_id
    WHERE ${conditions.join(" AND ")}
    ORDER BY p.id`;
  const result = await pool.query(sql, values);
  res.json(result.rows);
});

app.get("/api/products/:id", async (req, res) => {
  const result = await pool.query(
    `SELECT p.*, c.name AS category FROM products p
     LEFT JOIN categories c ON c.id=p.category_id WHERE p.id=$1 AND p.active=true`,
    [req.params.id]
  );
  if (!result.rowCount) return res.status(404).json({ error: "Product not found" });
  res.json(result.rows[0]);
});

app.post("/api/auth/register", async (req, res) => {
  const { email, password, name } = req.body;
  if (!email || !password || !name)
    return res.status(400).json({ error: "email, password and name are required" });
  try {
    const user = await pool.query(
      "INSERT INTO users(email,password,name) VALUES($1,$2,$3) RETURNING id,email,name",
      [email, password, name]
    );
    await pool.query("INSERT INTO carts(user_id) VALUES($1)", [user.rows[0].id]);
    res.status(201).json(user.rows[0]);
  } catch (e) {
    if (e.code === "23505") return res.status(409).json({ error: "Email already exists" });
    res.status(500).json({ error: "Internal error" });
  }
});

app.post("/api/auth/login", async (req, res) => {
  const { email, password } = req.body;
  const result = await pool.query(
    "SELECT id,email,name FROM users WHERE email=$1 AND password=$2",
    [email, password]
  );
  if (!result.rowCount) return res.status(401).json({ error: "Invalid credentials" });
  res.json({ user: result.rows[0] });
});

async function getCart(userId) {
  const result = await pool.query(`
    SELECT ci.id, ci.product_id, p.name, p.price, p.stock, ci.quantity,
           (p.price * ci.quantity) AS subtotal
    FROM cart_items ci
    JOIN carts c ON c.id=ci.cart_id
    JOIN products p ON p.id=ci.product_id
    WHERE c.user_id=$1 ORDER BY ci.id`, [userId]);
  const total = result.rows.reduce((s, x) => s + Number(x.subtotal), 0);
  return { items: result.rows, total: Number(total.toFixed(2)) };
}

app.get("/api/cart/:userId", async (req, res) => {
  res.json(await getCart(req.params.userId));
});

app.post("/api/cart/:userId/items", async (req, res) => {
  const userId = Number(req.params.userId);
  const { productId, quantity } = req.body;
  if (!Number.isInteger(quantity) || quantity <= 0)
    return res.status(400).json({ error: "quantity must be a positive integer" });

  const cart = await pool.query("SELECT id FROM carts WHERE user_id=$1", [userId]);
  if (!cart.rowCount) return res.status(404).json({ error: "Cart not found" });

  const product = await pool.query("SELECT id,stock FROM products WHERE id=$1 AND active=true", [productId]);
  if (!product.rowCount) return res.status(404).json({ error: "Product not found" });
  if (quantity > product.rows[0].stock)
    return res.status(409).json({ error: "Not enough stock" });

  await pool.query(`
    INSERT INTO cart_items(cart_id,product_id,quantity)
    VALUES($1,$2,$3)
    ON CONFLICT(cart_id,product_id)
    DO UPDATE SET quantity=cart_items.quantity + EXCLUDED.quantity`,
    [cart.rows[0].id, productId, quantity]
  );
  res.status(201).json(await getCart(userId));
});

app.put("/api/cart/:userId/items/:itemId", async (req, res) => {
  const quantity = Number(req.body.quantity);
  if (!Number.isInteger(quantity) || quantity <= 0)
    return res.status(400).json({ error: "quantity must be a positive integer" });
  const result = await pool.query(`
    UPDATE cart_items ci SET quantity=$1
    FROM carts c, products p
    WHERE ci.id=$2 AND ci.cart_id=c.id AND ci.product_id=p.id
      AND c.user_id=$3 AND quantity <= p.stock
    RETURNING ci.id`, [quantity, req.params.itemId, req.params.userId]);
  if (!result.rowCount) return res.status(409).json({ error: "Cannot update item" });
  res.json(await getCart(req.params.userId));
});

app.delete("/api/cart/:userId/items/:itemId", async (req, res) => {
  await pool.query(`
    DELETE FROM cart_items ci USING carts c
    WHERE ci.id=$1 AND ci.cart_id=c.id AND c.user_id=$2`,
    [req.params.itemId, req.params.userId]);
  res.status(204).end();
});

app.post("/api/orders", async (req, res) => {
  const userId = Number(req.body.userId);
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    const cart = await client.query(`
      SELECT ci.product_id, ci.quantity, p.price, p.stock
      FROM cart_items ci JOIN carts c ON c.id=ci.cart_id
      JOIN products p ON p.id=ci.product_id
      WHERE c.user_id=$1 FOR UPDATE`, [userId]);

    if (!cart.rowCount) {
      await client.query("ROLLBACK");
      return res.status(400).json({ error: "Cart is empty" });
    }
    for (const item of cart.rows)
      if (item.quantity > item.stock) {
        await client.query("ROLLBACK");
        return res.status(409).json({ error: "Not enough stock" });
      }

    const total = cart.rows.reduce((s, x) => s + Number(x.price) * x.quantity, 0);
    const order = await client.query(
      "INSERT INTO orders(user_id,total) VALUES($1,$2) RETURNING *",
      [userId, total.toFixed(2)]
    );
    for (const item of cart.rows) {
      await client.query(
        "INSERT INTO order_items(order_id,product_id,quantity,price) VALUES($1,$2,$3,$4)",
        [order.rows[0].id, item.product_id, item.quantity, item.price]
      );
      await client.query("UPDATE products SET stock=stock-$1 WHERE id=$2",
        [item.quantity, item.product_id]);
    }
    await client.query("DELETE FROM cart_items WHERE cart_id=(SELECT id FROM carts WHERE user_id=$1)", [userId]);
    await client.query("COMMIT");
    res.status(201).json(order.rows[0]);
  } catch (e) {
    await client.query("ROLLBACK");
    res.status(500).json({ error: "Could not create order" });
  } finally { client.release(); }
});

app.get("/api/orders/:id", async (req, res) => {
  const order = await pool.query("SELECT * FROM orders WHERE id=$1", [req.params.id]);
  if (!order.rowCount) return res.status(404).json({ error: "Order not found" });
  const items = await pool.query(`
    SELECT oi.*, p.name FROM order_items oi JOIN products p ON p.id=oi.product_id
    WHERE oi.order_id=$1`, [req.params.id]);
  res.json({ ...order.rows[0], items: items.rows });
});

app.listen(process.env.PORT || 3000, () => console.log("API listening"));
