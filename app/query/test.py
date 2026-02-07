from query_executor import QueryExecutor

executor = QueryExecutor()

sql = """
SELECT event_type, COUNT(*) AS cnt
FROM user_events
GROUP BY event_type
LIMIT 5;
"""

rows = executor.execute(sql)
print(rows)

executor.close()
