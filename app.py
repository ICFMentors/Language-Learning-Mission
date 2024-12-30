from flask import Flask, render_template, request, redirect, session, flash, abort, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import sys
import os

app = Flask(__name__)

db = SQLAlchemy(app)

