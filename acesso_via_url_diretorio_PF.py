import requests
import re
import json
from src.API import *
from bs4 import BeautifulSoup

directory_url = 'https://servicos.dpf.gov.br/dadosabertos/SISMIGRA/'

response = requests.get(directory_url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

file_links = []
for link in soup.find_all('a'):
    file_url = link.get('href')
    if re.match(r'SISMIGRA_REGISTROS_ATIVOS_2022_\d{2}.csv', file_url):
        file_links.append(directory_url + file_url)



'''
print(file_links)
lista esperada:  ['https://servicos.dpf.gov.br/dadosabertos/SISMIGRA/SISMIGRA_REGISTROS_ATIVOS_2022_01.csv', 
'https://servicos.dpf.gov.br/dadosabertos/SISMIGRA/SISMIGRA_REGISTROS_ATIVOS_2022_02.csv', 
'https://servicos.dpf.gov.br/dadosabertos/SISMIGRA/SISMIGRA_REGISTROS_ATIVOS_2022_03.csv', 
'https://servicos.dpf.gov.br/dadosabertos/SISMIGRA/SISMIGRA_REGISTROS_ATIVOS_2022_04.csv', 
'https://servicos.dpf.gov.br/dadosabertos/SISMIGRA/SISMIGRA_REGISTROS_ATIVOS_2022_05.csv', 
'https://servicos.dpf.gov.br/dadosabertos/SISMIGRA/SISMIGRA_REGISTROS_ATIVOS_2022_06.csv', 
'https://servicos.dpf.gov.br/dadosabertos/SISMIGRA/SISMIGRA_REGISTROS_ATIVOS_2022_07.csv', 
'https://servicos.dpf.gov.br/dadosabertos/SISMIGRA/SISMIGRA_REGISTROS_ATIVOS_2022_08.csv', 
'https://servicos.dpf.gov.br/dadosabertos/SISMIGRA/SISMIGRA_REGISTROS_ATIVOS_2022_09.csv', 
'https://servicos.dpf.gov.br/dadosabertos/SISMIGRA/SISMIGRA_REGISTROS_ATIVOS_2022_10.csv', 
'https://servicos.dpf.gov.br/dadosabertos/SISMIGRA/SISMIGRA_REGISTROS_ATIVOS_2022_11.csv', 
'https://servicos.dpf.gov.br/dadosabertos/SISMIGRA/SISMIGRA_REGISTROS_ATIVOS_2022_12.csv']
'''

for file_url in file_links:
    month = file_url[-6:-4] # 01, 02, ..., 12
    response = requests.get(file_url)
    csv_content = response.content
    csv_text = csv_content.decode('utf-8').replace('\r', '').strip()
    rows = csv_text.split('\n')
    data = [row.split(';') for row in rows]
    for dado in data:
        if dado[0] != 'UF':
            dado_json = json.dumps({
                'uf': dado[0],
                'pais':dado[1],
                'classificacao':dado[2],
                'qtd':int(dado[3]),
                'mes':int(month),
            })
            cadastrar_registro(dado_json)
