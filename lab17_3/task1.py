import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from datetime import datetime

# Download stopwords if not already present
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    if pd.isnull(text):
        return ""
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove emojis and non-ASCII
    text = text.encode('ascii', 'ignore').decode('ascii')
    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', ' ', text)
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Lowercase
    text = text.lower()
    # Remove stopwords
    text = ' '.join([word for word in text.split() if word not in stop_words])
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def is_spam(text):
    # Excessive repeated characters (e.g., "loooool", "!!!!")
    if re.search(r'(.)\1{4,}', text):
        return True
    # Only link (after cleaning, empty or just 'http...')
    if re.fullmatch(r'(http\S+|www\S+|\s+)*', text):
        return True
    return False

def clean_dataframe(df):
    # Clean post_text
    df['clean_text'] = df['post_text'].apply(clean_text)
    
    # Remove spammy posts
    df = df[~df['post_text'].apply(is_spam)]
    
    # Remove duplicates based on clean_text
    df = df.drop_duplicates(subset=['clean_text'])
    
    # Handle missing likes and shares
    df['likes'] = pd.to_numeric(df['likes'], errors='coerce').fillna(0).astype(int)
    df['shares'] = pd.to_numeric(df['shares'], errors='coerce').fillna(0).astype(int)
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df['post_hour'] = df['timestamp'].dt.hour
    df['post_weekday'] = df['timestamp'].dt.day_name()
    
    # Select and reorder columns
    df = df[['post_id', 'clean_text', 'likes', 'shares', 'timestamp', 'post_hour', 'post_weekday']]
    return df
