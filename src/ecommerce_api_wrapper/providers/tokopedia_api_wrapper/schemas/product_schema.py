from marshmallow import EXCLUDE, Schema, fields, pre_load

from ....utils.transform import (
    convert_currency_string_to_int,
    convert_rb_string_to_numeric,
)


class ProductSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=True, allow_none=False)
    tiktok_shop_product_id = fields.String(required=True, allow_none=False)
    tiktok_shop_sku_id = fields.Integer(required=True, allow_none=True)
    name = fields.String(required=True, allow_none=True)
    url = fields.String(required=True, allow_none=True)
    app_link = fields.String(required=True, allow_none=True, data_key="applink")
    image = fields.String(required=True, allow_none=True)
    price = fields.Float(required=True, allow_none=True)
    price_original = fields.Float(required=True, allow_none=True)
    shop_id = fields.Integer(required=True, allow_none=True)
    shop_name = fields.String(required=True, allow_none=True)
    shop_url = fields.String(required=True, allow_none=True)
    tiktok_shop_seller_id = fields.Integer(required=True, allow_none=True)
    rating = fields.Float(required=True, allow_none=True)
    sold_count = fields.Integer(required=True, allow_none=True)
    discount = fields.String(required=True, allow_none=True)
    keyword = fields.String(required=True, allow_none=True)

    @pre_load()
    def pre_load(self, data, many, **kwargs):
        data["rating"] = (
            float(data.get("rating"))
            if data.get("rating") != "" and data.get("rating")
            else 0.0
        )
        data["tiktok_shop_product_id"] = (
            data["ttsProductID"] if data["ttsProductID"] else None
        )
        data["tiktok_shop_sku_id"] = (
            int(data["stock"]["ttsSKUID"])
            if data["stock"] and data["stock"]["ttsSKUID"]
            else None
        )

        # price
        data_price = data.get("price", {})
        if isinstance(data_price, dict):
            data["price"] = data_price.get("number", 0)
            data["price_original"] = convert_currency_string_to_int(
                data_price.get("original", "0")
            )
        elif isinstance(data_price, int):
            data["price"] = data_price
            data["price_original"] = data_price
        else:
            data["price"] = 0
            data["price_original"] = 0

        data["image"] = data.get("mediaURL", {}).get("image300", None)
        data["shop_id"] = (
            int(data["shop"]["id"]) if data["shop"] and data["shop"]["id"] else None
        )
        data["shop_name"] = (
            data["shop"]["name"] if data["shop"] and data["shop"]["name"] else None
        )
        data["shop_url"] = (
            data["shop"]["url"] if data["shop"] and data["shop"]["url"] else None
        )

        # labelGroups
        labelGroups = data["labelGroups"] if data["labelGroups"] else []
        ri_product_credibility = next(
            (
                labelGroup
                for labelGroup in labelGroups
                if labelGroup["position"] == "ri_product_credibility"
            ),
            None,
        )
        ri_ribbon = next(
            (
                labelGroup
                for labelGroup in labelGroups
                if labelGroup["position"] == "ri_ribbon"
            ),
            None,
        )
        data["sold_count"] = (
            convert_rb_string_to_numeric(ri_product_credibility["title"])
            if ri_product_credibility and ri_product_credibility["title"]
            else 0
        )
        data["discount"] = ri_ribbon.get("title", "0%") if ri_ribbon else "0%"
        data["tiktok_shop_seller_id"] = (
            int(data["shop"]["ttsSellerID"])
            if data["shop"] and data["shop"]["ttsSellerID"]
            else None
        )

        # Calculate total_gmv
        data["total_gmv"] = data["price"] * data["sold_count"]
        return data
