from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from aux_data import estados, meses
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)  # create Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:chaveacesso@db-instance-prog-web.cuokvhdjyvdp.us-east-1.rds.amazonaws.com/Database_SISMIGRA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from models import Registro, Residente, Provisorio, Temporario, Fronteirico, Pais, UF

users = {
    "arthur": generate_password_hash("henrique"),
    "guilherme": generate_password_hash("linard"),
    "raul": generate_password_hash("miguel")
}

# ---------- Funções Aux DA API -------------
# Cadastro de Imigrante Residente
def cadastrar_residente(uf, pais, qtd):
    new_residente = Residente(uf, pais, qtd)
    db.session.add(new_residente)
    db.session.commit()

def cadastrar_fronteirico(uf, pais, qtd):
    new_front = Fronteirico(uf, pais, qtd)
    db.session.add(new_front)
    db.session.commit()

# Cadastro de Imigrante Provisório
def cadastrar_provisorio(uf, pais, qtd):
    new_provisorio = Provisorio(uf, pais, qtd)
    db.session.add(new_provisorio)
    db.session.commit()

# Cadastro de Imigrante Temporário
def cadastrar_temporario(uf, pais, qtd):
    new_temporario = Temporario(uf, pais, qtd)
    db.session.add(new_temporario)
    db.session.commit()

# Cadastro de País
def cadastrar_pais(nome_pais):
    # Verifica se o país já existe no banco de dados
    existing_pais = Pais.query.filter_by(nome=nome_pais).first()
    if existing_pais:
        # País já existe, faça o tratamento adequado
        return

    new_pais = Pais(nome_pais)
    db.session.add(new_pais)
    db.session.commit()

# Cadastro de UF
def cadastrar_uf(sigla):
    # Verifica se a UF já existe no banco de dados
    existing_uf = UF.query.filter_by(nome=sigla).first()
    if existing_uf:
        # UF já existe, faça o tratamento adequado
        return

    new_uf = UF(sigla, estados[sigla])
    db.session.add(new_uf)
    db.session.commit()

# 1: Qual a distribuição de imigrantes do país X?

def consulta_distribuicao_imigrantes_pais(pais_filtro):
    pais_filtro = pais_filtro.upper()
    with app.app_context():
        distribuicao = db.session.query(Registro.classificacao, db.func.sum(Registro.qtd).label('Total')) \
            .filter(Registro.pais == pais_filtro) \
            .group_by(Registro.classificacao)\
            .all()

        return dict(sorted(distribuicao, key=lambda tup: tup[1]))
#2: Consulta de qual país com mais imigração entre os meses x e y

def consulta_pais_imigracao(mes_inicial, mes_final):
    with app.app_context():
        pais = db.session.query(Registro.pais, db.func.sum(Registro.qtd).label('Total'))\
                    .filter(Registro.mes.between(mes_inicial, mes_final))\
                    .group_by(Registro.pais)\
                    .order_by(db.desc('Total'))\
                    .first()

        return str(pais.pais), pais.Total

#3: Consulta de qual é o tipo principal de imigrante que recebemos no brasil entre os meses x e y

def consulta_tipo_imigrante(mes_inicial, mes_final):
    with app.app_context():
        tipo = db.session.query(Registro.classificacao, db.func.sum(Registro.qtd).label('Total'))\
                    .filter(Registro.mes.between(mes_inicial, mes_final))\
                    .group_by(Registro.classificacao)\
                    .order_by(db.desc('Total'))\
                    .first()

        return str(tipo.classificacao)

#4: Consulta de qual é o período do ano que recebmos mais imigrantes do tipo X

def consulta_periodo_popular(classificacao_filtro):
    classificacao_filtro = classificacao_filtro.capitalize()
    with app.app_context():
        periodo = db.session.query(Registro.mes, db.func.sum(Registro.qtd).label('Total'))\
                    .filter(Registro.classificacao == classificacao_filtro)\
                    .group_by(Registro.mes)\
                    .order_by(db.desc('Total'))\
                    .first()

        return str(periodo.mes)

def uf_nome_extenso(sigla):
    filtro = UF.query.filter_by(nome=sigla).first()
    nome_extenso_uf = filtro.nome_extenso
    return nome_extenso_uf

# 5: Qual o evento do estado X que chama mais atenção para o imigrante de tipo Y?

