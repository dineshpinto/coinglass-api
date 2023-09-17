class CoinglassAPIError(Exception):
    """ Generic exception for API communication """

    def __init__(self, status: int, err: str):
        self.status = status
        self.err = err

    def __str__(self):
        return f"(status={self.status}) {self.err}"


class CoinglassRequestError(Exception):
    """ Generic exception for API requests """

    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg

    def __str__(self):
        return f"(code={self.code}) {self.msg}"


class RateLimitExceededError(CoinglassRequestError):
    """ Raised when API rate limit is exceeded """

    def __init__(self):
        super().__init__(code=50001, msg="")


class NoDataReturnedError(CoinglassRequestError):
    """ Raised when no data is returned from API """

    def __init__(self):
        super().__init__(code=0, msg="API request returned no data")


class CoinglassParameterWarning(Warning):
    """ Warning for (potentially) invalid parameters """
