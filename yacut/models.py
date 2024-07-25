import random
from datetime import datetime

from .constants import MAX_SHORT_LENGTH, MAX_ORIGINAL_LENGTH
from settings import BASE_URL, ACCEPTED_SYMBOLS
from yacut import db

from .constants import MAX_ATTEMPTS, TOO_MANY_ATTEMPTS


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), unique=True,)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def generate_unique_short_id(length=6):
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            short = ''.join(random.sample(ACCEPTED_SYMBOLS, length))
            if URLMap.query.filter_by(short=short).first() is None:
                return short
            attempts += 1
            length += 1
        raise ValueError(TOO_MANY_ATTEMPTS)


    def to_dict(self, is_get=False):
        if is_get:
            return dict(
                url=self.original,
            )
        return dict(
            url=self.original,
            short_link=BASE_URL + self.short
        )
