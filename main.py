import sys
import os
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Ensure project root is in Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.topic_extractor import extract_topics
from agents.topic_normalizer import normalize_or_create
from agents.trend_aggregator import generate_trend_table

DATA_DIR = "data"


def load_reviews(date_str):
    """
    Load daily review batch.
    If no file exists for a date, return empty list.
    """
    path = os.path.join(DATA_DIR, f"reviews_{date_str}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_pipeline(target_date: str):
    """
    Runs the app review trend analysis pipeline
    for a 30-day rolling window ending at target_date.
    """
    target = datetime.strptime(target_date, "%Y-%m-%d")
    daily_counts = defaultdict(lambda: defaultdict(int))

    for i in range(30, -1, -1):
        day = target - timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")

        reviews = load_reviews(date_str)

        for review in reviews:
            topics = extract_topics(review["text"])
            for topic in topics:
                canonical_topic = normalize_or_create(topic)
                daily_counts[date_str][canonical_topic] += 1

    generate_trend_table(daily_counts)


if __name__ == "__main__":
    # Target date can be changed as needed
    run_pipeline("2024-06-30")
