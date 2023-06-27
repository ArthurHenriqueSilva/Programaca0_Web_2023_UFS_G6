from flask import Flask
from flask_sqlalchemy import SQLAlchemy
    
from API import *

# Consulta de qual país com mais imigração Q2
def consulta_pais_imigracao():
    pais = db.session.query(Registro.pais, db.func.sum(Registro.qtd).label('Total'))\
                    .group_by(Registro.pais)\
                    .order_by(db.desc('Total'))\
                    .first()

    return str(pais.pais)

# Consulta de qual é o tipo principal de imigrante que recebemos no brasil Q3
def consulta_tipo_imigrante():
    tipo = db.session.query(Registro.classificacao, db.func.sum(Registro.qtd).label('Total'))\
                    .group_by(Registro.classificacao)\
                    .order_by(db.desc('Total'))\
                    .first()

    return str(tipo.classificacao)

# Consulta de qual é o período do ano que recebmos mais imigrantes Q4
def consulta_periodo_popular():
    periodo = db.session.query(Registro.mes, db.func.sum(Registro.qtd).label('Total'))\
                    .group_by(Registro.mes)\
                    .order_by(db.desc('Total'))\
                    .first()

    return str(periodo.mes)