from flask import Flask, render_template, request, redirect, session, flash, abort, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash  # Add import for password hashing
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

import sqlite3
import sys
import os
import openai

# Connect to SQLite database
#conn = sqlite3.connect('data.db')
#cursor = conn.cursor()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'  # Make sure to set your own secret key for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources

db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Make sure User model matches Player table schema

# In your app.py file (or wherever you initialize the app)
with app.app_context():
    db.create_all()


class Player(db.Model, UserMixin):  # Updated to Player to match your table name
    userID = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Automatically increment the userID
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email should be unique and cannot be null
    username = db.Column(db.String(50), unique=True, nullable=False)  # Username is unique and cannot be null
    password = db.Column(db.String(100), nullable=False)  # Password cannot be null
    age = db.Column(db.Integer, nullable=False)  # Age cannot be null
    level = db.Column(db.Integer, default=0, nullable=False)  # Default value for level (0 if not specified)
    experience = db.Column(db.Integer, default=0, nullable=False)  # Default value for experience (0 if not specified)
    current_level_id = db.Column(db.Integer, nullable=True)  # Foreign key for the current level (can be nullable)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.achievement_id', ondelete='SET NULL'))  # Foreign key for achievements

    # Relationships
    achievement = db.relationship('Achievement', backref='players', passive_deletes=True)

    # Constraints (optional)
    __table_args__ = (
        db.CheckConstraint('age >= 0', name='check_age_non_negative'),  # Ensures age is non-negative
        db.CheckConstraint('level > 0', name='check_level_positive'),  # Ensures level is positive
        db.CheckConstraint('experience >= 0', name='check_experience_non_negative')  # Ensures experience is non-negative
    )

    def __repr__(self):
        return f'<Player {self.username}>'


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    age = IntegerField('Age', validators=[DataRequired()])

@app.route('/login')
def login():
def login():
    return render_template('login.html')

@app.route('/select-language')
def selectlanguage():
    return render_template('select-language.html')

@app.route('/create-character')
def createcharacter():
    return render_template('create-character.html')

@app.route('/homepage')
def homepage():
def homepage():
    return render_template('homepage.html')

@app.route('/select-level')
def selectlevel():
    return render_template('select-level.html')


@app.route('/sign-up', methods=["GET", "POST"])
def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Create a new player instance and add data to it
        new_player = Player(
            email=form.email.data,
            username=form.username.data,
            password=generate_password_hash(form.password.data),  # Hash password
            age=form.age.data,
            level=0,  # Default value for level
            experience=0  # Default value for experience
        )

        # Add the new player to the database and commit the changes
        db.session.add(new_player)
        db.session.commit()

        # Redirect to a login page or profile page after successful registration
        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))  # Define the login route

    return render_template('sign-up.html', form=form)


# Other routes (login, homepage, etc.) will follow here


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates all tables defined in the models
        print("Database tables created successfully.")
    app.run(debug=True)
