from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Dicionário com correspondência de Estados ->  Sigla:Nome_extenso 
estados = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AP': 'Amapá',
    'AM': 'Amazonas',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PR': 'Paraná',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'SC': 'Santa Catarina',
    'SP': 'São Paulo',
    'SE': 'Sergipe',
    'TO': 'Tocantins',
    '--':'Indefinido'
}


app = Flask(__name__)  # create Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:chaveacesso@db-instance-prog-web.cuokvhdjyvdp.us-east-1.rds.amazonaws.com/Database_SISMIGRA'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Registro(db.Model):
    __tablename__ = "Registro"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    uf = db.Column(db.String(2), db.ForeignKey('UF.nome'))
    pais = db.Column(db.String(50), db.ForeignKey('Pais.nome'))
    Classificacao = db.Column(db.String(15))
    qtd = db.Column(db.Integer())
    mes = db.Column(db.Integer())

    def __init__(self, uf, pais, classificacao, qtd, mes):
        self.uf = uf
        self.pais = pais
        self.classificacao = classificacao
        self.qtd = qtd
        self.mes = mes


class Residente(db.Model):
    __tablename__ = 'Residente'

    id = db.Column(db.Integer(), db.ForeignKey('Registro.id'), primary_key=True,)
    uf = db.Column(db.String(2), db.ForeignKey('UF.nome'))
    pais = db.Column(db.String(50), db.ForeignKey('Pais.nome'))
    qtd = db.Column(db.Integer())

    def __init__(self, uf, pais, qtd):
        self.uf = uf
        self.pais = pais
        self.qtd = qtd

class Provisorio(db.Model):
    __tablename__ = 'Provisorio'
    
    id = db.Column(db.Integer(), db.ForeignKey('Registro.id'), primary_key=True)
    uf = db.Column(db.String(2), db.ForeignKey('UF.nome'))
    pais = db.Column(db.String(50), db.ForeignKey('Pais.nome'))
    qtd = db.Column(db.Integer())

    def __init__(self, uf, pais, qtd):
        self.uf = uf
        self.pais = pais
        self.qtd = qtd

class Temporario(db.Model):
    __tablename__ = 'Temporario'
    
    id = db.Column(db.Integer(), db.ForeignKey('Registro.id'), primary_key=True)
    uf = db.Column(db.String(2), db.ForeignKey('UF.nome'))
    pais = db.Column(db.String(50), db.ForeignKey('Pais.nome'))
    qtd = db.Column(db.Integer())

    def __init__(self, uf, pais, qtd):
        self.uf = uf
        self.pais = pais
        self.qtd = qtd

class Fronteirico(db.Model):
    __tablename__ = 'Fronteirico'
    
    id = db.Column(db.Integer(), db.ForeignKey('Registro.id'), primary_key=True)
    uf = db.Column(db.String(2), db.ForeignKey('UF.nome'))
    pais = db.Column(db.String(50), db.ForeignKey('Pais.nome'))
    qtd = db.Column(db.Integer())

    def __init__(self, uf, pais, qtd):
        self.uf = uf
        self.pais = pais
        self.qtd = qtd


class Pais(db.Model):
    __tablename__ = 'Pais'

    nome = db.Column(db.String(50), primary_key=True)

    def __init__(self, nome):
        self.nome = nome


class UF(db.Model):
    __tablename__ = 'UF'

    nome = db.Column(db.String(2), primary_key=True)
    nome_extenso = db.Column(db.String(15))

    def __init__(self, nome, nome_ex):
        self.nome = nome
        self.nome_extenso = nome_ex



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
# Executa o cadastro linha a linha dos arquivos csv. Aciona a execução dos cadastros secundários
@app.route('/registros', methods=['POST'])
def cadastrar_registro():
    # Verifica se a solicitação possui todos os campos necessários
    if not request.json or 'uf' not in request.json or 'pais' not in request.json or 'classificacao' not in request.json or 'qtd' not in request.json:
        return jsonify({'error': 'Solicitação inválida. Certifique-se de fornecer todos os campos necessários.'}), 400

    # Cria um novo registro
    new_registro = Registro(
        request.json['uf'],
        request.json['pais'],
        request.json['classificacao'],
        request.json['qtd'],
        request.json['mes']
    )

    # Converte a classificação para minúsculas
    classificacao = new_registro.classificacao.lower()

    # Cadastra o país e o estado
    cadastrar_pais(new_registro.pais)
    cadastrar_uf(new_registro.uf)

    # Executa a ação apropriada com base na classificação
    if classificacao == 'residente':
        cadastrar_residente(new_registro.uf, new_registro.pais, new_registro.qtd)
    elif classificacao == 'provisório':
        cadastrar_provisorio(new_registro.uf, new_registro.pais, new_registro.qtd)
    elif classificacao == 'temporario':
        cadastrar_temporario(new_registro.uf, new_registro.pais, new_registro.qtd)
    else:
        cadastrar_fronteirico(new_registro.uf, new_registro.pais, new_registro.qtd)

    # Adiciona o novo registro ao banco de dados
    db.session.add(new_registro)
    db.session.commit()

    # Retorna os dados do registro inserido e o código de status 200
    return jsonify({
        'id': new_registro.id,
        'uf': new_registro.uf,
        'pais': new_registro.pais,
        'classificacao': new_registro.classificacao,
        'qtd': new_registro.qtd
    }), 200

# ------------- ROTAS DA API -------------

# with app.app_context():
#     db.create_all()