import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the dataset
# Some rows might have errors, so we'll try to handle them
try:
    df = pd.read_csv('ufo.csv', low_memory=False, on_bad_lines='skip')
except Exception as e:
    print(f"Error reading CSV: {e}")
    exit(1)

# Inspect columns
print("Columns:", df.columns)

# Convert datetime to datetime objects
# We need to handle '24:00' case which is common in some datasets
def parse_datetime(dt_str):
    try:
        # Check for 24:00
        if ' 24:00' in dt_str:
            dt_str = dt_str.replace(' 24:00', ' 00:00')
            return pd.to_datetime(dt_str) + pd.Timedelta(days=1)
        return pd.to_datetime(dt_str)
    except:
        return pd.NaT

df['datetime_parsed'] = df['datetime'].apply(parse_datetime)

# Drop rows with invalid datetime
df = df.dropna(subset=['datetime_parsed'])

# Extract hour
df['hour'] = df['datetime_parsed'].dt.hour

# Count sightings by hour
hourly_counts = df['hour'].value_counts().sort_index()

# Plotting
plt.figure(figsize=(12, 6))
hourly_counts.plot(kind='bar', color='skyblue')
plt.title("Nombre d'observations d'OVNI par heure de la journée")
plt.xlabel('Heure de la journée (0-23)')
plt.ylabel("Nombre d'observations")
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Print summary
print("Hourly Counts:")
print(hourly_counts)

# Save the plot
plt.tight_layout()
plt.savefig('ufo_by_hour.png')
print("Graph saved as ufo_by_hour.png")
