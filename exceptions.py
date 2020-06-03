class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class CFLError(Error):
    """Exception raised for errors in the input.
    please check https://fenicsproject.org/qa/13858/strange-oscilation-results-nonlinear-coupled-time-dependent/
    and https://en.wikipedia.org/wiki/Courant%E2%80%93Friedrichs%E2%80%93Lewy_condition

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message