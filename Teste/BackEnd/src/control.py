from flask import render_template, request
from API import app
import requests
from models import *
from flask_cors import CORS

CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

# q1
@app.route('/distribuicao_imigrantes_pais', methods=['POST'])
def func_distribuicao_imigrantes_pais():
    print(request.form)
    pais_filtro = request.form['pais_filtro_distribuicao_imigrantes_pais']
    data = {'pais': pais_filtro}
    response = requests.post('http://localhost:5000/api/distribuicao-de-imigrantes-pelo-pais', data=data)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return 'Erro ao obter a distribuição de imigrantes do país escolhido.'


# #q2
@app.route('/pais_mais_imigracao_periodo', methods=['POST'])
def func_pais_mais_imigracao_periodo():
    mes_inicial = request.form['mes_inicio_pais_mais_imigracao_periodo']
    mes_final = request.form['mes_fim_pais_mais_imigracao_periodo']
    data = {'mes_inicial': mes_inicial, 'mes_final': mes_final}
    response = requests.post('http://localhost:5000/api/pais-com-mais-imigracao-no-periodo', json=data)
    if response.status_code == 200:
        result = response.json()
        pais_nome = result['pais']
        qtd_pais = str(result['qtd_pais'])
        resultado = 'País: '+ pais_nome + ' QTD: ' + qtd_pais

        return result
    else:
        return 'Erro ao obter o país com mais imigração em determinado período'
# # q3
@app.route('/tipo_imigracao_mais_popular_periodo', methods=['POST'])
def func_tipo_imigracao_periodo():
    mes_inicial = request.form['mes_inicio_tipo_imigracao_mais_popular_periodo']
    mes_final = request.form['mes_fim_tipo_imigracao_mais_popular_periodo']
    data = {'mes_inicial': mes_inicial, 'mes_final': mes_final}
    response = requests.post('http://localhost:5000/api/tipo-de-imigracao-mais-popular-no-periodo', json=data)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return 'Erro ao obter o tipo de imigração mais popular em determinado período'  
# # q4
@app.route('/periodo_popular_tipo', methods=['POST'])
def func_periodo_popular_tipo():
    tipo_filtro = request.form['tipo_filtro_periodo_popular']
    data = {'classificacao': tipo_filtro}
    response = requests.post('http://localhost:5000/api/periodo-mais-popular-para-o-tipo', json=data)
    if response.status_code == 200:
        result = response.json()

        return result
    else:
        return 'Erro ao obter o período mais popular de tipo de imigração'  
# # q5
@app.route('/mes_popular_estado', methods=['POST'])
def func_mes_popular_estado():
    estado_filtro = request.form['estado_filtro_mes_popular_estado']
    classificacao_filtro = request.form['classificacao_filtro_mes_popular_estado']
    data = {'uf': estado_filtro, 'classificacao': classificacao_filtro}
    response = requests.post('http://localhost:5000/api/mes-que-chama-mais-atencao-para-o-imigrante-em-um-estado', json=data)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return 'Erro ao obter o mês mais popular de imigração para o estado'    
# # q6
@app.route('/estado_mais_residente_no_mes', methods=['POST'])
def func_estado_mais_residente_no_mes():
    mes = request.form['mes_estado_mais_residente_por_periodo']
    data = {'mes': mes}
    response = requests.post('http://localhost:5000/api/estado-com-mais-residentes-no-mes', json=data)
    if response.status_code == 200:
        result = response.json()

        return result
    else:
        return 'Erro ao obter o estado com mais residentes em determinado período'




# q7
@app.route('/estado_mais_imigrantes', methods=['POST'])
def func_estado_mais_imigrantes():
    pais_filtro = request.form['pais_filtro_estado_mais_imigrantes']
    data = {'pais': pais_filtro}
    response = requests.post('http://localhost:5000/api/estado-com-mais-imigrantes', json=data)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return 'Erro ao obter o estado com mais imigrantes'
    
# # q8
@app.route('/tipo_imigrante_pais', methods=['POST'])
def func_tipo_imigrante_pais():
    pais_filtro = request.form['pais_filtro_tipo_imigrante_pais']
    data = {'pais':pais_filtro}
    response = requests.post('http://localhost:5000/api/maior-tipo-imigrante-do-pais',json=data)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return 'Erro ao obter o tipo mais comum de imigrantes do país escolhido.'
# # q9
@app.route('/quantidade_pais_maior_periodo_imigracao', methods=['POST'])
def func_pais_imigracao_periodo_popular():
    pais_filtro = request.form['pais_filtro_pais_imigracao_periodo_popular']
    mes_filtro = request.form['mes_filtro_pais_imigracao_periodo_popular']
    data = {'pais':pais_filtro, 'mes':mes_filtro}
    response = requests.post('http://localhost:5000/api/quantidade-do-pais-no-periodo-de-maior-imigracao', json=data)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return 'Erro ao obter a quantidade de imigrantes do país escolhido no período informado'
# # q10
@app.route('/classificacao_imigracao_mais_popular_mes', methods=['POST'])
def func_classificacao_pais_tempo():
    pais_filtro = request.form['pais_filtro_classificacao_imigracao_mais_popular_mes']
    mes_filtro = request.form['mes_filtro_classificacao_pais_tempo']
    data = {'pais':pais_filtro, 'mes':mes_filtro}
    response = requests.post('http://localhost:5000/api/classificacao-de-imigrante-mais-popular-em-um-mes', json=data)
    if response.status_code == 200:
        result = response.json()

        return result
    else:
        return 'Erro ao obter a classificação mais recorrente no mês especificado advindos do país escolhido.'

if __name__ == '__main__':
    app.run()
