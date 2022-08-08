import uuid
from datetime import datetime
from functools import reduce
from random import randint
from random import randrange

from elasticsearch import Elasticsearch

from model import Category
from model import Characteristic
from model import Offering
from model import OfferingPrice
from model import Product
from model import Seller
from model import to_dict

ELASTIC_SEARCH_SERVER = "https://elastic:gg7qKeybI_+e1L3+VK+Q@localhost:9200"
# ELASTIC_SEARCH_SERVER = "https://admin:admin@localhost:9201"
es = Elasticsearch(ELASTIC_SEARCH_SERVER,
                   ca_certs=False,
                   verify_certs=False)

# es = Elasticsearch('https://localhost:9200', verify_certs=False, http_auth=('elastic', 'gg7qKeybI_+e1L3+VK+Q'))

brand_array = ['Bosch',
               'Arçelik',
               'Samsung',
               'Beko',
               'VESTEL',
               'Profilo',
               'Siemens',
               'Altus',
               'LG',
               'Grundig',
               'Hoover',
               'Regal',
               'Electrolux',
               'Seg',
               'Miele',
               'Vestfrost',
               'Finlux',
               'Windsor',
               'Silverline',
               'Bood']

description = ["Fancy Description 1", "Fancy Description 2", "Fancy Description 3", "Fancy Description 4",
               "Fancy Description 5", "Fancy Description 6"]
title = ["Product Title1", "Product Title2", "Product Title3", "Product Title4",
         "Product Title5", "Product Title6"]

colour = ["Red", "White", "Black", "Yellow", "Green", "Blue"]

categories = ["Electronic", "Home Appliance", "Photography", "Computers", "Sports", "Outdoor", "Books"]

resolution = ['1280_x_1024', '1920_x_1080', '3840_x_2160', '1920_x_1080', '3840_x_2160']
optical_zoom = ['10X', '16X', '20X', '25X']
screen_size = ['30-39"_(76-99_cm)',
               '40-49"_(102-125_cm)',
               '50-59"_(127-150_cm)',
               '60-69"_(152-175_cm)',
               '70"_(178_cm)_y_más']
weight = ['Hasta_149_g',
          '150_-_299_g',
          '300_-_499_g',
          '500g_y_más',
          'Hasta_1_kg']
image_stabilization = ['Digital_',
                       'Dinámica',
                       'Óptica']
file_format = ['AVI',
               'JPEG',
               'MOV']

aspect_ratio = ['5_fps',
                '10_fps',
                '15_fps',
                '20_fps',
                '24_fps',
                '30_fps',
                '50_fps',
                '60_fps',
                '120_fps',
                '200_fps',
                '240_fps']

wireless_communication = ['2,4_GHz_radiofrecuencia',
                          '802.11a',
                          'Bluetooth',
                          'Infrarrojo']

effective_video_resolution = ['360_píxeles',
                              '480_píxeles',
                              '720_píxeles',
                              '1080_píxeles',
                              '4000_píxeles']

type_of_exposition = ['Manual', 'Automatic']

char_dic = {
    "Brand": brand_array,
    "Description": description,
    "Title": title,
    "Color": colour,
    "Resolution": resolution,
    "Optical Zoom": optical_zoom,
    "Screen Size": screen_size,
    "Weight": weight,
    "Image Stabilization": image_stabilization,
    "File Format": file_format,
    "Aspect Ratio": aspect_ratio,
    "Wireless Communication": wireless_communication,
    "Effective Video Resolution": effective_video_resolution,
    "Type Of Exposition": type_of_exposition,
    "SKU": "",
    "Image": ""
}

offering_price_array = ["100", "99.8", "78.7", "65.5", "54.9", "53.5", "84.6", "91.3", "49.9", "89.6"]

product_names = ['S45',
                 'S100',
                 'S110',
                 'S200',
                 'S230',
                 'S300',
                 'S330',
                 'S400',
                 'S410',
                 'S500',
                 'SD10',
                 'SD20',
                 'SD30',
                 'SD40',
                 'SD100',
                 'SD110',
                 'SD200',
                 'SD300',
                 'SD400',
                 'SD430']


def get_sku():
    numbers = []
    for x in range(10):
        numbers.append(randrange(10))
    return ''.join(map(str, numbers))


def get_image():
    return "www.akyuzk.com/images/" + uuid.uuid4().hex + ".jpg"


def generate_12_random_numbers():
    numbers = []
    for x in range(12):
        numbers.append(randrange(10))
    return numbers


def calculate_checksum(ean):
    sum_ = lambda x, y: int(x) + int(y)
    evensum = reduce(sum_, ean[::2])
    oddsum = reduce(sum_, ean[1::2])
    return (10 - ((evensum + oddsum * 3) % 10)) % 10


ean_array = []


def get_random_ean():
    numbers = generate_12_random_numbers()
    numbers.append(calculate_checksum(numbers))
    return ''.join(map(str, numbers))


def get_random_offering():
    ch_arr = []
    op_arr = []
    ind_ean = randint(0, 4999)
    sku = get_sku()
    for key in char_dic:
        if key == "SKU":
            ch_arr.append(Characteristic(uuid.uuid4().hex, key, sku))
        elif key == "Image":
            ch_arr.append(Characteristic(uuid.uuid4().hex, key, get_image()))
        else:
            val_ = char_dic.get(key)
            ch_arr.append(Characteristic(uuid.uuid4().hex, key, val_[randint(0, len(val_) - 1)]))

    ind_ = randint(0, len(offering_price_array) - 1)
    op_arr.append(OfferingPrice("Price", offering_price_array[ind_], "EUR"))
    op_arr.append(OfferingPrice("Shipment Price", randint(0, 5).__str__(), "EUR"))

    brand_name = brand_array[ind_ean % 20] + " " + product_names[ind_ean % 20]
    product = Product(uuid.uuid4().hex, brand_name, brand_name + "'s lovely description")

    rand_ = randint(1, 5)
    cat_code = "{:03d}".format(rand_);
    cat = Category(cat_code, categories[rand_])

    code = "{:03d}".format(randint(1, 5))
    s = Seller(code, "Seller " + code)

    is_buy_box = True if ind_ean % 10 == 0 else False

    return Offering(uuid.uuid4().hex, product, ch_arr, op_arr, s, cat, 'vgc_' + ean_array[ind_ean],
                    ean_array[ind_ean], sku, buy_box=is_buy_box)


