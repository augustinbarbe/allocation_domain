from flask_restx import Namespace, Resource, fields

from ..service_adapter import service
from ..parsers import pagination_parser, get_pagination

from allocation import views
from allocation.domain import commands

api = Namespace("pools", description="Pool inventory", validate=True)

pool = api.model(
    "Pool",
    {
        "resource_id": fields.String(required=True),
        "pool_id": fields.String,
        "quantity": fields.Integer(required=True),
        "eta": fields.DateTime(required=True),
    },
)

pools = api.model(
    "Pools",
    {
        "total": fields.Integer,
        "num_pages": fields.Integer,
        "members": fields.List(fields.Nested(pool)),
    },
)


@api.route("/")
@api.doc(security="apikey")
class Resources(Resource):
    @api.doc(description="Retrieve all pools")
    @api.expect(pagination_parser)
    @api.marshal_with(pools)
    def get(self):
        pagination = get_pagination()
        return views.get_pools(service, pagination)

    @api.doc(description="Add a pool")
    @api.expect(pool)
    @api.marshal_with(pool)
    def post(self):
        return service.handle(commands.CreatePool(**api.payload))
