from sys import stdout
from flask import Flask, render_template

# Create a flask instance
app = Flask(__name__)

# Create home page route decorator
@app.route('/')
# def index():
#     return "<h1>Hello World</h1>"
def index():
    user_name = "John"
    stuff = "<h1>this is a <i>italic</i> string with html</h1>"
    pizza = ["Dominos", "PizzaHut", "Joeys", 33]
    return render_template('index.html',
            user_name=user_name,
            stuff=stuff,
            pizza=pizza)

# Create users page route decorator
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

# Custom error 404 page route
@app.errorhandler(404)
def error_404(e):
    return render_template('error_404.html'), 404

# Custom error 500 page route
@app.errorhandler(500)
def error_500(e):
    return render_template('error_404.html'), 500

app.run()