from flask import Flask, render_template, request, redirect, session, flash, abort, url_for
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