class HTTPError(Exception):
    def __init__(self, code, reason, body):
        self.code = code
        self.reason = reason
        self.body = body
