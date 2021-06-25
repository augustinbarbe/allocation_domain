import os
from flask_restx import Api, fields

from allocation.domain.exc import UnprocessableEntity, EntityNotFound
from allocation.entrypoints.api.security import (
    UnAuthorizedError,
    ForbiddenError,
)

from .resources import api as ns_resources
from .pools import api as ns_pools
from .allocations import api as ns_allocations

authorizations = {
    "apikey": {"type": "apiKey", "in": "header", "name": "Authorization"},
}

api = Api(
    title="Resources API",
    version=os.environ.get("VERSION"),
    description="API for resources operations",
    authorizations=authorizations,
    security="oauth2",
)

error_fields = api.model(
    "Error", {"message": fields.String, "error_type": fields.String}
)


@api.errorhandler(UnprocessableEntity)
@api.marshal_with(error_fields, code=422)
def handle_bad_input_error(error):
    return {"message": error, "error_type": error.__class__.__name__}, 422


@api.errorhandler(EntityNotFound)
@api.marshal_with(error_fields, code=404)
def handle_not_found_error(error):
    return {"message": error, "error_type": error.__class__.__name__}, 404


@api.errorhandler(ForbiddenError)
@api.marshal_with(error_fields, code=403)
def handle_forbidden_error(error):
    return {"message": error, "error_type": error.__class__.__name__}, 403


@api.errorhandler(UnAuthorizedError)
@api.marshal_with(error_fields, code=401)
def handle_authorization_error(error):
    return {"message": error, "error_type": error.__class__.__name__}, 401


@api.errorhandler(Exception)
@api.marshal_with(error_fields, code=500)
def handle_unknown_error(error):
    return {
        "message": "An unknwon error has happened on our side",
        "error_type": "UnknonError",
    }, 500


api.namespaces.clear()
api.add_namespace(ns_resources)
api.add_namespace(ns_pools)
api.add_namespace(ns_allocations)
