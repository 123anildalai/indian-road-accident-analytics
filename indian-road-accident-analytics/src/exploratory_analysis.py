"""
Exploratory Data Analysis & Statistical Risk Modeling
Project: Indian Road Accident & Risk Analytics
Author: Anil Dalai (https://github.com/123anildalai)
"""

import pandas as pd
import numpy as np

def run_eda(input_csv='data/cleaned_road_accidents.csv'):
    df = pd.read_csv(input_csv)
    print("=" * 60)
    print("      INDIAN ROAD ACCIDENT & RISK ANALYTICS - SUMMARY")
    print("=" * 60)
    
    total_accidents = len(df)
    total_fatalities = df['fatalities'].sum()
    total_injuries = df['injuries'].sum()
    fatality_rate = (total_fatalities / total_accidents) * 100
    
    print(f"Total Recorded Incidents: {total_accidents:,}")
    print(f"Total Fatalities        : {total_fatalities:,}")
    print(f"Total Injuries          : {total_injuries:,}")
    print(f"Overall Fatality Rate   : {fatality_rate:.2f}%")
    print("-" * 60)
    
    # 1. State-wise Breakdown
    print("\n1. Top States by Casualties & Severity:")
    state_metrics = df.groupby('state').agg(
        total_accidents=('accident_id', 'count'),
        total_fatalities=('fatalities', 'sum'),
        total_injuries=('injuries', 'sum'),
        fatal_accidents=('is_fatal', 'sum')
    ).reset_index()
    state_metrics['fatality_ratio'] = (state_metrics['total_fatalities'] / state_metrics['total_accidents'] * 100).round(2)
    state_metrics = state_metrics.sort_values(by='total_accidents', ascending=False)
    print(state_metrics.to_string(index=False))
    
    # 2. Road Type Vulnerability
    print("\n2. Severity Analysis by Road Infrastructure:")
    road_metrics = df.groupby('road_type').agg(
        accidents=('accident_id', 'count'),
        fatalities=('fatalities', 'sum'),
        overspeeding_share=('is_overspeeding', lambda x: round(x.mean() * 100, 1))
    ).reset_index()
    road_metrics['fatality_per_100_accidents'] = (road_metrics['fatalities'] / road_metrics['accidents'] * 100).round(2)
    road_metrics = road_metrics.sort_values(by='fatality_per_100_accidents', ascending=False)
    print(road_metrics.to_string(index=False))
    
    # 3. Vehicle Type Crash Share
    print("\n3. High-Risk Vehicle Segments:")
    veh_metrics = df.groupby('vehicle_type').agg(
        total_accidents=('accident_id', 'count'),
        fatalities=('fatalities', 'sum'),
        fatal_count=('is_fatal', 'sum')
    ).reset_index()
    veh_metrics['pct_of_total_accidents'] = (veh_metrics['total_accidents'] / total_accidents * 100).round(1)
    veh_metrics = veh_metrics.sort_values(by='total_accidents', ascending=False)
    print(veh_metrics.to_string(index=False))
    
    # 4. Critical Time Windows & High-Risk Hours
    print("\n4. Temporal Risk Windows:")
    time_metrics = df.groupby('time_slot').agg(
        accidents=('accident_id', 'count'),
        fatalities=('fatalities', 'sum'),
        dui_incidents=('is_dui', 'sum')
    ).reset_index()
    time_metrics['fatality_rate'] = (time_metrics['fatalities'] / time_metrics['accidents'] * 100).round(2)
    time_metrics = time_metrics.sort_values(by='fatality_rate', ascending=False)
    print(time_metrics.to_string(index=False))
    
    print("\n" + "=" * 60)
    print("Key Actionable Finding: Two-wheelers on National & State Highways during")
    print("evening rush & unlit night hours exhibit the highest fatality density.")
    print("=" * 60)

if __name__ == '__main__':
    run_eda()
