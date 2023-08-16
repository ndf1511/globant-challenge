WITH grouped_by_department_year AS (
	SELECT E.department_id, D.department, EXTRACT(YEAR FROM datetime) as year, count(distinct E.id) as hired
	FROM employees E
	INNER JOIN departments D
	ON E.department_id = D.id
	GROUP BY E.department_id, D.department, EXTRACT(YEAR FROM datetime)
),
mean_calc AS (
	SELECT AVG(hired) as hired_mean_2021
	FROM grouped_by_department_year
	WHERE year = 2021
)
SELECT department_id, department, hired
FROM 
( 
	SELECT department_id, department, SUM(hired) as hired
	FROM grouped_by_department_year
	GROUP BY 1,2
) grouped_by_department
WHERE hired >
(
	SELECT hired_mean_2021
	FROM mean_calc
)
ORDER BY hired DESC