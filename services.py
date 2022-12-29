import os
import requests
from jinja2 import Template
from settings import API_PATH
from dotenv import load_dotenv

class Order():
    def __init__(self, receiver_name, code, phone, address, date, sku=None, size=None, product_name=None):
        self.receiver_name = receiver_name
        self.code = code
        self.phone = phone
        self.address = address
        self.date = date
        self.sku = sku
        self.size = size
        self.product_name = product_name

    def __str__(self):
        return f"Order({self.receiver_name}, {self.code}, {self.phone}, {self.address}, {self.date}, {self.sku}," \
               f"{self.size}, {self.product_name})"

def check_fields(fields, headers) -> dict:
    """
    Возвращает словарь:
    ключ - имя требуемого поля (на которое переиминуем заголовк датафрейма)
    значение - имя поля в таблце экселе или None если его нет
    """
    res = {}
    for field_name, variations_list in fields.items():
        res[field_name] = None
        for variant in variations_list:
            for header in headers:
                if variant == header.lower():
                    res[field_name] = header
                    break
    return res


def send_request(order):
    load_dotenv()
    with open("template.xml") as f:
        xml_file = f.read()
        rendered_template = Template(xml_file).render(
                      extra = os.getenv("API_EXTRA"),
                      login = os.getenv("API_LOGIN"),
                      password = os.getenv("API_PASSWORD"),
                      receiver_name = order.receiver_name,
                      code = order.code,
                      phone = order.phone,
                      address = order.address,
                      date = order.date,
                      sku = order.sku,
                      size = order.size,
                      product_name = order.product_name)
        response = requests.post(API_PATH, data = rendered_template.encode('utf-8'))
        print(response.text)