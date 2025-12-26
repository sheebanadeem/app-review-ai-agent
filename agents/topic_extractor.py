def extract_topics(text: str):
    """
    Lightweight topic extractor without external APIs.
    Keeps assignment deterministic and debuggable.
    """

    keywords = [
        "login",
        "authentication",
        "payment",
        "crash",
        "slow",
        "ui",
        "performance",
        "bug",
        "error"
    ]

    text_lower = text.lower()
    found = []

    for k in keywords:
        if k in text_lower:
            found.append(k)

    # fallback
    if not found:
        found.append("general feedback")

    return found
