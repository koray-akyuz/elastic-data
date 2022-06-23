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

ELASTIC_SEARCH_SERVER = "https://elastic:gg7qKeybI_+e1L3+VK+Q@localhost:9200"
es = Elasticsearch(ELASTIC_SEARCH_SERVER,
                   ca_certs=False,
                   verify_certs=False)

# es = Elasticsearch('https://localhost:9200', verify_certs=False, http_auth=('elastic', 'gg7qKeybI_+e1L3+VK+Q'))

brand_array = ["Nikon", "Canon", "Sony", "Panasonic", "Kodak", "Fujifilm"]
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
    "EAN": "",
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
                 'SD430',
                 'SD450',
                 'SD500',
                 'SD550',
                 'SD600',
                 'SD630',
                 'SD700 IS',
                 'SD750',
                 'SD770 IS',
                 'SD780 IS',
                 'SD790 IS',
                 'SD800 IS',
                 'SD850 IS',
                 'SD870 IS',
                 'SD880 IS',
                 'SD890 IS',
                 'SD900',
                 'SD940 IS',
                 'SD950 IS',
                 'SD960 IS',
                 'SD970 IS',
                 'SD980 IS',
                 'SD990 IS',
                 'SD1000',
                 'SD1100 IS',
                 'SD1200 IS',
                 'SD1300 IS',
                 'SD1400 IS',
                 'SD3500 IS',
                 'SD4000 IS',
                 'SD4500 IS',
                 '110 HS',
                 '320 HS',
                 '340 HS[4]',
                 '520 HS']


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


def get_random_ean():
    numbers = generate_12_random_numbers()
    numbers.append(calculate_checksum(numbers))
    return ''.join(map(str, numbers))


def get_random_offering():
    ch_arr = []
    op_arr = []
    for key in char_dic:
        if key == "SKU":
            ch_arr.append(Characteristic(key, get_sku()))
        elif key == "EAN":
            ch_arr.append(Characteristic(key, get_random_ean()))
        elif key == "Image":
            ch_arr.append(Characteristic(key, get_image()))
        else:
            val_ = char_dic.get(key)
            ch_arr.append(Characteristic(key, val_[randint(0, len(val_) - 1)]))

    ind_ = randint(0, len(offering_price_array) - 1)
    op_arr.append(OfferingPrice("Price", offering_price_array[ind_], "EUR"))
    op_arr.append(OfferingPrice("Shipment Price", randint(0, 5).__str__(), "EUR"))

    ind_ = randint(0, len(product_names) - 1)
    brand_ind_ = randint(0, len(brand_array) - 1)
    brand_name = brand_array[brand_ind_] + " " + product_names[ind_]
    product = Product(brand_name, brand_name + "'s lovely description")

    rand_ = randint(1, 5)
    cat_code = "{:03d}".format(rand_);
    cat = Category(cat_code, categories[rand_])

    code = "{:03d}".format(randint(1, 5))
    s = Seller(code, "Seller " + code)

    return Offering(uuid.uuid4().hex, product, ch_arr, op_arr, s, cat)


if __name__ == '__main__':

    f = open("log.txt", 'a')

    # es.options(ignore_status=[400,404]).indices.delete(index='offers')

    # resp = es.count(index="offers")
    # print(resp)

    # for _ in range(90000):
    #     of = get_random_offering()
    #     es.index(index="offers", id=of.id, document=to_dict(of))

    # es.index(index="offers", id=id_, document=of_dict)

    f.write("start: " + datetime.now().strftime('"%m/%d/%Y, %H:%M:%S.%f"') + "\n")
    resp = es.search(index="offers", from_=400, size=100, query=
    {
        "bool": {
            "must": [
                {"match": {"characteristics.code": "Color"}},
                {"match": {"characteristics.value": "Red"}},
                {"match": {"characteristics.code": "Resolution"}},
                {"match": {"characteristics.value": "1920_x_1080"}},
            ]
        }

    })
    print(resp)

    c = 0

    for hit in resp['hits']['hits']:
        # f.write(str(hit["_source"]) + "\n")
        print(hit["_source"])
        c = c + 1

    f.write("end: " + datetime.now().strftime('"%m/%d/%Y, %H:%M:%S.%f"') + "\n")
    print('cccc ->: ', c)
    print('matched: ', resp['hits']['total']['value'])
