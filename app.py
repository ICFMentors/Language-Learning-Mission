from flask import Flask, render_template, request, redirect, session, flash, abort, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash  # Add import for password hashing
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import chat

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
def load_user(player_id):
    return Player.query.get(int(player_id)) 

# In your app.py file (or wherever you initialize the app)
with app.app_context():
    db.create_all()


class Player(db.Model, UserMixin):  # Updated to Player to match your table name
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Automatically increment the userID
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email should be unique and cannot be null
    username = db.Column(db.String(50), unique=True, nullable=False)  # Username is unique and cannot be null
    password = db.Column(db.String(100), nullable=False)  # Password cannot be null
    age = db.Column(db.Integer, nullable=False)  # Age cannot be null
    level = db.Column(db.Integer, default=0, nullable=False)  # Default value for level (0 if not specified)
    experience = db.Column(db.Integer, default=0, nullable=False)  # Default value for experience (0 if not specified)
    current_level_id = db.Column(db.Integer, nullable=True)  # Foreign key for the current level (can be nullable)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.achievement_id', ondelete='SET NULL'))  # Foreign key for achievements

    def get_id(self):
        return str(self.user_id)

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

class Achievement(db.Model):
    __tablename__ = 'achievement'  # Table name matches the foreign key reference
    achievement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Achievement {self.name}>'


@login_manager.user_loader
def load_user(player_id):
    return Player.query.get(int(player_id))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check if user exists and if password matches
        user = Player.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):  # Check hashed password
            login_user(user)
            return redirect(url_for('homepage'))  # Redirect to the homepage after login
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/select-language')
def select_language():
    return render_template('select-language.html')

@app.route('/create-character')
def create_character():
    return render_template('create-character.html')

@app.route('/homepage')
@login_required
def homepage():
    return render_template('homepage.html')


@app.route('/select-level')
def select_level():
    return render_template('select-level.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Create a new player instance and add data to it
        new_player = Player(
            email=form.email.data,
            username=form.username.data,
            password=generate_password_hash(form.password.data),  # Hash password
            age=form.age.data,
            level=1,  # Default value for level
            experience=0  # Default value for experience
        )

        # Add the new player to the database and commit the changes
        db.session.add(new_player)
        db.session.commit()


        # Automatically log the user in after registration
        login_user(new_player)

        flash("Registration successful! Welcome!")
        return redirect(url_for('homepage'))  # Redirect to homepage after sign-up

    return render_template('signup.html', form=form)


@app.route('/game')
def playGame():
    return render_template('game.html')
@app.route('/api/translate')
def interact():
    #data = request.get_json()
    original_text=request.args.get('text')
    print(original_text)
    return jsonify({
            'translated_text': chat.translate_text(original_text)
        })
    
    # Check the action from the request
    #if data.get('action') == 'interact_with_cashier':
        # Respond with a message from the cashier
        #return jsonify({
        #    'message': 'Hello! Thank you for stopping by. How can I assist you today?'
        #})
    # else:
    #     # Default response for unknown actions
    #     return jsonify({
    #         'message': 'I am not sure what you mean.'
    #     }), 400



if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates all tables defined in the models
        print("Database tables created successfully.")
    app.run(debug=True)


try:
    db.session.commit()
except Exception as e:
    print(f"Error committing to database: {e}")

if Player.level <= 0:
    Player.level = 1  # Set a default level (or another positive number)
