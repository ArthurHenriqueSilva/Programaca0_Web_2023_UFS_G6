import requests
import re
from bs4 import BeautifulSoup
import json
import unittest
from API import app, db

class TestAPI(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:chaveacesso@db-instance-prog-web.cuokvhdjyvdp.us-east-1.rds.amazonaws.com/Database_SISMIGRA'
        self.app = app.test_client()

        with app.app_context():  # Criando o contexto de aplicação
            db.create_all()

    def processar_csvs(self):
        directory_url = 'https://servicos.dpf.gov.br/dadosabertos/SISMIGRA/'

        response = requests.get(directory_url)
        html_content = response.content

        soup = BeautifulSoup(html_content, 'html.parser')

        file_links = []
        for link in soup.find_all('a'):
            file_url = link.get('href')
            if re.match(r'SISMIGRA_REGISTROS_ATIVOS_2022_\d{2}.csv', file_url):
                file_links.append(directory_url + file_url)

        for file_url in file_links:
            month = file_url[-6:-4]  # 01, 02, ..., 12
            response = requests.get(file_url)
            csv_content = response.content
            csv_text = csv_content.decode('utf-8').replace('\r', '').strip()
            rows = csv_text.split('\n')
            # Skip the header row
            count = 1
            for row in rows:
                dado = row.split(';')
                
                if dado == ['\ufeffUF', 'NACIONALIDADE', 'CLASSIFICACAO', 'QTD']:
                    continue
                if dado[1] == None:
                    dado[1] = "Não informado"
                print(dado , '/// contador:', count)
                if len(dado) >= 4:
                    registro = {
                        'uf': dado[0],
                        'pais': dado[1],
                        'classificacao': dado[2],
                        'qtd': int(dado[3]),
                        'mes': int(month),
                    }
                    # Executa a requisição local
                response = self.app.post('registros', json=registro)
                self.assertEqual(response.status_code, 200)
                count += 1

    def test_processar_csvs(self):
        self.processar_csvs()

if __name__ == '__main__':
    unittest.main()
