-- ====================================================================
-- Analytical Queries: Indian Road Accident & Risk Analytics
-- Author: Anil Dalai (https://github.com/123anildalai)
-- Description: Core analytical metrics, CTEs, Window Functions, and KPI calculations
-- ====================================================================

-- 1. Executive KPI Summary (Total Incidents, Fatalities, Fatality Rate, Casualty Ratio)
SELECT 
    COUNT(accident_id) AS total_incidents,
    SUM(fatalities) AS total_fatalities,
    SUM(injuries) AS total_injuries,
    SUM(total_casualties) AS total_casualties,
    ROUND(SUM(fatalities) * 100.0 / COUNT(accident_id), 2) AS fatality_rate_pct,
    ROUND(SUM(total_casualties) * 1.0 / COUNT(accident_id), 2) AS avg_casualty_per_accident
FROM road_accidents;

-- 2. State-Wise Risk Ranking (Window Function: DENSE_RANK & Running Totals)
WITH StateSummary AS (
    SELECT 
        state,
        COUNT(accident_id) AS incident_count,
        SUM(fatalities) AS total_fatalities,
        SUM(injuries) AS total_injuries,
        ROUND(SUM(fatalities) * 100.0 / COUNT(accident_id), 2) AS fatality_rate
    FROM road_accidents
    GROUP BY state
)
SELECT 
    state,
    incident_count,
    total_fatalities,
    total_injuries,
    fatality_rate,
    DENSE_RANK() OVER (ORDER BY total_fatalities DESC) AS state_fatality_rank,
    ROUND(total_fatalities * 100.0 / SUM(total_fatalities) OVER (), 2) AS pct_share_national_fatalities
FROM StateSummary
ORDER BY total_fatalities DESC;

-- 3. High-Risk Road Infrastructure & Overspeeding Correlation
SELECT 
    road_type,
    COUNT(accident_id) AS total_accidents,
    SUM(CASE WHEN overspeeding = 'Yes' THEN 1 ELSE 0 END) AS overspeeding_accidents,
    ROUND(SUM(CASE WHEN overspeeding = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(accident_id), 2) AS overspeeding_pct,
    SUM(fatalities) AS total_fatalities,
    ROUND(SUM(fatalities) * 100.0 / COUNT(accident_id), 2) AS fatality_rate_pct
FROM road_accidents
GROUP BY road_type
ORDER BY fatality_rate_pct DESC;

-- 4. Vehicle Vulnerability Matrix (Two-Wheelers vs Other Modes)
SELECT 
    vehicle_type,
    COUNT(accident_id) AS total_crashes,
    SUM(CASE WHEN safety_gear_used = 'No' THEN 1 ELSE 0 END) AS no_safety_gear_count,
    ROUND(SUM(CASE WHEN safety_gear_used = 'No' THEN 1 ELSE 0 END) * 100.0 / COUNT(accident_id), 2) AS no_safety_gear_pct,
    SUM(fatalities) AS fatal_casualties,
    ROUND(SUM(fatalities) * 100.0 / SUM(SUM(fatalities)) OVER (), 2) AS pct_of_all_fatalities
FROM road_accidents
GROUP BY vehicle_type
ORDER BY fatal_casualties DESC;

-- 5. Time-of-Day Risk & DUI Cluster Identification (CTE with Hour Bins)
WITH HourlyProfile AS (
    SELECT 
        hour_val,
        CASE 
            WHEN hour_val BETWEEN 0 AND 4 THEN 'Late Night (00-04)'
            WHEN hour_val BETWEEN 5 AND 8 THEN 'Early Morning (05-08)'
            WHEN hour_val BETWEEN 9 AND 11 THEN 'Morning Peak (09-11)'
            WHEN hour_val BETWEEN 12 AND 15 THEN 'Afternoon (12-15)'
            WHEN hour_val BETWEEN 16 AND 19 THEN 'Evening Peak (16-19)'
            ELSE 'Night (20-23)'
        END AS time_window,
        accident_id,
        fatalities,
        alcohol_involved
    FROM road_accidents
)
SELECT 
    time_window,
    COUNT(accident_id) AS total_accidents,
    SUM(CASE WHEN alcohol_involved = 'Yes' THEN 1 ELSE 0 END) AS dui_accidents,
    ROUND(SUM(CASE WHEN alcohol_involved = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(accident_id), 2) AS dui_percentage,
    SUM(fatalities) AS fatalities,
    ROUND(SUM(fatalities) * 100.0 / COUNT(accident_id), 2) AS fatality_risk_index
FROM HourlyProfile
GROUP BY time_window
ORDER BY fatality_risk_index DESC;

-- 6. Month-Over-Month Incident Trend with LAG Window Function
WITH MonthlyTrends AS (
    SELECT 
        year_val,
        month_name,
        MIN(accident_date) AS min_date,
        COUNT(accident_id) AS current_month_incidents,
        SUM(fatalities) AS current_month_fatalities
    FROM road_accidents
    GROUP BY year_val, month_name
)
SELECT 
    year_val,
    month_name,
    current_month_incidents,
    LAG(current_month_incidents, 1) OVER (ORDER BY min_date) AS prev_month_incidents,
    ROUND((current_month_incidents - LAG(current_month_incidents, 1) OVER (ORDER BY min_date)) * 100.0 / 
          NULLIF(LAG(current_month_incidents, 1) OVER (ORDER BY min_date), 0), 2) AS mom_incident_growth_pct,
    current_month_fatalities
FROM MonthlyTrends
ORDER BY min_date;
