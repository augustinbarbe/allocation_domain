# TODO : Format error response and append status code

from flask import request
import json
import os
from six.moves.urllib.request import urlopen
from functools import wraps
from jose import jwt


class UnAuthorizedError(Exception):
    pass


class ForbiddenError(Exception):
    pass


ALGORITHMS = ["RS256"]
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")

API_AUDIENCE = os.environ.get("AUTH0_API_AUDIENCE")


def get_token():
    """Obtains the Access Token from the Authorization Header"""
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise UnAuthorizedError(
            "Authorization header is expected",
        )

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise UnAuthorizedError(
            "Authorization header must start with" " Bearer",
        )
    elif len(parts) == 1:
        raise UnAuthorizedError("Token not found")
    elif len(parts) > 2:
        raise UnAuthorizedError(
            "Authorization header must be" " Bearer token",
        )

    token = parts[1]
    return token


def decrypt_token(token):
    jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/",
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise UnAuthorizedError("token is expired")

        except jwt.JWTClaimsError:
            raise UnAuthorizedError(
                "incorrect claims, please check the audience and issuer",
            )
        except Exception as e:
            print(e)
            raise UnAuthorizedError(
                "Unable to parse authentication token.",
            )

    raise UnAuthorizedError("Unable to find appropriate key")


def requires_auth(f):
    """Determines if the Access Token is valid and inject id of corresponding user"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token()
        payload = decrypt_token(token)
        user_id = payload.get("sub").split("|")[-1]
        return f(user_id=user_id, *args, **kwargs)

    return decorated
