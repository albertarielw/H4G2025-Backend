from functools import wraps

from flask_jwt_extended import current_user, verify_jwt_in_request

from common.exceptions import AuthenticationException, AuthorizationException


def user_logged_in(is_admin=False):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                verify_jwt_in_request()

            except Exception as err:
                raise AuthenticationException(
                    f"You need to log in in order to perform this action. Error: {err}"
                ) from err

            if is_admin and current_user.cat != "ADMIN":
                raise AuthorizationException("You are not authorised to perform this action.")

            return f(*args, **kwargs)

        return decorated

    return decorator
