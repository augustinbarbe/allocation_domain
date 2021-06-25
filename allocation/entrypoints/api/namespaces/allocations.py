from flask_restx import Namespace, Resource, fields

from ..service_adapter import service
from ..parsers import pagination_parser, get_pagination

from allocation import views

api = Namespace("allocations", description="Request allocations")

request = api.model(
    "Allocation",
    {
        "request_id": fields.String,
        "resource_id": fields.String,
        "quantity": fields.Integer,
    },
)

requests = api.model(
    "Requests",
    {
        "total": fields.Integer,
        "num_pages": fields.Integer,
        "members": fields.List(fields.Nested(request)),
    },
)


@api.route("/")
@api.doc(security="apikey")
class Resources(Resource):
    @api.doc(description="Retrieve all allocated requests")
    @api.marshal_with(requests)
    @api.expect(pagination_parser)
    def get(self):
        pagination = get_pagination()
        return views.get_requests(service, pagination)
