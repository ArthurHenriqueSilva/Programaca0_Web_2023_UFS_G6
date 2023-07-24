from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from API import Registro, Residente, UF, app, db


# Função auxiliar para retornar o nome completo do estado com base na sigla
def uf_nome_extenso(sigla):
    filtro = UF.query.filter_by(nome=sigla).first()
    nome_extenso_uf = filtro.nome_extenso
    return nome_extenso_uf


'''
Comando SQL:

SELECT uf, SUM(qtd) AS Total
FROM PUBLIC."Registro"
WHERE classificacao = 'Residente'
GROUP BY UF
ORDER BY Total DESC
LIMIT 1

'''
# 6: Qual o estado que possui mais registros de imigrantes residentes?
def consulta_estado_mais_residentes():
    with app.app_context():
        estado = db.session.query(Residente.uf, db.func.count().label('Total')) \
            .group_by(Residente.uf) \
            .order_by(db.desc('Total')) \
            .first()
        nome_ext = uf_nome_extenso(str(estado.uf))
        print(nome_ext)
        return(nome_ext)




'''
Comando SQL:

SELECT UF, SUM(QTD) AS Total
FROM PUBLIC."Registro" WHERE PAIS = 'DINAMARCA'
GROUP BY UF
ORDER BY Total DESC
LIMIT 1;


'''
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


'''
Comando SQL:

SELECT classificacao, SUM(qtd) AS Total
FROM PUBLIC."Registro"
WHERE pais = 'X'
GROUP BY classificacao
ORDER BY Total DESC
LIMIT 1
'''

# Qual o tipo de imigração que mais ocorre a partir do País X?
def consulta_imigracao_recorrente_do_pais(pais_filtro):
    pais_filtro = pais_filtro.upper()
    with app.app_context():
        registros = Registro.query.filter_by(pais=pais_filtro).all()
        soma_por_tipo = {}
        for registro in registros:
            tipo_imigraccao = registro.classificacao
            soma_por_tipo[tipo_imigraccao] = soma_por_tipo.get(tipo_imigraccao, 0) + 1
        
        tipo_mais_recorrente = max(soma_por_tipo, key=soma_por_tipo.get)
        print(tipo_mais_recorrente)
        return tipo_mais_recorrente

if __name__ == '__main__':
    consulta_estado_mais_residentes()
    consulta_estado_com_mais_imigrantes('Dinamarca')
    consulta_imigracao_recorrente_do_pais('França')
