from src.API import *
import json

def nome_arquivo(nome_arq,mes):
    nome_arq1 = nome_arq[:31]
    nome_arq2 = nome_arq[33:]
    novo_nome_arq = nome_arq1 + mes + nome_arq2
    return novo_nome_arq

def adiciona_dados(nome_arq):
    linhas = open(nome_arq).readlines()
    for dados in linhas:
        dados = dados.strip().split(';')
        if dados[0] != 'UF':
            dados_json = json.dumps({
                'uf': dados[0],
                'pais':dados[1],
                'classificacao':dados[2],
                'qtd':int(dados[3]),
                'mes':int(dados[4]),
            })
            cadastrar_registro(dados_json)
            
nome_arq = "SISMIGRA_REGISTROS_ATIVOS_2022_00.csv"
for i in range(1,13):
    mes = str(i)
    if int(i) < 10:
        mes = "0" + mes
    
    adiciona_dados(nome_arq)
    print("o arquivo "+nome_arq+" foi adicionado.")
    nome_arq = nome_arquivo(nome_arq,mes)
    print(nome_arquivo(nome_arq,mes))
