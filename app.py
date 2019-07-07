from flask import Flask, request
import random
import json
import uuid
from twilio.rest import Client


app = Flask(__name__)


USER_ID = "1"


meals = [{
 "title": "Chiсken",
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


def read_file(filename):
    opened_file = open(filename, "r")
    config_content = opened_file.read()
    data = json.loads(config_content)
    opened_file.close()
    return data

def write_file(filename, data):
    opened_file = open(filename, "w")
    opened_file.write(json.dumps(data))
    opened_file.close()

@app.route("/")
def hello():
    return "Hello"

@app.route("/alive")
def alive():
    data = read_file('config.json')
    return json.dumps({"alive": data['alive']})

@app.route("/workhours")
def workhours():
    data = read_file('config.json')
    return json.dumps(data["workhours"])


@app.route("/promotion")
def promotion():
    promotion_number = random.randint(0, 2)
    promotions = read_file('promotions.json')
    print(json.dumps(promotions)[promotion_number])
    return json.dumps(promotions[promotion_number], ensure_ascii=False)


@app.route("/promo/<code>")
def promo(code):
    promos_file = open("promo.json", "r")
    promocodes = json.loads(promos_file.read())

    for promocode in promocodes:
        if promocode["code"] == code:
            users_data = read_file('users.json')

            users_data[USER_ID]["promocode"] = code

            write_file('users.json', users_data)

        return json.dumps({"valid": True, "discount": promocode["discount"]})
    return json.dumps({"valid": False})


@app.route("/meals")
def meals_route():
    users_data = read_file('users.json')

    discount = 0

    promocode = users_data[USER_ID]["promocode"]

    meals_copy = json.loads(json.dumps(meals))

    if promocode != None:
        promocodes = read_file('promo.json')

        for p in promocodes:
            if p['code'] == promocode:
                discount = p['discount']

        for meal in meals_copy:
            meal['price'] = (1.0 - discount/100) * meal['price']

    return json.dumps(meals)

@app.route("/orders", methods=["GET", "POST"])
def orders():
    if request.method == 'GET':
        orders_data = read_file('orders.json')
        user_orders = []
        for order_id in orders_data:
            if orders_data[order_id]['user_id'] == USER_ID:
                user_orders.append(orders_data[order_id])
        return json.dumps(user_orders)
    elif request.method == 'POST':
        raw_data = request.data.decode("utf-8")
        data = json.loads(raw_data)

        discount = 0
        users_data = read_file('users.json')
        promocode = users_data[USER_ID]["promocode"]
        if promocode != None:
            promocodes = read_file('promo.json')

            for p in promocodes:
                if p['code'] == promocode:
                    discount = p['discount']



        summ = 0
        meals_copy = json.loads(json.dumps(meals))
        for meal in meals_copy:
            meal_id = meal['id']
            for user_meal_id in data['meals']:
                if user_meal_id == meal_id:
                    summ = summ + meal['price'] * (1.0 - discount/100)
                    break
        new_order_id = str(uuid.uuid4())
        new_order = {
            "id": new_order_id,
            "meals": data['meals'],
            "summ": summ,
            "status": "accepted",
            "user_id": USER_ID
        }

        order_data = read_file("orders.json")
        order_data[new_order_id] = new_order
        write_file('orders.json', order_data)

        return json.dumps({'order_id': new_order_id, "status": new_order['status']})

@app.route("/activeorder")
def activeorder():
    orders_data = read_file('orders.json')
    user_orders = []
    for order_id in orders_data:
        order = orders_data[order_id]
        if order['user_id'] == USER_ID and order['status'] == 'accepted':
           return json.dumps(order)
    return "", 404

@app.route("/orders/<order_id>", methods=["DELETE"])
def one_order(order_id):
    orders_data = read_file("orders.json")
    for saved_order_id in orders_data:
        order = orders_data[saved_order_id]
        if saved_order_id == order_id and order['used_id'] == USER_ID:
            orders_data[saved_order_id]['status'] = 'cancelled'
            write_file('orders.json', orders_data)
        return json.dumps({'order_id': order_id, "status": "cancelled"})
    return "", 404

@app.route("/notification")
def notif():
    sms_client = Client(
        "ACa62b1cec99ca2f42abd0cdbb63709056",
        "0fb11c629600af19006b75f6ed14b0e5"
    )
    message = sms_client.messages.create(
        body="New order is accepted!",
        from_="+14344803924",
        to="+79500006753"

    )
    return json.dumps({"status": True})


app.run("0.0.0.0", 8000)
