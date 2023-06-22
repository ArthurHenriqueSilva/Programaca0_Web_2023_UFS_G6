from flask import render_template, request
from API import app
import requests
from models import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estado_mais_imigrantes', methods=['POST'])
def func_estado_mais_imigrantes():
    pais_filtro = request.form['pais_filtro_estado_mais_imigrantes']
    data = {'pais': pais_filtro}
    response = requests.post('http://localhost:5000/api/estado-com-mais-imigrantes', json=data)
    if response.status_code == 200:
        result = response.json()
        estado_nome = result['estado']
        qtd_estado = result['quantidade']
        return render_template('index.html', retorno_estado_mais_imigrantes=estado_nome, qtd_estado_mais_imigrantes=qtd_estado)
    else:
        return 'Erro ao obter o estado com mais imigrantes'
    


if __name__ == '__main__':
    app.run()