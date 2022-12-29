import pandas as pd
import json
from services import check_fields
import os

class Checker:
    def __init__(self, df):
        self.df = df

    def check_match_required_fields(self):
        with open('field_variations.json', encoding='utf-8') as f:
            field_variations = json.load(f)
        return check_fields(field_variations['required_fields'], list(self.df))

    def check_match_unrequired_fields(self):
        with open('field_variations.json', encoding='utf-8') as f:
            field_variations = json.load(f)
        return check_fields(field_variations['unrequired_fields'], list(self.df))

    def get_duplicate_headers(self):
        headers = [header.lower().split(".")[0] for header in list(self.df)]
        dup = {x for x in headers if headers.count(x) > 1}
        return dup if dup else None




if __name__ == "__main__":
    file_names = os.listdir("new_files")
    for n , file_name in enumerate(file_names):
        print(f"-" * 30, file_name, f"-" * 30)
        df = pd.read_excel(f"new_files/{file_name}")
        excel_file = Checker(df)
        print(excel_file.check_match_required_fields())
        print(excel_file.check_match_unrequired_fields())
        print(excel_file.get_duplicate_headers())


