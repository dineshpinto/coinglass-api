class RequiresUpgradedPlanException(Exception):
    """ Raised when an endpoint requires an upgraded plan """
    pass


class RateLimitExceededException(Exception):
    """ Raised when rate limit is exceeded """
    pass
