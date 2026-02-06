
INSERT INTO products (product_name, category, price)
SELECT
    'Product_' || gs,
    CASE
        WHEN random() < 0.30 THEN 'Electronics'
        WHEN random() < 0.55 THEN 'Clothing'
        WHEN random() < 0.75 THEN 'Home'
        ELSE 'Footwear'
    END,
    ROUND((random() * 500 + 10)::numeric, 2)
FROM generate_series(1, 200) gs;



INSERT INTO users (signup_date, country, platform, is_paid)
SELECT
    DATE '2023-10-01' + (random() * 120)::int,
    CASE
        WHEN random() < 0.35 THEN 'India'
        WHEN random() < 0.55 THEN 'US'
        WHEN random() < 0.70 THEN 'UK'
        WHEN random() < 0.85 THEN 'Germany'
        ELSE 'Canada'
    END,
    CASE
        WHEN random() < 0.65 THEN 'mobile'
        ELSE 'web'
    END,
    random() < 0.25
FROM generate_series(1, 50000);




INSERT INTO user_events (user_id, event_type, event_time)
SELECT
    u.user_id,
    CASE
        WHEN r < 0.45 THEN 'search'
        WHEN r < 0.75 THEN 'view_product'
        WHEN r < 0.90 THEN 'add_to_cart'
        ELSE 'checkout'
    END,
    u.signup_date
        + (random() * 14)::int * INTERVAL '1 day'
        + (random() * 24)::int * INTERVAL '1 hour'
FROM (
    SELECT
        user_id,
        signup_date,
        random() AS r
    FROM users
    CROSS JOIN generate_series(1, 20)  
) u;



INSERT INTO orders (user_id, order_date, total_amount)
SELECT
    user_id,
    signup_date + (random() * 30)::int * INTERVAL '1 day',
    ROUND((random() * 300 + 20)::numeric, 2)
FROM users
WHERE random() < 0.40;



INSERT INTO order_items (order_id, product_id, quantity)
SELECT
    o.order_id,
    (random() * 199 + 1)::int,
    (random() * 3 + 1)::int
FROM orders o
CROSS JOIN generate_series(1, 2);
