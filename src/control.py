from flask import render_template, request
from API import app
import requests
from models import *

@app.route('/')
def index():
    return render_template('index.html')

# q1
@app.route('/distribuicao_imigrantes_pais', methods=['POST'])
def func_distribuicao_imigrantes_pais():
    pais_filtro = request.form['pais_filtro_distribuicao_imigrantes_pais']
    data = {'pais': pais_filtro}
    response = requests.post('http://localhost:5000/api/distribuicao-de-imigrantes-pelo-pais', json=data)
    if response.status_code == 200:
        result = response.json()
        total_front = str(result['Total_Fronteirico'])
        total_prov = str(result['Total_Provisorio'])
        total_res = str(result['Total_Residente'])
        total_temp = str(result['Total_Temporario'])
        resultado = 'Total de imigrantes Fronteiriços: ' + total_front + '<br>'
        resultado += 'Total de imigrantes Provisórios: ' + total_prov + '<br><br>'
        resultado += 'Total de imigrantes Residentes: ' + total_res + '<br><br>'
        resultado += 'Total de imigrantes Temporários: ' + total_temp + '<br>'
        consulta = 'Distribuição de imigrantes: ' + pais_filtro
        return render_template('result.html', resultado=resultado, consulta_nome=consulta)


# #q2
# @app.route('/', methods=[''])
# # q3
# @app.route('/', methods=[''])
# # q4
# @app.route('/', methods=[''])
# # q5
# @app.route('/', methods=[''])
# # q6
# @app.route('/', methods=[''])




# q7
@app.route('/estado_mais_imigrantes', methods=['POST'])
def func_estado_mais_imigrantes():
    pais_filtro = request.form['pais_filtro_estado_mais_imigrantes']
    data = {'pais': pais_filtro}
    response = requests.post('http://localhost:5000/api/estado-com-mais-imigrantes', json=data)
    if response.status_code == 200:
        result = response.json()
        estado_nome = result['estado']
        qtd_estado = str(result['quantidade'])
        resultado = 'Estado: '+ estado_nome + ' QTD: ' + qtd_estado

        return render_template('result.html',resultado=resultado, consulta_nome='Estado com mais imigrantes de determinado País.')
    else:
        return 'Erro ao obter o estado com mais imigrantes'
    
# # q8
# @app.route('/', methods=[''])
# # q9
# @app.route('/', methods=[''])
# # q10
# @app.route('/', methods=[''])

if __name__ == '__main__':
    app.run()