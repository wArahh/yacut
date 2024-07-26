import random
import re
from datetime import datetime
from http import HTTPStatus

from yacut import db

from .constants import (
    ACCEPTED_SYMBOLS, CANNOT_BE_MORE_MAX_ORIGINAL,
    MAX_ATTEMPTS, MAX_ORIGINAL_LENGTH, MAX_SHORT_LENGTH,
    REGEXP_ACCEPTED_SYMBOLS, SHORT_BASE_LENGTH,
    TOO_MANY_ATTEMPTS, UNEXPECTED_NAME, URL_ALREADY_EXISTS
)
from .error_handlers import InvalidAPIUsage


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), unique=True, )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short)

    @staticmethod
    def get_object(short):
        return URLMap.get(short).first()

    @staticmethod
    def get_object_or_404(short):
        return URLMap.get(short).first_or_404()

    @staticmethod
    def create(original, short=None, is_api=False):
        if short is None:
            short = URLMap.generate_unique_short()
        if is_api:
            if URLMap.get_object(short) is not None:
                raise InvalidAPIUsage(
                    URL_ALREADY_EXISTS, HTTPStatus.BAD_REQUEST
                )
            if (
                    len(short) > MAX_SHORT_LENGTH
                    or not re.match(REGEXP_ACCEPTED_SYMBOLS, short)
            ):
                raise InvalidAPIUsage(UNEXPECTED_NAME, HTTPStatus.BAD_REQUEST)
            if len(original) > MAX_ORIGINAL_LENGTH:
                raise ValueError(CANNOT_BE_MORE_MAX_ORIGINAL)
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def generate_unique_short():
        for _ in range(MAX_ATTEMPTS):
            short = ''.join(
                random.sample(ACCEPTED_SYMBOLS, SHORT_BASE_LENGTH)
            )
            if URLMap.get(short).first() is not None:
                raise ValueError(TOO_MANY_ATTEMPTS)
            return short

    def to_dict(self, is_get=False):
        if is_get:
            return dict(
                url=self.original,
            )
        return dict(
            url=self.original,
            short_link='http://localhost/' + self.short
        )
