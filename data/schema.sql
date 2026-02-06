-- USERS: one row per customer
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    signup_date DATE NOT NULL,
    country VARCHAR(50),
    platform VARCHAR(20) CHECK (platform IN ('web', 'mobile')),
    is_paid BOOLEAN DEFAULT FALSE
);

-- PRODUCTS: catalog of items
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price NUMERIC(10,2) CHECK (price >= 0)
);

-- ORDERS: each order belongs to ONE user
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id),
    order_date TIMESTAMP NOT NULL,
    total_amount NUMERIC(10,2) CHECK (total_amount >= 0)
);

-- ORDER_ITEMS: line items inside an order
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(order_id),
    product_id INT NOT NULL REFERENCES products(product_id),
    quantity INT CHECK (quantity > 0)
);

-- USER_EVENTS: every action a user takesuser
CREATE TABLE user_events (
    event_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id),
    event_type VARCHAR(50) NOT NULL,
    event_time TIMESTAMP NOT NULL
);
