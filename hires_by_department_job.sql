SELECT job, department, 
	SUM(CASE WHEN quarter = 1 then 1 else 0 end) as Q1,
	SUM(CASE WHEN quarter = 2 then 1 else 0 end) as Q2,
	SUM(CASE WHEN quarter = 3 then 1 else 0 end) as Q3,
	SUM(CASE WHEN quarter = 4 then 1 else 0 end) as Q4
FROM	
(
	SELECT 
		E.id,
		J.job,
		D.department,
		EXTRACT(QUARTER FROM E.datetime) AS quarter
	FROM employees E
	INNER JOIN jobs J
	ON E.job_id = J.id
	INNER JOIN departments D
	ON E.department_id = D.id
	WHERE EXTRACT(YEAR FROM datetime) = 2021
) as filtered_table
GROUP BY job, department
ORDER BY department asc, job asc