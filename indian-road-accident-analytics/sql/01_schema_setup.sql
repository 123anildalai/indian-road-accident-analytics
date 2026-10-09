-- ====================================================================
-- Database Schema: Indian Road Accident & Risk Analytics
-- Author: Anil Dalai (https://github.com/123anildalai)
-- Engine: MySQL 8.0+ / PostgreSQL Compatible DDL
-- ====================================================================

DROP TABLE IF EXISTS road_accidents;

CREATE TABLE road_accidents (
    accident_id VARCHAR(20) PRIMARY KEY,
    accident_date DATE NOT NULL,
    year_val INT NOT NULL,
    month_name VARCHAR(10) NOT NULL,
    day_name VARCHAR(15) NOT NULL,
    time_val TIME NOT NULL,
    hour_val INT NOT NULL,
    state VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    area_type ENUM('Urban', 'Rural') NOT NULL,
    road_type VARCHAR(50) NOT NULL,
    weather_condition VARCHAR(50) NOT NULL,
    lighting_condition VARCHAR(50) NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL,
    driver_age_group VARCHAR(20) NOT NULL,
    alcohol_involved ENUM('Yes', 'No') NOT NULL,
    overspeeding ENUM('Yes', 'No') NOT NULL,
    safety_gear_used ENUM('Yes', 'No') NOT NULL,
    contributing_factor VARCHAR(100) NOT NULL,
    accident_severity VARCHAR(50) NOT NULL,
    fatalities INT DEFAULT 0,
    injuries INT DEFAULT 0,
    total_casualties INT DEFAULT 0,
    INDEX idx_state_city (state, city),
    INDEX idx_date (accident_date),
    INDEX idx_road_severity (road_type, accident_severity)
);
