from flask_cors import CORS
from flask_jwt_extended import JWTManager

from common.exceptions import AuthenticationException
from models import db, User


def configure_extensions(app):
    db.init_app(app)
    CORS(app)

    # JWT Initialization
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity: User):
        # Register a callback function that takes whatever object is passed in as the
        # identity when creating JWTs and converts it to a JSON serializable format.
        return identity.uid

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        # Register a callback function that loads a user from your database whenever
        # a protected route is accessed. This should return any python object on a
        # successful lookup, or None if the lookup failed for any reason (for example
        # if the user has been deleted from the database).
        user_id = jwt_data["sub"]

        user = User.query.filter_by(uid=user_id).first()
        if user is None:
            raise AuthenticationException("User ID provided is not valid.")

        return user
