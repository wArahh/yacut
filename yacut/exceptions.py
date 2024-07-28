class URLMapError(Exception):
    pass


class ShortURLError(URLMapError):
    pass


class DuplicateShortURLError(URLMapError):
    pass
