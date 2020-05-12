
class BaseError(Exception):
    """Base class for exceptions in this module."""

class InvalidSinkCallable(BaseError):
    """Exception raised for errors in the callable used for sink initialization.

      Attributes:
          expression -- input expression in which the error occurred
          message -- explanation of the error
    """

    def __init__(self, expression, message="Invalid sink callable found"):
        super().__init__()
        self.expression = expression
        self.message = message
