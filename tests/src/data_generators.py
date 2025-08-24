import random
import string


def get_random_string(length: int = 6, is_numbers: bool = True) -> str:
    """Получение рандомной строки"""
    symbols = string.ascii_letters + string.digits if not is_numbers else string.ascii_letters
    return "".join(random.choices(symbols, k=length))
