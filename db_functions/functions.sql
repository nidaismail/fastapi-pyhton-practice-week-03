-- Examples - Practice: join tables

-- Practice Task 1 - Every customer's orders
SELECT
    c.company_name,
    COUNT(o.order_id) AS total_orders
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.company_name
ORDER BY total_orders ASC;

--Practice Task 2 -  Orders per employee.
SELECT
    e.first_name,
    e.last_name,
    COUNT(o.order_id) AS total_orders
FROM employees AS e
LEFT JOIN orders AS o
    ON e.employee_id = o.employee_id
GROUP BY e.employee_id, e.first_name, e.last_name
ORDER BY total_orders DESC;
 
--Practice task 3 - The best customers
SELECT
    c.company_name,
    SUM(od.unit_price * od.quantity * (1 - od.discount)) AS total_spent
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
JOIN order_details AS od
    ON o.order_id = od.order_id
GROUP BY c.customer_id, c.company_name
ORDER BY total_spent DESC
LIMIT 5;                