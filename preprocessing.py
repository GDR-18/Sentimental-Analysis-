import re

def preprocess_text(text):

    text = str(text).lower()

    text = re.sub(r"http\\S+", "", text)

    text = re.sub(r"[^a-zA-Z ]", "", text)

    text = re.sub(r"\\s+", " ", text)

    return text.strip()

from spellchecker import SpellChecker

def is_valid_text(text):
    # 1. Check for empty inputs
    if not text or not text.strip():
        return False
        
    # 2. Block text if any single word has a long keyboard smash pattern
    gibberish_pattern = r'[bcdfghjklmnpqrstvwxyz]{4,}'
    if re.search(gibberish_pattern, text.lower()):
        return False

    spell = SpellChecker()
    words = text.lower().split()
    
    # 3. Look at every individual word
    for word in words:
        clean_word = re.sub(r'[^\w\s]', '', word)
        
        if clean_word:  
            # If a word is long and completely unrecognized, block it
            if len(clean_word) > 4 and clean_word not in spell:
                return False
                
    return True