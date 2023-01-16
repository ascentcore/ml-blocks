class ErrorBase(Exception):
    """Error Base exception class
        Attributes:
                value   -- value given
                message -- explanation of the error
    """

    def __init__(self, value, message):
        self._value = value
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: {self._value}'


class ErrorInvalidArgument(ErrorBase):
    """Exception raised when argument is invalid
            Attributes:
                    value   -- value given
    """

    def __init__(self, value, message="Invalid argument given"):
        super().__init__(value=value, message=message)


class ErrorInvalidUsage(ErrorBase):
    """Exception raised when usage is invalid
            Attributes:
                    value   -- value given
    """

    def __init__(self, value, message="Invalid usage"):
        super().__init__(value=value, message=message)


class error_out_of_range(ErrorBase):
    """Exception raised when out of range is triggered
            Attributes:
                    value   -- value given
    """

    def __init__(self, value, message="Out of range"):
        super().__init__(value=value, message=message)


class error_environment(ErrorBase):
    """Exception raised when environment variables are not set
            Attributes:
                    value   -- value given
    """

    def __init__(self, value, message="Environment variables not set"):
        super().__init__(value=value, message=message)


class ErrorNotImplemented(ErrorBase):
    """Exception raised when implementation is not done
            Attributes:
                    value   -- value given
    """

    def __init__(self, value="", message="Implementation not done"):
        super().__init__(value=value, message=message)


class ErrorNotPresent(ErrorBase):
    """Exception raised when path is invalid
            Attributes:
                    value   -- value given
    """

    def __init__(self, value, message="Not present"):
        super().__init__(value=value, message=message)


class ErrorFatal(ErrorBase):
    """Exception raised program hit a fatal path
            Attributes:
                    value   -- value given
    """

    def __init__(self, value="", message="Fatal error"):
        super().__init__(value=value, message=message)
        exit(1)