def delete_all():
    es.options(ignore_status=[400, 404]).indices.delete(index='offers')


def match_all():
    resp = es.search(index="offers", query={"match_all": {}})
    total_count = resp['hits']['total']['value']
    print(total_count)
    for hit in resp['hits']['hits']:
        print(hit["_source"])


def match_vgc(vgc):
    resp = es.search(index="offers", query={"match": {'variantGroupCode': vgc}})
    total_count = resp['hits']['total']['value']
    print(total_count)
    for hit in resp['hits']['hits']:
        print(hit["_source"])


def match_query(_from=0, size=100):
    print(datetime.now())
    match_arr = [{"match": {"category.id": '003'}}, {"match": {"buyBox": True}}]

    resp = es.search(index="offers", from_=_from, size=size, query={
        "bool": {
            "must": match_arr
        }
    })

    total_count = resp['hits']['total']['value']
    print(total_count)
    for hit in resp['hits']['hits']:
        print(hit["_source"])
    print(datetime.now())


def aggregate_query():
    print(datetime.now())
    body = {
        "size": 0,
        "query":
            {
                "bool": {
                    "should": [
                        {"match": {"category.id": '002'}},
                        {"match": {"category.id": '003'}},
                    ]
                }
            },
        "aggs": {
            "ean_agg": {
                "terms": {
                    "field": "ean.keyword",
                    "size": 100
                },
                "aggregations": {
                    "hits": {
                        "top_hits": {"size": 100}
                    },
                    "limitBucket": {
                        "bucket_sort": {
                            "sort": [],
                            "from": 0,
                            "size": 100
                            # ,"gap_policy": "SKIP"
                        }
                    }
                }
            }
        }
    }
    result = es.search(index="offers", body=body)
    total_count = result['hits']['total']['value']
    print('total count: ', total_count)
    buckets = result['aggregations']['ean_agg']['buckets']
    ret_dic = {}
    for bucket in buckets:
        ean = ''
        group_arr = []
        hits = bucket['hits']['hits']['hits']
        for hit in hits:
            group_arr.append(hit['_source'])
            ean = hit['_source']['ean']
        ret_dic[ean] = group_arr
    print(datetime.now())
    return ret_dic


def fill_index():
    for i in range(5000):
        ean_array.append(get_random_ean())

    for _ in range(10000):
        of = get_random_offering()
        es.index(index="offers", id=of.id, document=to_dict(of))


def get_price(prices):
    for price in prices:
        if price.get('type') == 'Price':
            return price.get('value') if price.get('value') is not None else '0'


def find_buy_box(arr_):
    min_arr = ()
    max_arr = ()
    arr_length = len(arr_)
    if arr_length == 1:
        return arr_[0]

    a0_price = get_price(arr_[0].get('prices'))
    a1_price = get_price(arr_[1].get('prices'))

    if a0_price > a1_price:
        max_arr = (arr_[0].get('id'), a0_price)
        min_arr = (arr_[1].get('id'), a1_price)
    else:
        max_arr = (arr_[1].get('id'), a1_price)
        min_arr = (arr_[0].get('id'), a0_price)

    i = 2
    while i < arr_length:
        ai_price = get_price(arr_[i].get('prices'))
        if ai_price > max_arr[1]:
            max_arr = (arr_[i].get('id'), ai_price)
        elif ai_price < min_arr[1]:
            min_arr = (arr_[i].get('id'), ai_price)
        i = i + 1

        # print('min  ', min_arr)
        # print('max  ', max_arr)

    # for a in arr_:
    #     prices = a.get('prices')
    #     price = get_price(prices)
    #     id_ = a.get('id')


if __name__ == '__main__':
    match_vgc('vgc_2750793807185')
    # match_query()
    # delete_all()
    # fill_index()
    # # match_query()
    #
    # dict_ = aggregate_query()
    #
    # for key in dict_:
    #     find_buy_box(dict_.get(key))

    # delete_all()
# delete_all()
# aggregate_query()

# f = open("log.txt", 'a')
#
# for i in range(20):
#     ean_array.append(get_random_ean())

# es.options(ignore_status=[400,404]).indices.delete(index='offers')
#
# resp = es.count(index="offers")
# print(resp)

# for _ in range(100):
#     of = get_random_offering()
#     print(of.to_json())
#     es.index(index="offers", id=of.id, document=to_dict(of))

# es.index(index="offers", id=id_, document=of_dict)

# f.write("start: " + datetime.now().strftime('"%m/%d/%Y, %H:%M:%S.%f"') + "\n")
# resp = es.search(index="offers", from_=0, size=200, query={"match_all": {}}, aggregations=)
# print(resp)
#
# c = 0
#
# for hit in resp['hits']['hits']:
#     # f.write(str(hit["_source"]) + "\n")
#     print(hit["_source"])
#     c = c + 1
#
# f.write("end: " + datetime.now().strftime('"%m/%d/%Y, %H:%M:%S.%f"') + "\n")
# print('cccc ->: ', c)
# print('matched: ', resp['hits']['total']['value'])
