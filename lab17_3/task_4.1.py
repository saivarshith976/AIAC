import pandas as pd
import re
import json
from pathlib import Path

# Optional: TF-IDF vectorizer (falls back gracefully if sklearn missing)
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False

# Path to the movie reviews CSV file
movie_reviews_path = r"C:\Users\savin\OneDrive\Desktop\AI Ass\LAB 17\movie_reviews-1.csv"
out_dir = Path(r"C:\Users\savin\OneDrive\Desktop\AI Ass\LAB 17")

# Read the CSV file into a DataFrame
df = pd.read_csv(movie_reviews_path)

# --- Before summary ---
before_summary = {
    'rows': int(len(df)),
    'cols': int(len(df.columns)),
    'columns': df.columns.tolist()
}

# --- Standardize column names ---
rename_map = {
    'review': 'review_text', 'text': 'review_text', 'content': 'review_text', 'comment': 'review_text',
    'Review': 'review_text', 'Text': 'review_text', 'Content': 'review_text', 'Comment': 'review_text',
    'rating': 'rating', 'ratings': 'rating', 'score': 'rating', 'Rating': 'rating', 'Score': 'rating'
}
df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)

# Ensure expected columns exist
if 'review_text' not in df.columns:
    # Try best-effort fallback to the first object/string-like column
    candidate = None
    for c in df.columns:
        if df[c].dtype == object:
            candidate = c
            break
    if candidate is None:
        raise ValueError("Could not find a text column for reviews.")
    df['review_text'] = df[candidate]

# --- Text standardization: lowercase, remove HTML tags ---
def clean_text(s: str) -> str:
    if pd.isna(s):
        return ""
    s = str(s)
    s = re.sub(r"<[^>]+>", "", s)  # remove HTML
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s

df['review_text_clean'] = df['review_text'].apply(clean_text)

# --- Ratings: handle missing and normalize (0-10 -> 0-1) ---
if 'rating' in df.columns:
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    # Fill missing with median
    med = df['rating'].median()
    df['rating'] = df['rating'].fillna(med)
    # Clip to 0..10 then scale to 0..1
    df['rating'] = df['rating'].clip(lower=0, upper=10)
    df['rating_norm'] = df['rating'] / 10.0
else:
    # If rating missing, create placeholder normalized rating as NaN
    df['rating_norm'] = pd.NA

# --- Encode reviews using TF-IDF (if sklearn available) ---
tfidf_info = { 'enabled': False }
if SKLEARN_AVAILABLE:
    tfidf = TfidfVectorizer(max_features=1000, ngram_range=(1,2), min_df=2)
    X = tfidf.fit_transform(df['review_text_clean'].fillna(""))
    # Save TF-IDF matrix and vocabulary
    try:
        import scipy.sparse as sp
        tfidf_path = out_dir / 'movie_reviews_tfidf.npz'
        sp.save_npz(tfidf_path.as_posix(), X)
        vocab_path = out_dir / 'movie_reviews_tfidf_vocab.json'
        vocab = tfidf.vocabulary_
        with open(vocab_path, 'w', encoding='utf-8') as f:
            json.dump(vocab, f)
        tfidf_info = {
            'enabled': True,
            'tfidf_path': tfidf_path.as_posix(),
            'vocab_path': vocab_path.as_posix(),
            'num_features': int(X.shape[1])
        }
    except Exception:
        # If SciPy is not present, skip saving sparse matrix
        tfidf_info = {
            'enabled': True,
            'tfidf_saved': False,
            'num_features': int(X.shape[1])
        }

# --- Build cleaned dataset for sentiment classification ---
keep_cols = []
id_candidates = ['id', 'review_id', 'user_id']
for c in id_candidates:
    if c in df.columns:
        keep_cols.append(c)
keep_cols += ['review_text_clean']
if 'rating_norm' in df.columns:
    keep_cols += ['rating_norm']

clean_df = df[keep_cols].copy()

# --- After summary ---
after_summary = {
    'rows': int(len(clean_df)),
    'cols': int(len(clean_df.columns)),
    'columns': clean_df.columns.tolist(),
    'tfidf': tfidf_info
}

# --- Save cleaned dataset ---
clean_csv = out_dir / 'movie_reviews_cleaned.csv'
clean_df.to_csv(clean_csv.as_posix(), index=False)

# --- Report before vs after ---
print("=== Movie Reviews Cleaning: Before vs After ===")
print({'before': before_summary, 'after': after_summary, 'clean_csv': clean_csv.as_posix()})
print("Sample (first 10 rows) of cleaned data:")
print(clean_df.head(10))