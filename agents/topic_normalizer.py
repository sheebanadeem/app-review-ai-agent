import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Paths
# -----------------------------
REGISTRY_PATH = "memory/topic_registry.json"
CACHE_PATH = "memory/topic_cache.json"

# -----------------------------
# Model (loaded once)
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

SIMILARITY_THRESHOLD = 0.75


# -----------------------------
# Utilities
# -----------------------------
def safe_load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r") as f:
            content = f.read().strip()
            if not content:
                return default
            return json.loads(content)
    except json.JSONDecodeError:
        return default


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# -----------------------------
# Loaders
# -----------------------------
def load_registry():
    return safe_load_json(REGISTRY_PATH, {})


def save_registry(registry):
    save_json(REGISTRY_PATH, registry)


def load_cache():
    return safe_load_json(CACHE_PATH, {})


def save_cache(cache):
    save_json(CACHE_PATH, cache)


# -----------------------------
# Core Normalization Logic
# -----------------------------
def normalize_or_create(raw_topic: str) -> str:
    """
    Normalize a raw topic into a canonical topic.
    Uses semantic similarity + caching.
    """

    raw_topic = raw_topic.strip().lower()

    # -----------------------------
    # 1️⃣ Cache check (FAST PATH)
    # -----------------------------
    cache = load_cache()
    if raw_topic in cache:
        return cache[raw_topic]["canonical"]

    # -----------------------------
    # 2️⃣ Registry check
    # -----------------------------
    registry = load_registry()

    if not registry:
        # First topic ever
        registry[raw_topic] = {
            "embedding": model.encode(raw_topic).tolist()
        }
        save_registry(registry)

        cache[raw_topic] = {
            "canonical": raw_topic,
            "confidence": 1.0
        }
        save_cache(cache)

        return raw_topic

    # -----------------------------
    # 3️⃣ Semantic similarity
    # -----------------------------
    raw_embedding = model.encode(raw_topic)

    best_topic = None
    best_score = 0.0

    for canonical_topic, data in registry.items():
        canonical_embedding = np.array(data["embedding"])
        score = cosine_similarity(
            [raw_embedding], [canonical_embedding]
        )[0][0]

        if score > best_score:
            best_score = score
            best_topic = canonical_topic

    # -----------------------------
    # 4️⃣ Decision
    # -----------------------------
    if best_score >= SIMILARITY_THRESHOLD:
        canonical = best_topic
        confidence = round(float(best_score), 3)
    else:
        canonical = raw_topic
        confidence = 1.0

        registry[canonical] = {
            "embedding": raw_embedding.tolist()
        }
        save_registry(registry)

    # -----------------------------
    # 5️⃣ Cache write-back
    # -----------------------------
    cache[raw_topic] = {
        "canonical": canonical,
        "confidence": confidence
    }
    save_cache(cache)

    return canonical
