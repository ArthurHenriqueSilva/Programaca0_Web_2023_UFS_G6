from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, ForeignKey, Integer, String, Column, Float, DateTime, Boolean
from sqlalchemy.orm import Mapped, Session
from sqlalchemy_utils import JSONType

import jwt
import os
from datetime import datetime as dt, timedelta

app = Flask(__name__)  # create Flask app

app.config['SQLALCHEMY_DATABASE_URI'] = '**'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False