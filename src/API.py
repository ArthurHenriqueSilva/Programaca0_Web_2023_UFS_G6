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


db = SQLAlchemy(app)

class Registro(db.Model):
    __tablename__ = "Registro"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    uf = db.Column(db.String(2), db.ForeignKey('uf.Nome'))
    Pais = db.Column(db.String(50), db.ForeignKey('Pais.Nome'))
    Classificacao = db.Column(db.String(15))
    qtd = db.Column(db.Integer())

    def __init__(self, uf, pais, classificacao, qtd):
        self.uf = uf
        self.pais = pais
        self.classificacao = classificacao
        self.qtd = qtd


class Residente(db.Model):
    __tablename__ = 'Residente'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    uf = db.Column(db.String(2), db.ForeignKey('uf.Nome'))
    Pais = db.Column(db.String(50), db.Foreignkey('Pais.Nome'))
    qtd = db.Column(db.Integer())

    def __init__(self, uf, pais, qtd):
        self.uf = uf
        self.pais = pais
        self.qtd = qtd

class Provisorio(db.Model):
    __tablename__ = 'Provisorio'
    
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    uf = db.Column(db.String(2), db.ForeignKey('uf.Nome'))
    Pais = db.Column(db.String(50), db.Foreignkey('Pais.Nome'))
    qtd = db.Column(db.Integer())

    def __init__(self, uf, pais, qtd):
        self.uf = uf
        self.pais = pais
        self.qtd = qtd

class Temporario(db.Model):
    __tablename__ = 'Temporario'
    
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    uf = db.Column(db.String(2), db.ForeignKey('UF.Nome'))
    Pais = db.Column(db.String(50), db.Foreignkey('Pais.Nome'))
    qtd = db.Column(db.Integer())

    def __init__(self, uf, pais, qtd):
        self.uf = uf
        self.pais = pais
        self.qtd = qtd


class Pais(db.Model):
    __tablename__ = 'Pais'

    nome = db.Column(db.String(50), primarykey=True)

    def __init__(self, nome):
        self.nome = nome


class UF(db.Model):
    __tablename__ = 'UF'

    nome = db.Column(db.String(2), primarykey=True)
    nome_extenso = db.Column(db.String(15))

    def __init__(self, nome, nome_ex):
        self.nome = nome
        self.nome_extenso = nome_ex
