from allocation.domain.models import Resource, Pool, Request
from allocation.entrypoints.api.service_adapter import ServiceAdapter
from sqlalchemy.orm import Query
from sqlalchemy_filters import apply_pagination


def paginate_results(query: Query, pagination: dict = None) -> dict:
    if pagination:
        query, pagination = apply_pagination(query, **pagination)
        return {
            "total": pagination.total_results,
            "num_pages": pagination.num_pages,
            "members": query.all(),
        }

    return {
        "total": query.count(),
        "num_pages": 1,
        "members": query.all(),
    }


def get_resources(
    service: ServiceAdapter,
    pagination: dict,
) -> dict:
    with service.message_bus.uow as uow:
        resources = paginate_results(uow.session.query(Resource), pagination)
        uow.session.expunge_all()
        return resources


def get_pools(
    service: ServiceAdapter,
    pagination: dict,
) -> dict:
    with service.message_bus.uow as uow:
        pool_result = paginate_results(uow.session.query(Pool), pagination)
        uow.session.expunge_all()
        return pool_result


def get_requests(
    service: ServiceAdapter,
    pagination: dict,
) -> dict:
    with service.message_bus.uow as uow:
        requests_result = paginate_results(uow.session.query(Request), pagination)
        uow.session.expunge_all()
        return requests_result
