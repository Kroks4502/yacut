import random

from settings import (SHORT_URL_ALLOW_CHARACTERS, SHORT_URL_AUTO_GEN_LEN,
                      SHORT_URL_USER_MAX_LEN, URL_PATTERN)

from .models import URLMap


def get_unique_short_id(length: int = SHORT_URL_AUTO_GEN_LEN) -> str:
    short_id = (''.join(random.choice(SHORT_URL_ALLOW_CHARACTERS)
                        for _ in range(length)))
    if is_not_uniq_short(short_id):
        return get_unique_short_id()
    return short_id


def is_not_uniq_short(short_id: str) -> bool:
    return bool(URLMap.query.filter_by(short=short_id).first())


def is_not_valid_url(url: str) -> bool:
    return not bool(URL_PATTERN.fullmatch(url))


def is_not_valid_short_id(short_id: str) -> bool:
    validation_characters = set(short_id)
    return (not validation_characters.issubset(SHORT_URL_ALLOW_CHARACTERS) or
            len(short_id) > SHORT_URL_USER_MAX_LEN)
