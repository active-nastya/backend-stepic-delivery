from flask import Flask
import random
app = Flask(__name__)

stepik_alive = True
workhours_open = "10:00"
workhours_closes = "21:00"
promotion_text = "Сегодня скидка 15 % по промокоду stepik!"


promotions = [
    "Cкидка 15% по проомокоду stepik",
    "Скидка 10% по промокоду summer",
    "Удваиваем все пиццы по промокоду udodopizza"


]


@app.route("/")
def hello():
    return "Hello"

@app.route("/alive")
def alive():
    if stepik_alive == True:
        return '{alive: True}'
    else:
         return '{alive: false}'

@app.route("/workhours")
def workhours():
    return '{openes: " '+ workhours_open +' "", closes: " ' + workhours_closes + ' "}'


@app.route("/promotion")
def promotion():
    promotion_number = random.randint(0,2)
    return '{"promotion":" '+promotions[promotion_number]+' "}'


@app.route("/promo/<code>")
def checkpromo(code):
    if code == "stepik":
        return '{"valid":true, "discount":15}'
    elif code == "summer":
        return '{"valid":true, "discount": 10}'
    elif code == "pleaseplease":
        return '{"valid":true, "discount": 5}'
    return '{valid:false, "discount": 0}'



app.run("0.0.0.0", 8000)
