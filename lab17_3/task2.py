import pandas as pd
import numpy as np

def preprocess_stock_data(df):
    # Handle missing values in 'closing_price' and 'volume'
    df['closing_price'] = df['closing_price'].interpolate(method='linear')
    df['volume'] = df['volume'].fillna(method='ffill').fillna(method='bfill')

    # Create lag features: 1-day and 7-day returns
    df['return_1d'] = df['closing_price'].pct_change(periods=1)
    df['return_7d'] = df['closing_price'].pct_change(periods=7)

    # Normalize 'volume' column using log-scaling
    df['volume_log'] = np.log1p(df['volume'])

    # Detect outliers in 'closing_price' using IQR method
    Q1 = df['closing_price'].quantile(0.25)
    Q3 = df['closing_price'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df['closing_price_outlier'] = ~df['closing_price'].between(lower_bound, upper_bound)

    # Drop rows with NaN values created by lag features
    df = df.dropna().reset_index(drop=True)
    return df

# Example usage:
# df = pd.read_csv('stock_data.csv', parse_dates=['date'])
# processed_df = preprocess_stock_data(df)
# processed_df.to_csv('processed_stock_data.csv', index=False)