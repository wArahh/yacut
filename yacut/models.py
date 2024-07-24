from datetime import datetime

from settings import BASE_URL
from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String(16), unique=True,)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self, is_get=False):
        if is_get:
            return dict(
                url=self.original,
            )
        return dict(
            url=self.original,
            short_link=BASE_URL + self.short
        )
