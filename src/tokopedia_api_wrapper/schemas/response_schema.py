from marshmallow import EXCLUDE, Schema, fields, pre_load

from .product_schema import ProductSchema


class ResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    total_items = fields.Integer(required=True, allow_none=False)
    products = fields.List(
        fields.Nested(ProductSchema), required=True, allow_none=False, data_key="items"
    )

    @pre_load()
    def pre_load(self, data, many, **kwargs):
        data["total_items"] = (
            data.get("data", {})
            .get("searchProductV5", {})
            .get("header", {})
            .get("totalData", 0)
        )
        data["items"] = (
            data.get("data", {})
            .get("searchProductV5", {})
            .get("data", {})
            .get("products", [])
        )
        # Add keyword to each product
        for product in data["items"]:
            product["keyword"] = data["keyword"]
        return data
