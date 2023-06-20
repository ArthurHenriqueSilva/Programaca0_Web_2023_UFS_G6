from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from API import Registro, Residente, Provisorio, Temporario, Fronteirico, UF, app, db

#1: Qual a distribuição de imigrantes pelo país?

#5: Qual o evento do estado X que chama mais atenção para o imigrante de tipo Y?

"""

Consulta SQL:

SELECT mes, SUM(qtd) AS Total
FROM PUBLIC."Registro"
WHERE uf = 'X' AND classificacao = 'Y'
GROUP BY mes
ORDER BY Total DESC
LIMIT 1;

"""

def mes_mais_atrativo (uf_filtro, classificacao_filtro):
    with app.app_context():
        
        registros = db_session.query(Registro.mes, db.func.sum(Registro.qtd)).filter(Registro.uf == uf_filtro, Registro.Classificacao == classificacao_filtro).all() \
            .group_by(Registro.mes) \
            .order_by(db.desc('Total')) \
            .first()
        
    return str(registros.mes)

#9: Qual país mais imigra no período de maior chegada de imigrantes no país?

"""

Consulta SQL:

SELECT pais, SUM(qtd) AS Total
FROM PUBLIC."Registro"
WHERE mes = periodo_de_maior_chegada
GROUP BY pais
ORDER BY Total DESC
LIMIT 1;

"""

#Utiliza como base as consultas das questões 2 e 4

def consulta_pais_imigracao():

    pais = db.session.query(Registro.pais, db.func.sum(Registro.qtd).label('Total')) \
            .group_by(Registro.pais) \
            .order_by(db.desc('Total')) \
            .first()

    return str(pais.pais)

def consulta_periodo_popular():
    periodo = db.session.query(Registro.mes, db.func.sum(Registro.qtd).label('Total')) \
            .group_by(Registro.mes) \
            .order_by(db.desc('Total')) \
            .first()

    return str(periodo.mes)

def consulta_pais_imigracao_periodo_popular():
    pais_popular = consulta_pais_imigracao()
    periodo_popular = consulta_periodo_popular()
    pais_popular = pais_popular.upper()
    with app.app_context():

        registros = db.session.query(Registro.pais, db.func.sum(Registro.qtd)).filter(Registro.pais == pais_popular, Registro.mes == periodo_popular).all() \
            .group_by(Registro.pais) \
            .order_by(db.desc('Total')) \
            .first()
        
    return str(registros.pais)

#10: Qual a classificação do país X que mais recebemos no tempo Y?

"""

Consulta SQL:

SELECT pais, SUM(qtd) AS Total
FROM PUBLIC."Registro"
WHERE pais = 'X' AND mes = Y
GROUP BY classificacao
ORDER BY Total DESC
LIMIT 1;

"""

def classificacao_pais_tempo(pais_filtro, mes_filtro):
    pais_filtro = pais_filtro.upper()
    with app.app_context():
        
        registros = Registro.query.filter(Registro.pais == pais_filtro, Registro.mes == mes_filtro).all()

        soma_classificacao = {}
        for registro in registros:
            tipo_classificacao = registro.Classificacao
            soma_classificacao[tipo_classificacao] = soma_classificacao.get(tipo_classificacao, 0) + 1
        
        classificacao_mais_recebida = max(soma_classificacao, key=soma_classificacao.get)
        return classificacao_mais_recebida
