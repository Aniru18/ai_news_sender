def clean_text(text: str):
    """
    Basic cleaning
    """
    return text.replace("\n", " ").strip()


def trim_text(text: str, max_words: int = 600):
    """
    Token control layer
    600 words ≈ ~800 tokens
    """
    words = text.split()
    return " ".join(words[:max_words])
