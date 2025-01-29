SELECT DISTINCT status
FROM projects_task
ORDER BY status;

SELECT project_id, COUNT(*) AS task_count
FROM projects_task
GROUP BY project_id
ORDER BY task_count DESC;

SELECT p.name, COUNT(t.id) AS task_count
FROM projects_project p
LEFT JOIN projects_task t ON p.id = t.project_id
GROUP BY p.id
ORDER BY p.name;

SELECT t.*
FROM projects_task t
JOIN projects_project p ON t.project_id = p.id
WHERE p.name LIKE 'N%'
ORDER BY t.name;

SELECT p.name, COUNT(t.id) AS task_count
FROM projects_project p
LEFT JOIN projects_task t ON p.id = t.project_id
WHERE p.name LIKE '%a%' AND LENGTH(p.name) > 1
GROUP BY p.id
ORDER BY p.name;

SELECT name
FROM projects_task
GROUP BY name
HAVING COUNT(*) > 1
ORDER BY name;

SELECT t.name, t.status, COUNT(*) AS matches_count
FROM projects_task t
JOIN projects_project p ON t.project_id = p.id
WHERE p.name = 'Delivery'
GROUP BY t.name, t.status
HAVING COUNT(*) > 1
ORDER BY matches_count DESC;

SELECT p.name
FROM projects_project p
JOIN projects_task t ON p.id = t.project_id
WHERE t.status = TRUE
GROUP BY p.id
HAVING COUNT(t.id) > 10
ORDER BY p.id;