import random
from datetime import datetime

from settings import ACCEPTED_SYMBOLS, BASE_URL
from yacut import db

from .constants import (BAD_REQUEST_400, MAX_ATTEMPTS, MAX_ORIGINAL_LENGTH,
                        MAX_SHORT_LENGTH, NOT_EXISTS_404, TOO_MANY_ATTEMPTS,
                        UNEXPECTED_NAME, URL_ALREADY_EXISTS, URL_NOT_EXISTS)
from .error_handlers import InvalidAPIUsage


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), unique=True,)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_object(short):
        urls = URLMap.query.filter_by(short=short).first()
        if urls is None:
            raise InvalidAPIUsage(URL_NOT_EXISTS, NOT_EXISTS_404)
        return urls

    @staticmethod
    def check_unique_short(short):
        if URLMap.query.filter_by(short=short).first() is not None:
            raise InvalidAPIUsage(URL_ALREADY_EXISTS, BAD_REQUEST_400)

    @staticmethod
    def check_and_create(original, short):
        URLMap.check_unique_short(short)
        if len(short) > MAX_SHORT_LENGTH or any(
                char not in set(ACCEPTED_SYMBOLS) for char in short
        ):
            raise InvalidAPIUsage(UNEXPECTED_NAME, BAD_REQUEST_400)
        urls = URLMap()
        urls.original = original
        urls.short = short
        db.session.add(urls)
        db.session.commit()
        return urls

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
