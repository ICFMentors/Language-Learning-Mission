from flask import Flask, render_template, request, redirect, session, flash, abort, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import sys
import os
import openai

app = Flask(__name__)

db = SQLAlchemy(app)

# Connect to SQLite database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup')
def index():
    return render_template('signup.html')

@app.route('/login')
def index():
    return render_template('login.html')

@app.route('/select-language')
def index():
    return render_template('select-language.html')

@app.route('/create-character')
def index():
    return render_template('create-character.html')

@app.route('/homepage')
def index():
    return render_template('homepage.html')

@app.route('/select-level')
def index():
    return render_template('select-level.html')