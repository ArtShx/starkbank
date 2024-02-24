import logging
import re

def setup_logger():
    ...

def get_logger():
    return logging.getLogger("main")


def contains_only_numbers(s: str) -> bool:
    """Regex function to check if the string only contains numbers."""
    pattern = r'^\d+$'

    return bool(re.match(pattern, s))