def consulta_mes_mais_atrativo(uf_filtro, classificacao_filtro):
    with app.app_context():
        registro = db.session.query(Registro.mes, db.func.sum(Registro.qtd).label('Total'))\
            .filter(Registro.uf == uf_filtro, Registro.classificacao == classificacao_filtro) \
            .group_by(Registro.mes) \
            .order_by(db.desc('Total')) \
            .first()
        
    return registro


# 6: Qual o estado que possui mais registros de imigrantes residentes no mes X?

def consulta_estado_mais_residentes(mes_filtro):
    with app.app_context():
        estado = db.session.query(Residente.uf, db.func.count().label('Total')) \
            .filter(Registro.mes == mes_filtro) \
            .group_by(Residente.uf) \
            .order_by(db.desc('Total')) \
            .first()
        nome_ext = uf_nome_extenso(str(estado.uf))
        return(nome_ext)
    

# 7: Qual estado recebe mais imigrantes do país X?

def consulta_estado_com_mais_imigrantes(pais_filtro):
    pais_filtro = pais_filtro.upper()
    with app.app_context():
        # Filtrar os registros pelo país especificado
        registros = Registro.query.filter_by(pais=pais_filtro).all()
        
        # Calcular a soma da coluna "QTD" para cada estado
        soma_por_estado = {}
        for registro in registros:
            estado = registro.uf
            soma_por_estado[estado] = soma_por_estado.get(estado, 0) + registro.qtd
        
        # Encontrar o estado com a maior soma
        estado_mais_imigrantes = max(soma_por_estado, key=soma_por_estado.get)
        
        # Obter o nome completo do estado
        nome_ext = uf_nome_extenso(estado_mais_imigrantes)
        # Retornar o estado e a quantidade de imigrantes
        return estado_mais_imigrantes, soma_por_estado[estado_mais_imigrantes]

# 8: Qual o tipo de imigração que mais ocorre a partir do País X?

def consulta_imigracao_recorrente_do_pais(pais_filtro):
    pais_filtro = pais_filtro.upper()
    with app.app_context():
        registros = Registro.query.filter_by(pais=pais_filtro).all()
        soma_por_tipo = {}
        for registro in registros:
            tipo_imigraccao = registro.classificacao
            soma_por_tipo[tipo_imigraccao] = soma_por_tipo.get(tipo_imigraccao, 0) + 1
        
        tipo_mais_recorrente = max(soma_por_tipo, key=soma_por_tipo.get)
        return str(tipo_mais_recorrente)

# 9: Qual a quantidade de imigrante do país no período de maior chegada de imigrantes no país?

def consulta_quantidade_pais_periodo_popular(periodo_popular, pais_filtro):
    pais_filtro = pais_filtro.upper()
    with app.app_context():
        registros = db.session.query(Registro.pais, db.func.sum(Registro.qtd).label('Total')) \
            .filter(Registro.pais == pais_filtro, Registro.mes == periodo_popular) \
            .group_by(Registro.pais) \
            .order_by(db.desc('Total')) \
            .first()

    return str(registros.Total)


# 10: Qual a classificação do país X que mais recebemos no tempo Y?

def consulta_classificacao_pais_tempo(pais_filtro, mes_filtro):
    pais_filtro = pais_filtro.upper()
    with app.app_context():
        registros = db.session.query(Registro.classificacao, db.func.sum(Registro.qtd).label('Total')) \
                    .filter(Registro.pais == pais_filtro, Registro.mes == mes_filtro) \
                    .group_by(Registro.classificacao) \
                    .order_by(db.desc('Total')) \
                    .first()

        return str(registros.classificacao)

#Rota 1

@app.route('/api/distribuicao-de-imigrantes-pelo-pais', methods=['POST'])
def distribuicao_imigrantes_pais():
    pais_filtro = request.json.get('pais')
    distribuicao = consulta_distribuicao_imigrantes_pais(pais_filtro)
    print(distribuicao)
    return jsonify({'Total_Fronteirico': distribuicao.get('Fronteiriço', 0), 'Total_Provisorio': distribuicao.get('Provisório', 0), 'Total_Residente': distribuicao.get('Residente', 0), 'Total_Temporario': distribuicao.get('Temporário', 0)})

