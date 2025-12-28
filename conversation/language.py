# conversation/language.py

def detect_language(text: str) -> str:
    """
    Detects language of the user input.
    Currently supports:
    - Hindi
    - English (default)
    """

    hindi_chars = set(
        "अआइईउऊएऐओऔ"
        "कखगघचछजझ"
        "टठडढतथदधन"
        "पफबभमयरलव"
        "शषसह"
    )

    if any(char in hindi_chars for char in text):
        return "hi"

    return "en"
