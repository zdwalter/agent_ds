"""
Natural Language Processing skill using TextBlob.
"""

import json
import subprocess
import sys
from typing import Any, Dict, List

try:
    from textblob import TextBlob
    from textblob.exceptions import MissingCorpusError
except ImportError:
    print(
        "Error: TextBlob not installed. Please run 'pip install textblob'",
        file=sys.stderr,
    )

    # Define dummy TextBlob to avoid crash, but functions will raise
    class TextBlob:  # type: ignore[no-redef]
        def __init__(self, text):
            raise ImportError("TextBlob not installed")

    MissingCorpusError = Exception


def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze sentiment of the given text.
    Returns a dict with polarity (-1 to 1) and subjectivity (0 to 1).
    """
    blob = TextBlob(text)
    return {
        "polarity": blob.sentiment.polarity,
        "subjectivity": blob.sentiment.subjectivity,
        "text": text,
    }


def extract_noun_phrases(text: str) -> List[str]:
    """
    Extract noun phrases from the text.
    Returns a list of noun phrases (strings).
    """
    try:
        blob = TextBlob(text)
        return list(blob.noun_phrases)
    except MissingCorpusError:
        # If NLTK data missing, return empty list
        return []


def tokenize_words(text: str) -> List[str]:
    """
    Tokenize text into words.
    Returns a list of words.
    """
    try:
        blob = TextBlob(text)
        return [word for word in blob.words]
    except MissingCorpusError:
        # Fallback to simple whitespace splitting
        import re

        return re.findall(r"\b\w+\b", text)


def detect_language(text: str) -> str:
    """
    Detect language of the text.
    Returns the ISO 639‑1 language code (e.g., 'en', 'fr').
    """
    # First try using langdetect library directly
    try:
        from langdetect import detect

        return detect(text)
    except ImportError:
        pass
    except Exception:
        pass
    # Fallback to TextBlob
    try:
        blob = TextBlob(text)
        return blob.detect_language()
    except (AttributeError, ImportError):
        # Language detection not available
        return "unknown"


# Optional: If you want to ensure NLTK data is present, you could add a setup function.
def _ensure_nltk_data():
    """Download required NLTK data for TextBlob."""
    try:
        import nltk

        nltk.download("punkt", quiet=True)
        nltk.download("averaged_perceptron_tagger", quiet=True)
    except ImportError:
        pass


# Call it on module import (could be heavy, maybe skip)
# _ensure_nltk_data()
