-- 1. Average yield by crop and province
SELECT crop, province, ROUND(AVG(yield_kg_ha), 1) AS avg_yield
FROM yields
GROUP BY crop, province
ORDER BY crop, avg_yield DESC;

-- 2. Year-over-year change in yield
SELECT crop, province, year, yield_kg_ha,
       ROUND(yield_kg_ha - LAG(yield_kg_ha) OVER (
           PARTITION BY crop, province ORDER BY year), 1) AS change_from_prev_year
FROM yields
ORDER BY crop, province, year;

-- 3. Top 3 provinces for each crop
WITH avg_yields AS (
    SELECT crop, province, AVG(yield_kg_ha) AS avg_yield
    FROM yields
    GROUP BY crop, province
),
ranked AS (
    SELECT crop, province, ROUND(avg_yield, 1) AS avg_yield,
           RANK() OVER (PARTITION BY crop ORDER BY avg_yield DESC) AS rnk
    FROM avg_yields
)
SELECT * FROM ranked WHERE rnk <= 3 ORDER BY crop, rnk;

-- 4. Best and worst year for each crop (average across provinces)
WITH yearly AS (
    SELECT crop, year, AVG(yield_kg_ha) AS avg_yield
    FROM yields
    GROUP BY crop, year
),
ranked AS (
    SELECT crop, year, ROUND(avg_yield, 1) AS avg_yield,
           ROW_NUMBER() OVER (PARTITION BY crop ORDER BY avg_yield DESC) AS best_rank,
           ROW_NUMBER() OVER (PARTITION BY crop ORDER BY avg_yield ASC) AS worst_rank
    FROM yearly
)
SELECT crop, year, avg_yield,
       CASE WHEN best_rank = 1 THEN 'Best year' ELSE 'Worst year' END AS type
FROM ranked
WHERE best_rank = 1 OR worst_rank = 1
ORDER BY crop, type;

-- 5. Five-year moving average of yield
SELECT crop, province, year, yield_kg_ha,
       ROUND(AVG(yield_kg_ha) OVER (
           PARTITION BY crop, province
           ORDER BY year
           ROWS BETWEEN 4 PRECEDING AND CURRENT ROW), 1) AS moving_avg_5yr
FROM yields
ORDER BY crop, province, year;