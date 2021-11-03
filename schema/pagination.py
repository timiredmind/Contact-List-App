from marshmallow import Schema, fields
from utils import generate_url


class PaginationSchema(Schema):
    class Meta:
        ordered = True
    link = fields.Method(serialize="get_pagination_link")
    page = fields.Int(dump_only=True)
    pages = fields.Int(dump_only=True)
    per_page = fields.Int(dump_only=True)
    total = fields.Int(dump_only=True)

    def get_pagination_link(self, paginated_object):
        paginated_links = {
            "first": generate_url(page=1, per_page=paginated_object.per_page),
            "last": generate_url(page=paginated_object.pages, per_page=paginated_object.per_page)
        }

        if paginated_object.has_prev:
            paginated_links["prev"] = generate_url(page=paginated_object.prev_num, per_page=paginated_object.per_page)

        if paginated_object.has_next:
            paginated_links["next"] = generate_url(page=paginated_object.next_num, per_page=paginated_object.per_page)

        return paginated_links

