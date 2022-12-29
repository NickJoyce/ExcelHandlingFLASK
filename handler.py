import pandas as pd
import json
from datetime import datetime
import shutil

from exceptions import NotAllRequiredFieldsHaveMatch
from services import Order, check_fields, send_request
from checker import Checker



# file_names = os.listdir("new_files")
# for n , file_name in enumerate(file_names):
#     df = pd.read_excel(f"new_files/{file_name}")
#     print(f"[{n+1}] {file_name}: {list(df)}")


file = "new_files/Анастасия_19.12.22.xlsx"

def main_handler(file):
    # датафрейм из листа экселя
    df = pd.read_excel(file)

    checker = Checker(df)

    # проверям наличие соответсвий полей определнных в файле json полям датафрема
    # для обязательных и необязательных полей
    checked_required_fields = checker.check_match_required_fields()
    checked_unrequired_fields = checker.check_match_unrequired_fields()

    # если у всех обязательных полей найдены совпадения:
    if all(list(checked_required_fields.values())):
        # переименовываем заголовки в датафрейме
        for new_name, old_name in checked_required_fields.items():
            df.rename(columns={old_name: new_name}, inplace=True)
    else:
        raise NotAllRequiredFieldsHaveMatch("Не все обязательные поля нашлись в списке совпадений")

    # переименовываем заголовки датафрейма у необязательных полей (если есть совпадения
    for new_name, old_name in checked_unrequired_fields.items():
        if old_name:
            df.rename(columns={old_name: new_name}, inplace=True)

    for row in df.itertuples():
        order = Order(receiver_name = row.receiver_name,
                      code = row.code,
                      phone = row.phone,
                      address = row.address,
                      date = datetime.now().strftime('%Y-%m-%d'))

        # проверяем есть ли столбцы в датафрейме для необязательных полей
        try:
            order.sku = row.sku
        except AttributeError:
            pass

        try:
            order.size = row.size
        except AttributeError:
            pass

        try:
            order.product_name = row.product_name
        except AttributeError:
            pass

        # отправляем запрос
        send_request(order)

    new_folder = "handled_files"
    shutil.move(file, new_folder)

if __name__ == "__main__":
    ...