#Rota 2
@app.route('/api/pais-com-mais-imigracao-no-periodo', methods=['POST'])
def pais_com_mais_imigracao():
    meses_filtro = [request.json.get('mes_inicial'), request.json.get('mes_final')]
    pais, qtd_pais = consulta_pais_imigracao(mes_inicial=meses_filtro[0], mes_final=meses_filtro[1])
    return jsonify({'pais': pais, 'qtd_pais': qtd_pais, 'mes_inicial': meses_filtro[0], 'mes_final': meses_filtro[1]})

#Rota 3
@app.route('/api/tipo-de-imigracao-mais-popular-no-periodo', methods=['POST'])
def tipo_imigracao_popular():
    meses_filtro = [request.json.get('mes_inicial'), request.json.get('mes_final')]
    tipo = consulta_tipo_imigrante(mes_inicial=meses_filtro[0], mes_final=meses_filtro[1])
    return jsonify({'tipo': tipo, 'mes_inicial': meses_filtro[0], 'mes_final': meses_filtro[1], 'pais': 'Brasil'})

#Rota 4
@app.route('/api/periodo-mais-popular-para-o-tipo', methods=['POST'])
def periodo_popular():
    classificacao_filtro = request.json.get('classificacao')
    periodo = consulta_periodo_popular(classificacao_filtro=classificacao_filtro)
    return jsonify({'periodo': periodo, 'classificacao': classificacao_filtro})

#Rota 5

@app.route('/api/mes-que-chama-mais-atencao-para-o-imigrante-em-um-estado', methods=['POST'])
def mes_mais_atrativo():
    uf_filtro = request.json.get('uf')
    classificacao_filtro = request.json.get('classificacao')
    registro = consulta_mes_mais_atrativo(uf_filtro=uf_filtro, classificacao_filtro=classificacao_filtro)
    if registro is None:
        return jsonify({'mes': '0', 'uf': uf_filtro, 'classificacao': classificacao_filtro})
    return jsonify({'mes': str(registro.mes), 'uf': uf_filtro, 'classificacao': classificacao_filtro})

#Rota 6
@app.route('/api/estado-com-mais-residentes-no-mes', methods=['POST'])
def estado_mais_residentes():
    mes_filtro = request.json.get('mes')
    estado_mais_residentes = consulta_estado_mais_residentes(mes_filtro=mes_filtro)
    estado_nome = estado_mais_residentes
    return jsonify({'estado': estado_nome, 'mes': mes_filtro})

#Rota 7

@app.route('/api/estado-com-mais-imigrantes', methods=['POST'])
def estado_mais_imigrantes():
    pais_filtro = request.json.get('pais')
    estado_mais_imigrantes, qtd_estado = consulta_estado_com_mais_imigrantes(pais_filtro)
    estado_nome = estados[estado_mais_imigrantes]
    return jsonify({'estado': estado_nome, 'quantidade': qtd_estado, 'pais': pais_filtro})

#Rota 8

@app.route('/api/maior-tipo-imigrante-do-pais', methods=['POST'])
def tipo_imigrante_pais():
    pais_filtro = request.json.get('pais')
    tipo_imigrante = consulta_imigracao_recorrente_do_pais(pais_filtro)
    return jsonify({'pais': pais_filtro, 'tipo': tipo_imigrante})

#Rota 9

@app.route('/api/quantidade-do-pais-no-periodo-de-maior-imigracao', methods=['POST'])
def pais_imigracao_periodo_popular():
    pais_filtro = request.json.get('pais')
    mes_filtro = request.json.get('mes')
    qtd_pais = consulta_quantidade_pais_periodo_popular(mes_filtro, pais_filtro)
    return jsonify({'pais': pais_filtro, 'mes': mes_filtro, 'quantidade': qtd_pais})    


#Rota 10

@app.route('/api/classificacao-de-imigrante-mais-popular-em-um-mes', methods=['POST'])
def classificacao_pais_tempo():
    pais_filtro = request.json.get('pais')
    mes_filtro = request.json.get('mes')
    classificacao_popular = consulta_classificacao_pais_tempo(pais_filtro, mes_filtro)
    return jsonify({'pais': pais_filtro, 'mes': mes_filtro, 'classificacao': classificacao_popular})

# ------------- ROTAS DA API -------------
