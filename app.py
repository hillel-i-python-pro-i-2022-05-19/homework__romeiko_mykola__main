import csv
import statistics

import requests
from faker import Faker
from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from db import DB

app = Flask(__name__)

db = DB(db_file="sql_lite.db")


@app.route('/phones/create')
@use_args({"name": fields.Str(required=True), "phone": fields.Str(required=True)}, location="query")
def phones__create(kwargs):
    db.create_connection()
    sql_insert_phone_query = 'INSERT INTO phones (contactName, phoneValue) VALUES (:name, :phone);'
    db.conn.execute(sql_insert_phone_query, {'name': kwargs['name'], 'phone': kwargs['phone']})
    db.conn.commit()
    db.close_connection()
    return 'Ok'


@app.route('/phones/read-all')
def phones__read_all():
    db.create_connection()
    phones = db.conn.execute('SELECT * FROM phones;').fetchall()
    db.close_connection()
    all_data = [f'{phone_id["phoneID"]}: {phone_id["contactName"]}, {phone_id["phoneValue"]}' for phone_id in phones]
    return '<br>'.join(all_data)


@app.route('/phones/update/<int:pk>')
@use_args({"phone": fields.Str(required=True)}, location="query")
def phones__update(kwargs, pk):
    db.create_connection()
    db.conn.execute('''UPDATE phones
                       SET phoneValue=:phone
                       WHERE (phoneID=:pk);''', {'phone': kwargs['phone'], 'pk': pk})
    db.conn.commit()
    db.close_connection()
    return 'Ok'


@app.route('/phones/delete/<int:pk>')
def phones__delete(pk):
    db.create_connection()
    db.conn.execute('''DELETE FROM phones 
                       WHERE (phoneID=:pk);''', {'pk': pk})
    db.conn.commit()
    db.close_connection()
    return 'Ok'


@app.route('/requirements')
def get_requirements_text() -> str:
    """
    :return: content of requirements.txt file
    """
    with open('requirements.txt', 'r') as file:
        return file.read()


@app.route('/generate-users/')
@use_args({"quantity": fields.Int(required=False)}, location="query")
def generate_users(kwargs: dict) -> str:
    """
    by quantity param
    :return: amount of generated Name email data (example: Gary martha10@hotmail.com)
    """
    fake = Faker('en_US')
    Faker.seed(0)
    list_generated_emails = [f"{fake.profile()['name'].split()[0]} {fake.profile()['mail']}" for _ in range(kwargs.get("quantity", 100))]
    return ', '.join(list_generated_emails)


@app.route('/space/')
def amount_of_cosmonauts() -> str:
    """
    :return: amount of cosmonauts requested from third-part api
    """
    response = requests.get(url="http://api.open-notify.org/astros.json").json()
    return f"Amount of cosmonauts in space - {response.get('number', 'cannot get data')}."


@app.route('/mean/')
def calculate_avg_height_and_weight() -> str:
    """
    parse csv file requested from Google Drive
    :return: average height in cm and average weight in kg
    """
    response = requests.get(url="https://drive.google.com/u/0/uc?id=1yM0a4CSf0iuAGOGEljdb7qcWyz82RBxl&export=download")
    decoded_content = response.content.decode('utf-8')
    csv_reader = csv.DictReader(decoded_content.splitlines(), fieldnames=["Index", "Height(Inches)", "Weight(Pounds)"])
    height_data = []
    weight_data = []
    init_row = True
    for row in csv_reader:
        if init_row:
            init_row = False
            continue
        height = row.get('Height(Inches)')
        weight = row.get('Weight(Pounds)')
        height_data.append(float(height))
        weight_data.append(float(weight))
    avg_height_cm = statistics.mean(height_data) * 2.54
    avg_weight_kg = statistics.mean(weight_data) / 2.20462262185
    return f"""
    Average height - {avg_height_cm} cm<br>
    Average weight - {avg_weight_kg} kg
    """


if __name__ == '__main__':
    app.run(debug=True)
