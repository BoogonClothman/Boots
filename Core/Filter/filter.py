# Core/Filter/filter.py
import re

class Filter:
    """Filter for bad words."""
    def __init__(
            self,
            badwords_path: str
            ):
        """
        Constructor of Filter.
        
        Args:
            badwords_path (str): Path of bad words file.
        
        Attributes:
            bad_words (list[str]): Bad words.
            regex (re.Pattern): Regular expression of bad words.
        """
        self.bad_words = self._load_badwords(badwords_path)  # NoneType means FileError.
        self.regex = self._build_regex()

    def _load_badwords(self, badwords_path: str):
        """Load bad words from file."""
        try:
            with open(badwords_path, 'r', encoding='utf-8') as f:
                return list({line.strip() for line in f if line.strip()})
        except FileNotFoundError:
            print(f"[Filter._load_badwords] File \"{badwords_path}\" doesn't exist.")
            return None
        
    def _build_regex(self):
        """Build regular expression of bad words."""
        if self.bad_words is None:
            return None
        sorted_words = sorted(self.bad_words, key=lambda x: -len(x))
        pattern = "|".join(map(re.escape, sorted_words))
        return re.compile(f"({pattern})", flags=re.I)
        
    def filter_text(self, text: str, replace_char: str="*"):
        """Filter bad words in text."""
        if self.regex is None:
            return text
        return self.regex.sub(
            lambda m: replace_char * len(m.group()),
            text
        )
