import json


class Characteristic:
    def __init__(self, code, value):
        self.code = code
        self.value = value

    def to_string(self):
        return {"code": self.code, "value": self.value}


class OfferingPrice:
    def __init__(self, type_, value, currency):
        self.type = type_
        self.value = value
        self.currency = currency


class Product:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Category:
    def __init__(self, code, name):
        self.code = code
        self.name = name


class Seller:
    def __init__(self, seller_code, seller_name):
        self.seller_code = seller_code
        self.seller_name = seller_name


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


class Offering:
    def __init__(self, id_, product, characteristics, prices, seller, category):
        self.id = id_
        self.product = product
        self.characteristics = characteristics
        self.prices = prices
        self.seller = seller
        self.category = category

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4, ensure_ascii=False)
