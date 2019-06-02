from flask import Flask
import random
import json
app = Flask(__name__)

USER_ID = "1"

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
    promotion_file = open("promotions.json", "r")
    promotions = json.loads(promotion_file.read())

    return json.dumps(promotions[promotion_number], ensure_ascii=False)


@app.route("/promo/<code>")
def promo(code):
    promos_file = open("promo.json", "r")
    promocodes = json.loads(promos_file.read())

    for promocode in promocodes:
        if promocode["code"] == code:

            users_file_r = open('users.json', 'r')
            users_data = json.loads(users_file_r.read())
            users_file_r.close()

            users_data[USER_ID]["promocode"] = code

            users_file_w = open('users.json', 'w')
            users_file_w.write(json.dumps(users_data))
            users_file_w.close()

        return json.dumps({"valid": True, "discount": promocode["discount"]})
    return json.dumps({"valid": False})


@app.route("/meals")
def meals_route():
    users_file_r = open('users.json', 'r')
    users_data = json.loads(users_file_r.read())
    users_file_r.close()

    discount = 0

    promocode = users_data[USER_ID]["promocode"]

    if promocode != None:
        promos_file = open('promo.json', 'r')
        promocodes = json.loads(promos_file.read())
        promos_file.close()

        for p in promocodes:
            if p[ 'code' ] == promocode:
                discount = p['discount']

        for meal in meals:
            meal ['price'] = (1.0 - discount/ 100) * meal[ 'price']

    return json.dumps(meals)


app.run("0.0.0.0", 8000)
