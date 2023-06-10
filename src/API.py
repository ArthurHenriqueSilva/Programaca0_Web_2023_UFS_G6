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


# ------------- ROTAS DA API -------------
@app.route('/residentes', methods=['POST'])
def cadastrar_residente(uf, pais, qtd):
    new_residente = Residente(uf, pais, qtd)

@app.route('/provisorios', methods=['POST'])
def cadastrar_provisorio(uf, pais, qtd):
    new_provisorio = Provisorio(uf, pais, qtd)

@app.route('/temporarios', methods=['POST'])
def cadastrar_temporario(uf, pais, qtd):
    new_temporario = Temporario(uf, pais, qtd)



@app.route('/paises', methods=["POST"])
def cadastrar_pais(nome_pais):
    new_pais = Pais(nome_pais)

@app.route('/ufs', methods=['POST'])
def cadastrar_uf(sigla):
    # nome_extenso_dict será um dicionario com key=sigla e value=nome completo da UF
    new_uf = UF(sigla, nome_extenso_dict[sigla])

@app.route('/registros', methods=['POST'])
def cadastrar_registro():
    new_registro = Registro(
        request.json['uf'],
        request.json['pais'],
        request.json['classificacao'],
        request.json['qtd']
    )

    classificacao = new_registro.classificacao.lower() 

    cadastrar_pais(new_registro.pais)
    cadastrar_uf(new_registro.uf)
    
    if(classificacao == 'residente'):
        cadastrar_residente(new_registro.uf, new_registro.pais, new_registro.qtd)
    elif(classificacao == 'provisório'):
        cadastrar_provisorio(new_registro.uf, new_registro.pais, new_registro.qtd)
    else:
        cadastrar_temporario(new_registro.uf, new_registro.pais, new_registro.qtd)


    db.session.add(new_registro)
    db.session.commit()

    return jsonify({
        'id':new_registro.id,
        'uf':new_registro.uf,
        'pais':new_registro.pais,
        'classificacao':new_registro.classificacao,
        'qtd':new_registro.qtd
    })
# ------------- ROTAS DA API -------------