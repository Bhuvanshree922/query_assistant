-- Most used feature in first week

SELECT
    ue.event_type,
    COUNT(DISTINCT ue.user_id) AS users
FROM user_events ue
JOIN users u ON ue.user_id = u.user_id
WHERE ue.event_time <= u.signup_date + INTERVAL '7 days'
GROUP BY ue.event_type
ORDER BY users DESC
LIMIT 5;

-- Compare mobile vs web usage
SELECT
    u.platform,
    ue.event_type,
    COUNT(DISTINCT ue.user_id) AS users
FROM user_events ue
JOIN users u ON ue.user_id = u.user_id
GROUP BY u.platform, ue.event_type
ORDER BY u.platform, users DESC;

-- Top countries by checkout activity

SELECT
    u.country,
    COUNT(DISTINCT ue.user_id) AS users
FROM user_events ue
JOIN users u ON ue.user_id = u.user_id
WHERE ue.event_type = 'checkout'
GROUP BY u.country
ORDER BY users DESC
LIMIT 5;

-- Actions before first order

SELECT
    ue.event_type,
    COUNT(*) AS occurrences
FROM user_events ue
JOIN orders o ON ue.user_id = o.user_id
WHERE ue.event_time < o.order_date
GROUP BY ue.event_type
ORDER BY occurrences DESC;

-- Paid vs free user behavior

SELECT
    u.is_paid,
    ue.event_type,
    COUNT(DISTINCT ue.user_id) AS users
FROM user_events ue
JOIN users u ON ue.user_id = u.user_id
GROUP BY u.is_paid, ue.event_type
ORDER BY u.is_paid, users DESC;

-- First-week vs later behavior

SELECT
    CASE
        WHEN ue.event_time <= u.signup_date + INTERVAL '7 days'
        THEN 'first_week'
        ELSE 'later'
    END AS period,
    ue.event_type,
    COUNT(DISTINCT ue.user_id) AS users
FROM user_events ue
JOIN users u ON ue.user_id = u.user_id
GROUP BY period, ue.event_type
ORDER BY period, users DESC;
