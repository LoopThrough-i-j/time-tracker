class Error(Exception):
    """Base exception class"""

    pass


class BadRequestError(Error):
    """Bad request exception"""

    pass


class NotFoundError(Error):
    """Not found exception"""

    pass


class ValidationError(Error):
    """Validation exception"""

    pass
