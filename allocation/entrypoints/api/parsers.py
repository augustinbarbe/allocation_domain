from flask_restx import reqparse


pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument("page_number", type=int)
pagination_parser.add_argument("page_size", type=int)


def get_pagination():
    """Helper to return a pagination object from the request parser"""
    return pagination_parser.parse_args()
