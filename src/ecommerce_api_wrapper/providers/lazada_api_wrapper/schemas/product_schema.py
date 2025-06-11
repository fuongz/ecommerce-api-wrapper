from marshmallow import EXCLUDE, Schema, fields, pre_load

from ....utils.transform import (
    calculate_discount,
    convert_currency_string_to_int,
    convert_string_to_slug,
    convert_to_number,
)


class ProductSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=True)
    url = fields.String(required=True, allow_none=True)
    image = fields.String(required=True, allow_none=True)
    price = fields.Float(required=True, allow_none=True)
    price_original = fields.Float(required=True, allow_none=True)
    brand_name = fields.String(required=True, allow_none=True)
    brand_id = fields.Integer(required=True, allow_none=True)
    shop_id = fields.Integer(required=True, allow_none=True)
    shop_name = fields.String(required=True, allow_none=True)
    shop_url = fields.String(required=True, allow_none=True)
    rating = fields.Float(required=True, allow_none=True)
    sold_count = fields.Integer(required=True, allow_none=True)
    discount = fields.String(required=True, allow_none=True)
    keyword = fields.String(required=True, allow_none=True)
    review = fields.Integer(required=True, allow_none=True)
    sku = fields.String(required=True, allow_none=True)
    sku_id = fields.String(required=True, allow_none=True)
    cheapest_sku = fields.String(required=True, allow_none=True)

    @pre_load()
    def pre_load(self, data, many, **kwargs):
        data["id"] = int(data.get("itemId"))
        data["url"] = f"https:{data['itemUrl']}"
        data["price"] = float(data.get("price"))
        data["rating"] = (
            float(data.get("ratingScore")) if data.get("ratingScore") != "" else 0
        )
        data["price_original"] = convert_currency_string_to_int(
            data.get("originalPriceShow")
        )
        data["shop_name"] = data.get("sellerName")
        data["shop_id"] = data.get("sellerId")

        seller_slug = convert_string_to_slug(data.get("sellerName"))
        data["shop_url"] = f"https:{data['itemUrl']}/shop/{seller_slug}"

        discount = calculate_discount(data["price"], data["price_original"])
        data["discount"] = f"{discount}%"

        data["sold_count"] = convert_to_number(data.get("itemSoldCntShow"))

        data["brand_name"] = data.get("brandName")
        data["brand_id"] = data.get("brandId")
        data["review"] = int(data.get("review")) if data.get("review") != "" else 0
        data["sku"] = data.get("sku")
        data["sku_id"] = data.get("skuId")
        data["cheapest_sku"] = data.get("cheapest_sku")
        return data
