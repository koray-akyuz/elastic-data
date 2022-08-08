import json
import uuid


class Characteristic:
    def __init__(self, id_, code, value, variant=False):
        self.id = id_
        self.code = code
        self.value = value
        self.variant = variant

    def to_string(self):
        return {"code": self.code, "value": self.value}


class OfferingPrice:
    def __init__(self, type_, value, currency):
        self.type = type_
        self.value = value
        self.currency = currency


class Product:
    def __init__(self, _id, name, description):
        self.id = _id
        self.name = name
        self.description = description


class Category:
    def __init__(self, code, name):
        self.id = code
        self.name = name


class Seller:
    def __init__(self, seller_code, seller_name, segment='Regular', seller_image='www.sellerimage.com/234',
                 rating='4.5',
                 free_return=True,
                 return_policy='This part will be the return Policy'):
        self.code = seller_code
        self.name = seller_name
        self.segment = segment
        self.image = seller_image
        self.rating = rating
        self.freeReturn = free_return
        self.returnPolicy = return_policy


def to_dict(obj):
    if not hasattr(obj, "__dict__"):
        return obj
    result = {}
    for key, val in obj.__dict__.items():
        if key.startswith("_"):
            continue
        element = []
        if isinstance(val, list):
            for item in val:
                element.append(to_dict(item))
        else:
            element = to_dict(val)
        result[key] = element
    return result


class ShippingTerm:
    def __init__(self, min_delivery_days, max_delivery_days, lead_time_to_ship=5):
        self.minDeliveryDays = min_delivery_days
        self.maxDeliveryDays = max_delivery_days
        self.leadTimeToShip = lead_time_to_ship


class Offering:
    def __init__(self, id_, product, characteristics, prices, seller, category, variant_code, ean, sku,
                 shipping_term=ShippingTerm(1, 3),
                 main_image='www.image.com/imageXX', external_id=uuid.uuid4().hex, buy_box=False, stock=14):
        self.id = id_
        self.product = product
        self.characteristics = characteristics
        self.prices = prices
        self.seller = seller
        self.category = category
        self.variantGroupCode = variant_code
        self.ean = ean
        self.sku = sku
        self.shippingTerm = shipping_term
        self.mainImage = main_image
        self.externalId = external_id
        self.buyBox = buy_box
        self.stock = stock

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4, ensure_ascii=False)
