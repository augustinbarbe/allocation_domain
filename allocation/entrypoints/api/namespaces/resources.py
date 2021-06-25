from flask_restx import Namespace, Resource, fields

from ..service_adapter import service
from ..parsers import pagination_parser, get_pagination

from allocation.domain import commands
from allocation import views

api = Namespace("resources", description="Request resources")

request = api.model(
    "Request",
    {"resource_id": fields.String, "quantity": fields.Integer},
)


resource = api.model(
    "Resource",
    {"resource_id": fields.String, "available_quantity": fields.Integer},
)

resources = api.model(
    "Resources",
    {
        "total": fields.Integer,
        "num_pages": fields.Integer,
        "members": fields.List(fields.Nested(resource)),
    },
)


@api.route("/")
@api.doc(security="apikey")
class Resources(Resource):
    @api.doc(description="Retrieve all resources")
    @api.expect(pagination_parser)
    @api.marshal_with(resources)
    def get(self):
        pagination = get_pagination()
        return views.get_resources(service, pagination)


@api.route("/allocate")
@api.doc(security="apikey")
class Requests(Resource):
    @api.doc(description="Request resources")
    @api.expect(request)
    @api.marshal_list_with(request)
    def post(self):
        return service.handle(commands.Allocate(**api.payload))
