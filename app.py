from crypt import methods
from sys import stdout
from turtle import color
from urllib import request
from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
from flask_migrate import Migrate

# Create a flask instance
app = Flask(__name__)

# Create a secret key
app.config['SECRET_KEY'] = "Codemy Tutorials"

# Create SQLITE Database Start
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
# Create SQLITE Database END

# Create MYSQL Database Start
# RUI = 'mysql://username:password@localhost/db_name'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/blogger'
# Create MYSQL Database END

# Create MYSQL+PYMYSQL Database Start
# RUI = 'mysql://username:password@localhost/db_name'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/blogger'
# Create MYSQL+PYMYSQL Database END

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #create a string
    def __repr__(self):
        return '<Name %r' % self.name

# Create UserForm
class UserForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    email = StringField("What's your email?", validators=[DataRequired()])
    color = StringField("What's your favourite color?")
    submit = SubmitField("Submit")

# export FLASK_ENV=development
# export FLASK_APP=app.py

# Create a form class
class NamerForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

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

# Create route for UserForm page
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    name = None
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is None:
            new_user = User(name = form.name.data,
            email = form.email.data,
            color=form.color.data)
            db.session.add(new_user)
            db.session.commit()
            flash("User Added Successfully !!")
            name = form.name.data
            form.name.data=''
            form.email.data=''
            form.color.data=''
        else:
            flash("User already exists...")
        
    our_all_users = User.query.order_by(desc(User.date_added))
    return render_template('add_user.html',
    form=form,
    name=name,
    our_all_users = our_all_users)

# Create update user page route
@app.route('/user/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    form = UserForm()
    user_to_update = User.query.get_or_404(id)
    if request.method  == "POST":
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        user_to_update.color = request.form['color']
        try:
            db.session.commit()
            flash('User Updated Successfully...')
            return render_template('update_user.html',
            form=form,
            user_to_update=user_to_update,
            id=id)
        except:
            flash('Error please try agin..')
            return render_template('update_user.html',
            form=form,
            user_to_update=user_to_update,
            id=id)
    else:
        return render_template('update_user.html',
        form=form,
        user_to_update=user_to_update,
        id=id)

# Create a route for delete user
@app.route('/user/delete/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User Deleted Successfully...")
        form = UserForm()
        name = None
        our_all_users = User.query.order_by(desc(User.date_added))
        return render_template('add_user.html',
            form=form,
            name=name,
            our_all_users = our_all_users)
    except:
        flash("Error .. Please try again")
        return render_template('add_user.html',
            form=form,
            name=name,
            our_all_users = our_all_users)

# Create name page route
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # validate form
    if form.validate_on_submit():
        flash('Form Submitted Succesfully...')
        name = form.name.data
        form.name.data = ""

    return render_template('name.html',
    name=name,
    form=form)
    #return render_template('name.html')

# Run app
if __name__=="__main__":
    app.run()