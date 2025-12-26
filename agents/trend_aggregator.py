import pandas as pd
from collections import defaultdict
import os

TREND_PATH = "output/trend_report_T.csv"

def generate_trend_table(daily_topic_counts: dict):
    """
    daily_topic_counts:
    {
      "2024-06-01": {"delivery issue": 12, "food cold": 4},
      ...
    }
    """
    df = pd.DataFrame.from_dict(daily_topic_counts, orient="index")
    df = df.fillna(0).astype(int)
    df = df.transpose()
    df.to_csv(TREND_PATH)
