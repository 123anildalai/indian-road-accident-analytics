"""
Data Cleaning & Preprocessing Pipeline
Project: Indian Road Accident & Risk Analytics
Author: Anil Dalai (https://github.com/123anildalai)
"""

import pandas as pd
import numpy as np

def clean_and_preprocess(input_csv='data/indian_road_accidents.csv', output_csv='data/cleaned_road_accidents.csv'):
    print("Loading raw accident dataset...")
    df = pd.read_csv(input_csv)
    initial_shape = df.shape
    print(f"Loaded {initial_shape[0]} rows and {initial_shape[1]} columns.")
    
    # 1. Standardize text columns
    text_cols = ['state', 'city', 'area_type', 'road_type', 'weather_condition', 
                 'lighting_condition', 'vehicle_type', 'driver_age_group', 
                 'alcohol_involved', 'overspeeding', 'safety_gear_used', 
                 'contributing_factor', 'accident_severity']
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()
        
    # 2. Parse Date and Time
    df['date'] = pd.to_datetime(df['date'])
    df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday']).astype(int)
    
    # 3. Time of Day Bins
    def categorize_time_of_day(hour):
        if 5 <= hour < 9:
            return 'Early Morning'
        elif 9 <= hour < 12:
            return 'Morning Rush'
        elif 12 <= hour < 16:
            return 'Afternoon'
        elif 16 <= hour < 20:
            return 'Evening Rush'
        elif 20 <= hour < 23:
            return 'Night'
        else:
            return 'Late Night / Midnight'
            
    df['time_slot'] = df['hour'].apply(categorize_time_of_day)
    
    # 4. Binary Flags for Fast Metric Calculation
    df['is_fatal'] = (df['accident_severity'] == 'Fatal').astype(int)
    df['is_grievous'] = (df['accident_severity'] == 'Grievous Injury').astype(int)
    df['is_dui'] = (df['alcohol_involved'] == 'Yes').astype(int)
    df['is_overspeeding'] = (df['overspeeding'] == 'Yes').astype(int)
    
    # 5. Data Validation & Integrity Checks
    assert (df['fatalities'] < 0).sum() == 0, "Fatalities count contains negative values"
    assert (df['injuries'] < 0).sum() == 0, "Injuries count contains negative values"
    
    # Ensure total_casualties matches
    df['total_casualties'] = df['fatalities'] + df['injuries']
    
    # Save cleaned dataset
    df.to_csv(output_csv, index=False)
    print(f"Cleaned dataset saved successfully to {output_csv}. Shape: {df.shape}")
    return df

if __name__ == '__main__':
    clean_and_preprocess()
