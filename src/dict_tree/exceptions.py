class BoxTypeNotFound(ValueError):
    def __bool__(self):
        return False
    __nonzero__ = __bool__