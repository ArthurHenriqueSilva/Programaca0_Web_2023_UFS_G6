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

        return render_template('result.html',resultado=resultado, consulta_nome='País com mais imigração em determinado período.')
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
        tipo_nome = result['tipo']
        mes_inicial = result['mes_inicial']
        mes_final = result['mes_final']
        resultado = 'Tipo: '+ tipo_nome + ' a partir de ' + mes_inicial + ' até ' + mes_final + '.'

        return render_template('result.html',resultado=resultado, consulta_nome='Tipo de imigração mais popular em determinado período.')
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
        classificacao_nome = result['classificacao']
        periodo = result['periodo']
        resultado = 'O período de : '+ periodo + ' é o mais popular para o tipo de imigração: ' + classificacao_nome + '.'  

        return render_template('result.html',resultado=resultado, consulta_nome='Período mais popular de tipo de imigração.')
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
        if result['mes'] == '0':
            return render_template('result.html',resultado= 'Sem resultados', consulta_nome='Não existem dados para o filtro selecionado.')
        estado_nome = result['uf']
        mes = result['mes']
        classificacao_nome = result['classificacao']
        resultado = 'O mês de : '+ mes + ' é o mais popular para o estado: ' + estado_nome + ', atraindo mais imigrantes do tipo de classificação: ' + classificacao_nome + '.'

        return render_template('result.html',resultado=resultado, consulta_nome='Mês mais popular de imigração de uma classificação para o estado.')
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
        estado_nome = result['estado']
        mes_nome = result['mes']
        resultado = 'Estado: '+ estado_nome + '. O Mês: ' + mes_nome + ' é o mais popular para o estado para residentes.'

        return render_template('result.html',resultado=resultado, consulta_nome='Estado com mais residentes em determinado período.')
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
        estado_nome = result['estado']
        qtd_estado = str(result['quantidade'])
        resultado = 'Estado: '+ estado_nome + ' QTD: ' + qtd_estado

        return render_template('result.html',resultado=resultado, consulta_nome='Estado com mais imigrantes de determinado País.')
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
        pais = result['pais']
        tipo = result['tipo']
        resultado = 'Pais: ' + pais + '<br>' + ' Tipo de imigrante mais comum: ' + tipo
        return render_template('result.html', resultado=resultado, consulta_nome='Tipo mais comum de imigrante de determinado País.')
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
        pais = result['pais']
        mes = result['mes']
        qtd = result['quantidade']
        resultado = 'mes: ' + mes + '<br>' + 'pais: ' + pais + '<br>' + 'quantidade de imigrantes: ' + qtd
        return render_template('result.html', resultado=resultado, consulta_nome='Quantidade de imigrantes de determinado país no mês especificado.')
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
        pais = result['pais']
        mes = result['mes']
        classif = result['classificacao']
        resultado = 'mes: ' + mes + '<br>' + 'pais: ' + pais + '<br>' + 'classificação: ' + classif
        return render_template('result.html', resultado=resultado, consulta_nome='Quantidade de imigrantes de determinado país no mês especificado.')
    else:
        return 'Erro ao obter a classificação mais recorrente no mês especificado advindos do país escolhido.'

if __name__ == '__main__':
    app.run(host="0.0.0.0")
