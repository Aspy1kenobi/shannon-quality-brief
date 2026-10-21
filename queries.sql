-- Shannon Medical Center vs. West Texas peer hospitals
-- Source: CMS Care Compare (data.cms.gov/provider-data)
--   Hospital General Information (xubh-q36u)
--   HCAHPS Patient Survey, hospital level (dgck-syfz), period 10/01/2024 - 09/30/2025
-- Run with: duckdb < queries.sql   (or python run.py)

CREATE OR REPLACE TABLE hospitals AS SELECT * FROM read_csv_auto('data/hospitals.csv');
CREATE OR REPLACE TABLE hcahps    AS SELECT * FROM read_csv_auto('data/hcahps.csv');

-- Q1. Outcomes scorecard: how many CMS outcome measures is each hospital
--     statistically BETTER or WORSE than the national rate on?
--     (mortality + safety + readmission groups combined)
SELECT short_name,
       overall_star,
       mort_better + safety_better + readm_better AS measures_better,
       mort_worse  + safety_worse  + readm_worse  AS measures_worse,
       (mort_better + safety_better + readm_better)
     - (mort_worse  + safety_worse  + readm_worse) AS net_score
FROM hospitals
ORDER BY net_score DESC, measures_worse;

-- Q2. Patient experience: where does Shannon rank in the peer group on each
--     HCAHPS dimension? (linear mean score 0-100, rank 1 = best of 9)
WITH ranked AS (
  SELECT h.short_name, c.measure, c.linear_mean, c.star_rating,
         RANK() OVER (PARTITION BY c.measure ORDER BY c.linear_mean DESC) AS peer_rank
  FROM hcahps c JOIN hospitals h USING (facility_id)
)
SELECT r.measure,
       r.linear_mean                                   AS shannon_score,
       r.star_rating                                   AS shannon_stars,
       r.peer_rank                                     AS shannon_rank_of_9,
       (SELECT ROUND(MEDIAN(linear_mean),1) FROM ranked p
         WHERE p.measure = r.measure AND p.short_name <> 'Shannon') AS peer_median,
       r.linear_mean - (SELECT MEDIAN(linear_mean) FROM ranked p
         WHERE p.measure = r.measure AND p.short_name <> 'Shannon') AS gap_vs_peer_median
FROM ranked r
WHERE r.short_name = 'Shannon'
ORDER BY gap_vs_peer_median;

-- Q3. Is Shannon's medicine-communication score a Shannon problem or a
--     regional one? Compare spread across the whole peer group.
SELECT measure,
       MIN(linear_mean) AS lowest,
       MAX(linear_mean) AS highest,
       ROUND(AVG(linear_mean),1) AS group_avg,
       SUM(CASE WHEN star_rating <= 2 THEN 1 ELSE 0 END) AS hospitals_at_2_stars_or_less
FROM hcahps
WHERE measure IN ('MEDICINE_COMM','CLEANLINESS','DOCTOR_COMM')
GROUP BY measure
ORDER BY measure;
