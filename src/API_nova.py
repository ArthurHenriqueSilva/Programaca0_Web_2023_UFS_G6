from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from aux_data import estados, meses
app = Flask(__name__)  # create Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:chaveacesso@db-instance-prog-web.cuokvhdjyvdp.us-east-1.rds.amazonaws.com/Database_SISMIGRA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from models import Registro, Residente, Provisorio, Temporario, Fronteirico, Pais, UF
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
# ---------- Funções Aux DA API -------------
# ------------- ROTAS DA API -------------
def uf_nome_extenso(sigla):
    filtro = UF.query.filter_by(nome=sigla).first()
    nome_extenso_uf = filtro.nome_extenso
    return nome_extenso_uf

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
        print(nome_ext, soma_por_estado[estado_mais_imigrantes])
        # Retornar o estado e a quantidade de imigrantes
        return estado_mais_imigrantes, soma_por_estado[estado_mais_imigrantes]
    


@app.route('/api/estado-com-mais-imigrantes', methods=['POST'])
def estado_mais_imigrantes():
    pais_filtro = request.json.get('pais')
    estado_mais_imigrantes, qtd_estado = consulta_estado_com_mais_imigrantes(pais_filtro)
    estado_nome = estados[estado_mais_imigrantes]
    return jsonify({'estado': estado_nome, 'quantidade': qtd_estado})

# ------------- ROTAS DA API -------------
