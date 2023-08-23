from random import choices
import re

from .validators import short_validator


def get_unique_short_id(original_link):
    short_url = random_url(original_link)
    while short_validator(short_url):
        short_url = random_url(original_link)
    return short_url


def random_url(url):
    return ''.join(choices(
        list(re.sub(r"[^a-zA-Z0-9]", "", ''.join(url.split('/')))),
        k=6)
    )
