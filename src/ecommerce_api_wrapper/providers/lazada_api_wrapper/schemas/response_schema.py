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
        mods = data.get("mods", {})
        if mods:
            data["total_items"] = int(
                mods.get("filter", {}).get("filteredQuatity", "0")
            )
            data["items"] = mods.get("listItems", [])
            # Add keyword to each product
            for product in data["items"]:
                product["keyword"] = data["keyword"]
        else:
            data["total_items"] = 0
            data["items"] = []
        return data
