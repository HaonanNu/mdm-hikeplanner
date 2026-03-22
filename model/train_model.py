import datetime
import os
import pickle
from pathlib import Path

import pandas as pd
import seaborn as sn
from dotenv import load_dotenv
from pymongo import MongoClient
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Setup
script_dir = Path(__file__).resolve().parent
env_path = script_dir.parent / ".env"
load_dotenv(env_path, override=True)
mongo_uri = os.getenv("MONGO_DB_CONNECTION_STRING")
if not mongo_uri:
    raise SystemExit("Missing MongoDB URI. Set MONGO_DB_CONNECTION_STRING in .env or in the environment.")

mongo_db = "tracks"
mongo_collection = "tracks"

client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = db[mongo_collection]

# Check if data exists
if collection.count_documents({}) == 0:
    raise SystemExit("No tracks found in MongoDB.")

print("\n*** Loading Tracks from MongoDB ***")

# Load data
cursor = collection.find({})
chunks = []
for doc in cursor:
    chunks.append(doc)

df = pd.DataFrame(chunks).set_index("_id")

# Clean data
df = df.dropna()
features = ['downhill', 'uphill', 'length_3d', 'max_elevation']
target = 'moving_time'

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Models
print("Training LinearRegression...")
lr = LinearRegression()
lr.fit(X_train, y_train)

print("Training GradientBoostingRegressor...")
gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
gbr.fit(X_train, y_train)

# Save Models
print("Saving models...")
lr_path = script_dir / "LinearRegression.pkl"
gbr_path = script_dir / "GradientBoostingRegressor.pkl"

with open(lr_path, "wb") as f:
    pickle.dump(lr, f)

with open(gbr_path, "wb") as f:
    pickle.dump(gbr, f)

# Heatmap for correlations
print("Generating Correlation Heatmap...")
corr = df[features + [target]].corr(numeric_only=True)
sn.heatmap(corr, annot=True, fmt=".2f", annot_kws={"size": 7})

# Create static directory for plot if needed
static_dir = script_dir / "static"
static_dir.mkdir(parents=True, exist_ok=True)

print(f"Training complete. Models saved to {lr_path} and {gbr_path}")
