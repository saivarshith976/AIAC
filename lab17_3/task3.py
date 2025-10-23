import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Example: Load your IoT data (replace with your actual file path)
# df = pd.read_csv('iot_sensor_logs.csv')
# For demonstration, let's create a sample DataFrame:
data = {
    'sensor_id': ['A1', 'A2', 'A1', 'A2', 'A1', 'A2'],
    'temperature': [22.1, 23.5, None, 24.0, 22.8, None],
    'humidity': [45.2, None, 46.0, 47.1, None, 48.0],
    'timestamp': pd.date_range('2024-06-01', periods=6, freq='H')
}
df = pd.DataFrame(data)

# Sort by timestamp and sensor_id for proper forward fill
df = df.sort_values(['sensor_id', 'timestamp'])

# Handle missing values using forward fill per sensor
df[['temperature', 'humidity']] = df.groupby('sensor_id')[['temperature', 'humidity']].ffill()

# Remove sensor drift using rolling mean (window=2 for demo, adjust as needed)
df['temperature'] = df.groupby('sensor_id')['temperature'].transform(lambda x: x.rolling(window=2, min_periods=1).mean())
df['humidity'] = df.groupby('sensor_id')['humidity'].transform(lambda x: x.rolling(window=2, min_periods=1).mean())

# Normalize readings using standard scaling
scaler = StandardScaler()
df[['temperature', 'humidity']] = scaler.fit_transform(df[['temperature', 'humidity']])

# Encode categorical sensor IDs
encoder = LabelEncoder()
df['sensor_id_encoded'] = encoder.fit_transform(df['sensor_id'])

# Final structured dataset
structured_df = df[['sensor_id_encoded', 'temperature', 'humidity', 'timestamp']]

# Example: Save or return the structured dataset
# structured_df.to_csv('processed_iot_data.csv', index=False)

print(structured_df)