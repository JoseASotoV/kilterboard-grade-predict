import json
import pandas as pd
import re

# Load grades from JSON file
def load_grades(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Map average difficulty to grade
def map_difficulty(average_difficulty, grades):
    index = int(round(average_difficulty))
    if index < 0 or index >= len(grades):
        return "Unknown"
    grade = grades[index]['boulder_name']
    # Extract the V* part, allowing for one or more digits and optional '+'
    v_grade = re.search(r'V\d+\+?', grade)
    return v_grade.group() if v_grade else "Unknown"

# Load grades
grades = load_grades('./grades.json')

# Read the climbs JSON file
with open('../data/climbs_data.json', 'r') as file:
    data = json.load(file)

# Function to create a row for each angle
def create_rows(climb):
    rows = []
    
    if not isinstance(climb.get('placements'), list):
        return rows

    placements = {}
    for p in climb['placements']:
        if 'ledPosition' in p and 'type' in p:
            placements[p['ledPosition']] = p['type']
    
    if not isinstance(climb.get('climb_stats'), list):
        return rows

    for stat in climb['climb_stats']:
        try:
            row = {
                'uuid': climb['uuid'],
                'angle': stat['angle'],
                'difficulty_average': stat['difficulty_average'],
                'ascensionist_count': stat['ascensionist_count'],
                'boulder_grade': map_difficulty(stat['difficulty_average'], grades)
            }
        except KeyError:
            continue
        
        for i in range(0, 477):
            row[f'led_{i}'] = placements.get(i, 'NOT_USED')
        
        rows.append(row)
    
    return rows

# Process all climbs with layout_id = 1
all_rows = []
total_climbs = 0
processed_climbs = 0

for climb in data:
    total_climbs += 1
    if climb.get('layout_id') == 1:
        processed_climbs += 1
        all_rows.extend(create_rows(climb))

# Create DataFrame
df = pd.DataFrame(all_rows)

# Reorder columns
led_columns = [f'led_{i}' for i in range(0, 477)]
column_order = ['uuid', 'angle', 'difficulty_average', 'boulder_grade', 'ascensionist_count'] + led_columns
df = df[column_order]

# Print information about the data
print(f"Total climbs in JSON: {total_climbs}")
print(f"Climbs processed (layout_id = 1): {processed_climbs}")
print(f"Total rows in DataFrame: {len(df)}")
print(f"DataFrame shape: {df.shape}")
print("\nFirst few rows:")
print(df.head())
print("\nLast few rows:")
print(df.tail())

# Save to CSV
# CSV is too heavy, and can't upload to github
# df.to_csv('../data/climbs_data.csv', index=False) 
# Save to Parquet
df.to_parquet('../data/climbs_data.parquet')