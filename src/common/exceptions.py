class AuthenticationException(Exception):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.http_response_code = 401  # unauthorized
