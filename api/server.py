from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI(
    title="App Review Trend API",
    description="Read-only API exposing processed app review insights",
    version="1.0.0"
)

OUTPUT_DIR = "output"

def load_latest_report():
    files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".csv")]
    if not files:
        return None
    latest = sorted(files)[-1]
    return pd.read_csv(os.path.join(OUTPUT_DIR, latest))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/topics")
def get_topics():
    df = load_latest_report()
    if df is None:
        return []
    return sorted(df["topic"].unique().tolist())


@app.get("/trends")
def get_trends():
    df = load_latest_report()
    if df is None:
        return []
    return df.to_dict(orient="records")
