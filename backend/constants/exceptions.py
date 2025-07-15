class Error(Exception):
    pass


class BadRequestError(Error):
    pass


class NotFoundError(Error):
    pass


class ValidationError(Error):
    pass
