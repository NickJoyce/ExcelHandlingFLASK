from flask import Flask, render_template, url_for, redirect
import os
from checker import Checker
from handler import main_handler
import pandas as pd

app = Flask(__name__) #создание экземпляра объекта Flask и присваивание его переменной "application"

app.config['SECRET_KEY'] = 'd1269dcb5c175acb12678fa83e66e9ca1a707cb4'
app.config['PERMANENT_SESSION_LIFETIME'] = 604800 # неприрывное время жизни сеанса в секундах (604800 сек. = 7 суток)
app.config['APP_ROOT'] = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def check():
    file_names = os.listdir("new_files")
    data = []
    for n, file_name in enumerate(file_names):
        df = pd.read_excel(f"new_files/{file_name}")
        excel_file = Checker(df)
        req_match = excel_file.check_match_required_fields()
        unreq_match = excel_file.check_match_unrequired_fields()
        dup = excel_file.get_duplicate_headers()
        data.append({"file_name": file_name,
                     "req_match": req_match,
                     "unreq_match": unreq_match,
                     "dup": dup})
    return render_template('check.html', data=data)


@app.route("/upload", methods=['POST'])
def upload():
    file_names = os.listdir("new_files")
    for n , file_name in enumerate(file_names):
        file = f"new_files/{file_name}"
        main_handler(file)
    return redirect(url_for('check'))


if __name__ == '__main__':
    app.run(debug=True)