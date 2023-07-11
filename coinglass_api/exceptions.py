class CoinglassAPIException(Exception):
    """ Generic exception for API communication """

    def __init__(self, status: int, error: str):
        self.status = status
        self.error = error

    def __str__(self):
        return f"(status={self.status}) {self.error}"


class CoinglassRequestException(Exception):
    """ Generic exception for API requests """

    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg

    def __str__(self):
        return f"(code={self.code}) {self.msg}"


class RateLimitExceededException(CoinglassRequestException):
    """ Raised when rate limit is exceeded """

    def __init__(self):
        super().__init__(code=50001, msg="")
