# Power BI Dashboard Specification & DAX Measures

**Project**: Indian Road Accident & Risk Analytics  
**Author**: Anil Dalai ([GitHub Profile](https://github.com/123anildalai))

---

## 1. Data Model Architecture (Star Schema)

- **Fact Table**: `Fact_RoadAccidents`
- **Dimension Tables**:
  - `Dim_Calendar` (Date, Year, Quarter, Month, Weekday, IsWeekend)
  - `Dim_Location` (State, City, Area_Type)
  - `Dim_RoadInfrastructure` (Road_Type, Speed_Limit_Category)
  - `Dim_Vehicle` (Vehicle_Type, Safety_Category)

---

## 2. Core DAX Formulations

### Primary KPI Measures

```dax
// 1. Total Incidents
Total Accidents = COUNTROWS('Fact_RoadAccidents')

// 2. Total Fatalities
Total Fatalities = SUM('Fact_RoadAccidents'[fatalities])

// 3. Total Injuries
Total Injuries = SUM('Fact_RoadAccidents'[injuries])

// 4. Overall Casualties
Total Casualties = [Total Fatalities] + [Total Injuries]

// 5. Fatality Rate (%)
Fatality Rate % = 
DIVIDE(
    [Total Fatalities], 
    [Total Accidents], 
    0
)

// 6. Average Casualties Per Incident
Avg Casualties Per Incident = 
DIVIDE(
    [Total Casualties], 
    [Total Accidents], 
    0
)
```

### Behavioral & Risk Ratio Measures

```dax
// 7. Overspeeding Involvement Rate (%)
Overspeeding Share % = 
DIVIDE(
    CALCULATE([Total Accidents], 'Fact_RoadAccidents'[overspeeding] = "Yes"),
    [Total Accidents],
    0
)

// 8. DUI Accident Rate (%)
DUI Incident Share % = 
DIVIDE(
    CALCULATE([Total Accidents], 'Fact_RoadAccidents'[alcohol_involved] = "Yes"),
    [Total Accidents],
    0
)

// 9. Two-Wheeler Fatality Contribution (%)
Two-Wheeler Fatality Share % = 
DIVIDE(
    CALCULATE([Total Fatalities], 'Fact_RoadAccidents'[vehicle_type] = "Two-Wheeler"),
    [Total Fatalities],
    0
)

// 10. Month-over-Month Incident Growth (%)
MoM Accident Growth % = 
VAR PrevMonthAccidents = 
    CALCULATE(
        [Total Accidents], 
        DATEADD('Dim_Calendar'[Date], -1, MONTH)
    )
RETURN
    DIVIDE(
        [Total Accidents] - PrevMonthAccidents, 
        PrevMonthAccidents, 
        0
    )
```

---

## 3. Dashboard Layout & Visual Architecture

### Page 1: Executive KPI Command Center
- **Top Ribbon Cards**: `Total Accidents`, `Total Fatalities`, `Fatality Rate %`, `DUI Share %`, `Overspeeding %`
- **Map Visual**: Geospatial bubble map displaying accident density and fatalities by Indian state/city.
- **Trend Line**: Monthly accident and casualty trajectory over 2025–2026.
- **Donut Chart**: Accident severity distribution (Fatal, Grievous, Minor, Property Damage).

### Page 2: Road Infrastructure & Vehicle Vulnerability
- **Clustered Bar Chart**: Fatality rate per 100 accidents across road types (Expressways, National Highways, State Highways, Urban Arterials).
- **Matrix Visual**: Vehicle type cross-analyzed with safety gear compliance (Helmets/Seatbelts) vs. fatality outcome.
- **Top 10 Risk Locations**: Ranked cities with highest accident severity index.

### Page 3: Temporal & Behavioral Root-Cause
- **24-Hour Heatmap Matrix**: Incident density across hours of the day (00:00 to 23:00) vs. Day of week.
- **Scatter Plot**: Correlation between DUI incidents and night-time crash fatalities.
- **Slicers**: State, Road Type, Vehicle Category, Year/Month.
