from flask import Flask
import random
import json
app = Flask(__name__)

stepik_alive = True
workhours_open = "10:00"
workhours_closes = "21:00"
promotion_text = "Сегодня скидка 15 % по промокоду stepik!"
promocodes = []


promotions = [
    "Cкидка 15% по проомокоду stepik",
    "Скидка 10% по промокоду summer",
    "Удваиваем все пиццы по промокоду udodopizza"


]

promocodes = [
    {"code": "stepik", "discount":15},
    {"code": "summer", "discount":10},
    {"code": "pleaseplease", "discount":5},
    {"code":"doubletrouble", "discount": 50},
    {"code":"illbeback", "discount":25}


]

meals = [{
 "title": "Chinken",
 "id": 1,
 "available": True,
 "picture": "",
 "price": 20.0,
 "category": 1
}, {
 "title": "Milk",
 "id": 2,
 "available": True,
 "picture": "",
 "price": 10.0,
 "category": 1
}]








@app.route("/")
def hello():
    return "Hello"

@app.route("/alive")
def alive():
    config_file = open("config.json", "r")
    config_content = config_file.read()
    data = json.loads(config_content)
    config_file.close()
    return json.dumps({"alive": data['alive']})

@app.route("/workhours")
def workhours():
    config_file = open("config.json", "r")
    config_content = config_file.read()
    data = json.loads(config_content)
    config_file.close()
    return json.dumps(data["workhours"])


@app.route("/promotion")
def promotion():
    promotion_number = random.randint(0,2)
    return '{"promotion":" '+promotions[promotion_number]+' "}'


@app.route("/promo/<code>")
def promo(code):
    for promocode in promocodes:
        if promocode["code"] == code:
            return json.dumps({"valid": True, "discount":promocode["discount"]})
    return json.dumps({"valid": False})


@app.route("/meals")
def meals_route():
    return json.dumps(meals)


app.run("0.0.0.0", 8000)
