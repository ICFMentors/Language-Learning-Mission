from flask import Flask, render_template, request, redirect, session, flash, abort, url_for, jsonify, send_from_directory
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
    level = db.Column(db.Integer, nullable=False)  # Default value for level (0 if not specified)
    current_level_id = db.Column(db.Integer, nullable=True)  # Foreign key for the current level (can be nullable)
    current_player = db.Column(db.Integer, default=0, nullable=False)
    lang = db.Column(db.String(50), nullable=False)
    learning_lang = db.Column(db.String(50), nullable=False)
    def get_id(self):
        return str(self.user_id)

    # Constraints (optional)
    __table_args__ = (
        db.CheckConstraint('age >= 0', name='check_age_non_negative'),  # Ensures age is non-negative
        db.CheckConstraint('level > 0', name='check_level_positive'),  # Ensures level is positive
    )

    def __repr__(self):
        return f'<Player {self.username}>'


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    age = IntegerField('Age', validators=[DataRequired()])

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

@app.route('/select-language', methods=['GET', 'POST'])
def select_language():
    if(request.method == 'GET'): 
        return render_template('select-language.html')  
    else:
            
        playerId = session["_user_id"]
        player = Player.query.filter_by(user_id=playerId).first()
        #pass
        if player:
            player.lang = request.form['learning']
            player.learning_lang = request.form['learningIn']
            print(player.lang)
            print(player.learning_lang)   
            try:
                db.session.commit()
                return redirect('/select-level')
            except Exception as e:
                 error_message = 'There was an issue updating the player information. Please try again later.'
                 return render_template('select-language.html', player=[player], error_message=error_message)
        # else:
            # error_message = 'player not found.'
           # return render_template('select-level.html')

# Route for the character selection page
@app.route('/create-character', methods=['GET', 'POST'])
@login_required
def create_character():
#     if request.method == 'POST':
#         selected_character = request.json.get('character')
#         if not selected_character:
#             return jsonify({"error": "No character selected!"}), 400
        
#         # Update the player's current character in the database
#         current_player = Player.query.get(session['_user_id'])  # Use Flask-Login to get the logged-in player
#         if current_player:
#             current_player.current_level_id = selected_character  # Replace with the appropriate field for character
#             db.session.commit()
#             return jsonify({"message": f"Character {selected_character} selected successfully!"})
#         else:
#             return jsonify({"error": "Player not found!"}), 404
    
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
            lang=0,
            learning_lang=0
        )

        # Add the new player to the database and commit the changes
        db.session.add(new_player)
        db.session.commit()


        # Automatically log the user in after registration
        login_user(new_player)

        flash("Registration successful! Welcome!")
        return redirect(url_for('homepage'))  # Redirect to homepage after sign-up

    return render_template('signup.html', form=form)

# @app.route('/api/save-languages', methods=['POST'])
# @login_required
# def save_languages():
#     data = request.get_json()
#     learning_in = data['learningIn']
#     learning = data['learning']

#     if not learning_in or not learning:
#         return jsonify({"success": False, "error": "Both languages must be selected!"}), 400

#     # Update the current user's language preferences in the database
#     current_player = Player.query.get(session['_user_id'])
#     if current_player:
#         current_player.lang = learning_in
#         current_player.learning_lang = learning
#         db.session.commit()
#         return jsonify({"success": True})
#     else:
#         return jsonify({"success": False, "error": "Player not found!"}), 404


@app.route('/game')
def playGame():
    return render_template('game.html')
@app.route('/phasereditorgame/<path:filename>')
def playPhaserEditorGame(filename):
    return send_from_directory('phasereditorgame', filename)


@app.route('/town')
def playTown():
    return render_template('town.html')
@app.route('/api/translate')
def interact():
    #data = request.get_json()
    original_text=request.args.get('text')
    print(original_text)
    playerId = session["_user_id"]
    player = Player.query.filter_by(user_id=playerId).first()
    return jsonify({
            'translated_text': chat.translate_text(original_text, player.learning_lang, player.lang, player.age)
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

