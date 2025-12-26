from agents.topic_extractor import extract_topics
from agents.topic_normalizer import normalize_or_create
from agents.trend_aggregator import update_trends

def extract_step(review):
    return extract_topics(review["text"])

def normalize_step(topic):
    return normalize_or_create(topic)

def aggregate_step(date, topic):
    update_trends(date, topic)
