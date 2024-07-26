import random
from datetime import datetime

from yacut import db

from .constants import (ACCEPTED_SYMBOLS, BASE_URL, MAX_ATTEMPTS,
                        MAX_ORIGINAL_LENGTH, MAX_SHORT_LENGTH,
                        SHORT_BASE_LENGTH, TOO_MANY_ATTEMPTS)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), unique=True, )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_object(short):
        return URLMap.query.filter_by(short=short)

    @staticmethod
    def create_object(original, short=None):
        if short is None:
            for i in range(MAX_ATTEMPTS):
                short = ''.join(
                    random.sample(ACCEPTED_SYMBOLS, SHORT_BASE_LENGTH)
                )
                if URLMap.get_object(short).first() is not None:
                    raise ValueError(TOO_MANY_ATTEMPTS)
        urlmap = URLMap(original=original, short=short)
        db.session.add(urlmap)
        db.session.commit()
        return urlmap

    def to_dict(self, is_get=False):
        if is_get:
            return dict(
                url=self.original,
            )
        return dict(
            url=self.original,
            short_link=BASE_URL + self.short
        )
