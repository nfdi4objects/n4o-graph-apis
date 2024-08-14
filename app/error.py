class ApiError(Exception):
    def __init__(self, message, status=None):
        Exception.__init__(self)
        self.message = message
        self.status = status if status is not None else 500

    def to_dict(self):
        return {"message": self.message, "code": self.status}
