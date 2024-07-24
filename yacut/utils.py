import random
import string

from .models import URLMap

ACCEPTED_SYMBOLS = string.ascii_letters + string.digits


def generate_short_id(length=6):
    short_id = ''.join(random.choice(
        ACCEPTED_SYMBOLS
    ) for _ in range(length))
    while URLMap.query.filter_by(short=short_id).first() is not None:
        short_id = generate_short_id(length + 1)
    return short_id
