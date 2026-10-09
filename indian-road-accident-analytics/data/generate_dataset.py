import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_accident_data(num_records=5000, random_seed=42):
    np.random.seed(random_seed)
    random.seed(random_seed)
    
    states_cities = {
        'Odisha': ['Bhubaneswar', 'Cuttack', 'Rourkela', 'Sambalpur', 'Berhampur', 'Balasore'],
        'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Thane'],
        'Karnataka': ['Bengaluru', 'Mysuru', 'Hubballi', 'Mangaluru'],
        'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli'],
        'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Varanasi', 'Noida', 'Agra'],
        'Delhi NCR': ['New Delhi', 'South Delhi', 'North Delhi', 'East Delhi'],
        'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot']
    }
    
    state_weights = np.array([0.20, 0.18, 0.15, 0.15, 0.12, 0.10, 0.10])
    state_weights = state_weights / state_weights.sum()
    states = list(states_cities.keys())
    
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 9, 30)
    delta_days = (end_date - start_date).days
    
    data = []
    road_types = ['National Highway', 'State Highway', 'Expressway', 'Urban Arterial', 'Rural Local Road']
    road_p = np.array([0.35, 0.25, 0.15, 0.15, 0.10])
    road_p = road_p / road_p.sum()
    
    weather_conds = ['Clear', 'Rainy', 'Dense Fog', 'Heavy Monsoon', 'Overcast']
    weather_p = np.array([0.60, 0.18, 0.10, 0.08, 0.04])
    weather_p = weather_p / weather_p.sum()
    
    vehicle_types = ['Two-Wheeler', 'Four-Wheeler (Car/SUV)', 'Commercial Truck', 'Bus', 'Auto-Rickshaw']
    vehicle_p = np.array([0.42, 0.28, 0.16, 0.08, 0.06])
    vehicle_p = vehicle_p / vehicle_p.sum()
    
    factors = ['Overspeeding', 'Dangerous Overtaking', 'Driving Under Influence', 'Poor Road Condition', 'Adverse Weather', 'Traffic Rule Violation']
    age_groups = ['18-25', '26-35', '36-50', '51-65', '65+']
    age_p = np.array([0.32, 0.38, 0.18, 0.09, 0.03])
    age_p = age_p / age_p.sum()
    
    hour_weights = np.array([
        2, 2, 2, 2, 3, 4,
        5, 6, 7, 6, 4, 4,
        4, 4, 4, 5, 6, 7,
        8, 7, 5, 4, 3, 3
    ], dtype=float)
    hour_weights = hour_weights / hour_weights.sum()
    
    for i in range(1, num_records + 1):
        accident_id = f"IND-ACC-{i:05d}"
        
        # State & City
        chosen_state = np.random.choice(states, p=state_weights)
        chosen_city = random.choice(states_cities[chosen_state])
        
        # Date & Time
        random_days = random.randint(0, delta_days)
        acc_date = start_date + timedelta(days=random_days)
        hour = np.random.choice(range(24), p=hour_weights)
        minute = random.randint(0, 59)
        time_str = f"{hour:02d}:{minute:02d}"
        
        area_type = 'Urban' if random.random() < 0.62 else 'Rural'
        road_type = np.random.choice(road_types, p=road_p)
        weather = np.random.choice(weather_conds, p=weather_p)
        
        if 6 <= hour <= 17:
            lighting = 'Daylight'
        elif 18 <= hour <= 19 or 5 <= hour < 6:
            lighting = 'Dusk/Dawn'
        else:
            lighting = 'Night - Lit' if area_type == 'Urban' and random.random() < 0.7 else 'Night - Unlit'
            
        vehicle = np.random.choice(vehicle_types, p=vehicle_p)
        age_group = np.random.choice(age_groups, p=age_p)
        
        dui = 'Yes' if (lighting in ['Night - Lit', 'Night - Unlit'] and random.random() < 0.22) else ('Yes' if random.random() < 0.05 else 'No')
        overspeeding = 'Yes' if (road_type in ['National Highway', 'Expressway'] and random.random() < 0.55) else ('Yes' if random.random() < 0.35 else 'No')
        safety_gear = 'Yes' if (vehicle in ['Two-Wheeler', 'Four-Wheeler (Car/SUV)'] and random.random() < 0.58) else 'No'
        
        # Severity calculation
        risk_score = 0
        if road_type in ['National Highway', 'Expressway']: risk_score += 2
        if overspeeding == 'Yes': risk_score += 2
        if dui == 'Yes': risk_score += 3
        if lighting == 'Night - Unlit': risk_score += 2
        if vehicle == 'Two-Wheeler': risk_score += 2
        if safety_gear == 'No': risk_score += 2
        if weather in ['Heavy Monsoon', 'Dense Fog']: risk_score += 1
        
        if risk_score >= 8 and random.random() < 0.55:
            severity = 'Fatal'
            fatalities = random.randint(1, 3)
            injuries = random.randint(0, 4)
        elif risk_score >= 5:
            severity = 'Grievous Injury'
            fatalities = 0
            injuries = random.randint(1, 4)
        elif risk_score >= 3:
            severity = 'Minor Injury'
            fatalities = 0
            injuries = random.randint(1, 2)
        else:
            severity = 'Non-Injury / Property Damage'
            fatalities = 0
            injuries = 0
            
        if dui == 'Yes' and random.random() < 0.6:
            factor = 'Driving Under Influence'
        elif overspeeding == 'Yes' and random.random() < 0.6:
            factor = 'Overspeeding'
        else:
            factor = np.random.choice(factors)
            
        data.append({
            'accident_id': accident_id,
            'date': acc_date.strftime('%Y-%m-%d'),
            'year': acc_date.year,
            'month': acc_date.strftime('%b'),
            'day_of_week': acc_date.strftime('%A'),
            'time': time_str,
            'hour': hour,
            'state': chosen_state,
            'city': chosen_city,
            'area_type': area_type,
            'road_type': road_type,
            'weather_condition': weather,
            'lighting_condition': lighting,
            'vehicle_type': vehicle,
            'driver_age_group': age_group,
            'alcohol_involved': dui,
            'overspeeding': overspeeding,
            'safety_gear_used': safety_gear,
            'contributing_factor': factor,
            'accident_severity': severity,
            'fatalities': fatalities,
            'injuries': injuries,
            'total_casualties': fatalities + injuries
        })
        
    df = pd.DataFrame(data)
    output_path = 'projects/indian-road-accident-analytics/data/indian_road_accidents.csv'
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} records successfully at {output_path}")

if __name__ == '__main__':
    generate_accident_data()
