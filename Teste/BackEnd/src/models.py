from API import db


class Registro(db.Model):
    __tablename__ = "Registro"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    uf = db.Column(db.String(2), db.ForeignKey('UF.nome'))
    pais = db.Column(db.String(50), db.ForeignKey('Pais.nome'))
    classificacao = db.Column(db.String(15))
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
