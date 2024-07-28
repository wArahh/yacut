import random
import re
from datetime import datetime

from yacut import db

from .constants import (
    ACCEPTED_SYMBOLS, MAX_ATTEMPTS, MAX_ORIGINAL_LENGTH,
    MAX_SHORT_LENGTH, REGEXP_ACCEPTED_SYMBOLS,
    SHORT_BASE_LENGTH, TOO_MANY_ATTEMPTS, UNEXPECTED_NAME,
    URL_ALREADY_EXISTS
)
from .exceptions import (
    DuplicateShortURLError, ShortURLError, TooManyAttemptsError
)
from .utils import get_short_link


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), unique=True, )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_or_404(short):
        return URLMap.query.filter_by(short=short).first_or_404()

    @staticmethod
    def create(original, short=None, validated=False):
        if short is None:
            short = URLMap.generate_unique_short()
        if not validated:
            if (
                len(short) > MAX_SHORT_LENGTH
                or len(original) > MAX_ORIGINAL_LENGTH
                or not re.match(REGEXP_ACCEPTED_SYMBOLS, short)
            ):
                raise ShortURLError(UNEXPECTED_NAME)
            if URLMap.get(short) is not None:
                raise DuplicateShortURLError(URL_ALREADY_EXISTS)
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
            if URLMap.get(short) is None:
                return short
        raise TooManyAttemptsError(TOO_MANY_ATTEMPTS)

    def to_dict(self, is_get=False):
        if is_get:
            return dict(
                url=self.original,
            )
        return dict(
            url=self.original,
            short_link=get_short_link(self.short)
        )
