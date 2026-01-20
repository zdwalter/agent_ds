---
name: nlp_skill
description: Natural Language Processing capabilities using TextBlob and NLTK.
allowed-tools:
  - analyze_sentiment
  - extract_noun_phrases
  - tokenize_words
  - detect_language
---

# NLP Skill

This skill enables the agent to perform basic natural language processing tasks.

## Tools

### analyze_sentiment
Analyze the sentiment of a text, returning polarity and subjectivity scores.
- `text`: The text to analyze.

### extract_noun_phrases
Extract noun phrases from a text.
- `text`: The text to process.

### tokenize_words
Split text into individual words (tokenization).
- `text`: The text to tokenize.

### detect_language
Detect the language of a text.
- `text`: The text to analyze.
