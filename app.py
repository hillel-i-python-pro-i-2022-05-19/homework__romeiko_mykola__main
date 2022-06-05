import csv
import requests
from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args
from faker import Faker

from helpers import isfloat, calculate_average

app = Flask(__name__)


@app.route('/requirements/')
def get_requirements_text():
    with open('requirements.txt', 'r') as file:
        return file.read()


@app.route('/generate-users/')
@use_args({"quantity": fields.Int(required=False)}, location="query")
def generate_users(kwargs: dict) -> str:
    fake = Faker('en_US')
    Faker.seed(0)
    list_generated_emails = [fake.ascii_company_email() for _ in range(kwargs.get("quantity", 100))]
    return ', '.join(list_generated_emails)


@app.route('/space/')
def amount_of_cosmonauts():
    response = requests.get(url="http://api.open-notify.org/astros.json").json()
    return f"Amount of cosmonauts in space - {response.get('number', 'cannot get data')}."


@app.route('/mean/')
def calculate_avg_height_and_weight():
    response = requests.get(url="https://drive.google.com/u/0/uc?id=1yM0a4CSf0iuAGOGEljdb7qcWyz82RBxl&export=download")
    decoded_content = response.content.decode('utf-8')
    csv_reader = csv.DictReader(decoded_content.splitlines(), fieldnames=["Index", "Height(Inches)", "Weight(Pounds)"])
    height_data = []
    weight_data = []
    for row in csv_reader:
        height = row.get('Height(Inches)')
        weight = row.get('Weight(Pounds)')
        if isfloat(height):
            height_data.append(float(height))
        if isfloat(weight):
            weight_data.append(float(weight))
    avg_height_cm = calculate_average(height_data) * 2.54
    avg_weight_kg = calculate_average(weight_data) / 2.20462262185
    return f"""
    Average height - {avg_height_cm} cm<br>
    Average weight - {avg_weight_kg} kg
    """


if __name__ == '__main__':
    app.run(debug=True)
