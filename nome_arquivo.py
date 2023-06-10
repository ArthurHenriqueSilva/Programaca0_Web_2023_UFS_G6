def nome_arquivo(nome_arq,mes):
    nome_arq1 = nome_arq[:31]
    nome_arq2 = nome_arq[33:]
    novo_nome_arq = nome_arq1 + mes + nome_arq2
    return novo_nome_arq

for i in range(1,13):
    nome_arq = "SISMIGRA_REGISTROS_ATIVOS_2022_00.csv"
    mes = str(i)
    if int(i) < 10:
        mes = "0" + mes
    print(nome_arquivo(nome_arq,mes))
