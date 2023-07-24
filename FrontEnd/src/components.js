import React, { useState } from 'react';

import './style.css';

const Frame1 = () => {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();

    const formData = new URLSearchParams();
    formData.append(
      'pais_filtro_distribuicao_imigrantes_pais',
      event.target.pais_filtro_distribuicao_imigrantes_pais.value
    );

    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    };

    setLoading(true);
    fetch('http://localhost:5000/distribuicao_imigrantes_pais', requestOptions)
      .then((res) => {
        if (!res.ok) {
          throw new Error('Erro na solicitação');
        }
        return res.json();
      })
      .then((data) => {
        // Formatando os dados para retirar o prefixo "Total_"
        const formattedData = {};
        for (const [key, value] of Object.entries(data)) {
          if (key !== 'pais') {
            const formattedKey = key.replace('Total_', '');
            formattedData[formattedKey] = value;
          }
        }
        setData(formattedData);
        setError('');
        setLoading(false);
        console.log('Dados recebidos da API para Q1', data);
      })
      .catch((error) => {
        console.error(error);
        setData({});
        setError(
          'Erro ao obter a distribuição de imigrantes do país escolhido.'
        );
        setLoading(false);
      });
  };

  // Manipulador de evento para o botão de "Reset"
  const handleReset = () => {
    setData({});
    setError('');
  };

  return (
    <div>
      <h2>Quantização de imigrantes vindos de</h2>
      {!data.pais ? (
        <form onSubmit={handleSubmit}>
          <label htmlFor="pais_filtro_distribuicao_imigrantes_pais">
            País para filtragem:
          </label>
          <input type="text" name="pais_filtro_distribuicao_imigrantes_pais" />

          {/* Renderização condicional do botão */}
          {!loading && (
            <button className="submit_button" type="submit">
              Enviar
            </button>
          )}
        </form>
      ) : null}
      <div className="result">
        {loading && <p>Carregando...</p>}
        {error && <p>{error}</p>}
        {data && data.pais && (
          <div>
            <p>Resultado para {data.pais}:</p>
            <table>
              <thead>
                <tr>
                  <th>Classificação</th>
                  <th>Total</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(data).map(([classificacao, total]) => (
                  <tr key={classificacao}>
                    <td>{classificacao}</td>
                    <td>{total}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            {/* Botão de reset */}
            <button className="reset_button" onClick={handleReset}>
              Reset
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

const Frame2 = () => {
  return (
    <div>
      <h1>País com mais imigração entre os meses de</h1>
      <form action="/pais_mais_imigracao_periodo" method="post">
        <label htmlFor="mes_inicio_pais_mais_imigracao_periodo">
          Mês inicial para filtragem
        </label>
        <select name="mes_inicio_pais_mais_imigracao_periodo">
          <option value="1">Janeiro</option>
          <option value="2">Fevereiro</option>
          <option value="3">Março</option>
          <option value="4">Abril</option>
          <option value="5">Maio</option>
          <option value="6">Junho</option>
          <option value="7">Julho</option>
          <option value="8">Agosto</option>
          <option value="9">Setembro</option>
          <option value="10">Outubro</option>
          <option value="11">Novembro</option>
          <option value="12">Dezembro</option>
        </select>

        <label htmlFor="mes_fim_pais_mais_imigracao_periodo">
          Mês final para filtragem
        </label>
        <select name="mes_fim_pais_mais_imigracao_periodo">
          <option value="1">Janeiro</option>
          <option value="2">Fevereiro</option>
          <option value="3">Março</option>
          <option value="4">Abril</option>
          <option value="5">Maio</option>
          <option value="6">Junho</option>
          <option value="7">Julho</option>
          <option value="8">Agosto</option>
          <option value="9">Setembro</option>
          <option value="10">Outubro</option>
          <option value="11">Novembro</option>
          <option value="12">Dezembro</option>
        </select>

        <button className="submit_button" type="submit">
          Enviar
        </button>
      </form>
    </div>
  );
};

const Frame3 = () => {
  return (
    <div>
      <h1>Tipo principal de imigrante entre os meses de</h1>
      <form action="/tipo_imigracao_mais_popular_periodo" method="post">
        <label htmlFor="mes_inicio_tipo_imigracao_mais_popular_periodo">
          Mês inicial para filtragem
        </label>
        <select name="mes_inicio_tipo_imigracao_mais_popular_periodo">
          <option value="1">Janeiro</option>
          <option value="2">Fevereiro</option>
          <option value="3">Março</option>
          <option value="4">Abril</option>
          <option value="5">Maio</option>
          <option value="6">Junho</option>
          <option value="7">Julho</option>
          <option value="8">Agosto</option>
          <option value="9">Setembro</option>
          <option value="10">Outubro</option>
          <option value="11">Novembro</option>
          <option value="12">Dezembro</option>
        </select>

        <label htmlFor="mes_fim_tipo_imigracao_mais_popular_periodo">
          Mês final para filtragem
        </label>
        <select name="mes_fim_tipo_imigracao_mais_popular_periodo">
          <option value="1">Janeiro</option>
          <option value="2">Fevereiro</option>
          <option value="3">Março</option>
          <option value="4">Abril</option>
          <option value="5">Maio</option>
          <option value="6">Junho</option>
          <option value="7">Julho</option>
          <option value="8">Agosto</option>
          <option value="9">Setembro</option>
          <option value="10">Outubro</option>
          <option value="11">Novembro</option>
          <option value="12">Dezembro</option>
        </select>

        <button className="submit_button" type="submit">
          Enviar
        </button>
      </form>
    </div>
  );
};

const Frame4 = () => {
  return (
    <div>
      <h1>Mês com maior quantidade de registros de imigrantes do tipo</h1>
      <form action="/periodo_popular_tipo" method="post">
        <label htmlFor="tipo_filtro_periodo_popular">
          Tipo para filtragem:{' '}
        </label>
        <select name="tipo_filtro_periodo_popular">
          <option value="Fronteiriço">Fronteiriço</option>
          <option value="Provisório">Provisório</option>
          <option value="Residente">Residente</option>
          <option value="Temporário">Temporário</option>
        </select>

        <button className="submit_button" type="submit">
          Enviar
        </button>
      </form>
    </div>
  );
};

const Frame5 = () => {
  return (
    <div>
      <h1>Mês no qual esse Estado recebeu mais imigrantes do tipo</h1>
      <form action="/mes_popular_estado" method="post">
        <label htmlFor="estado_filtro_mes_popular_estado">
          Estado para filtragem:{' '}
        </label>
        <input type="text" name="estado_filtro_mes_popular_estado" />

        <label htmlFor="classificacao_filtro_mes_popular_estado">
          Tipo para filtragem:{' '}
        </label>
        <select name="classificacao_filtro_mes_popular_estado">
          <option value="Fronteiriço">Fronteiriço</option>
          <option value="Provisório">Provisório</option>
          <option value="Residente">Residente</option>
          <option value="Temporário">Temporário</option>
        </select>

        <button className="submit_button" type="submit">
          Enviar
        </button>
      </form>
    </div>
  );
};

const Frame6 = () => {
  return (
    <div>
      <h1>Estado com mais registros de imigrantes residentes no mês de</h1>
      <form action="/estado_mais_residente_no_mes" method="post">
        <label htmlFor="mes_estado_mais_residente_por_periodo">
          Mês para filtragem
        </label>
        <select name="mes_estado_mais_residente_por_periodo">
          <option value="1">Janeiro</option>
          <option value="2">Fevereiro</option>
          <option value="3">Março</option>
          <option value="4">Abril</option>
          <option value="5">Maio</option>
          <option value="6">Junho</option>
          <option value="7">Julho</option>
          <option value="8">Agosto</option>
          <option value="9">Setembro</option>
          <option value="10">Outubro</option>
          <option value="11">Novembro</option>
          <option value="12">Dezembro</option>
        </select>

        <button className="submit_button" type="submit">
          Enviar
        </button>
      </form>
    </div>
  );
};

const Frame7 = () => {
  return (
    <div>
      <h1>Estado com mais imigrantes vindos de</h1>
      <form action="/estado_mais_imigrantes" method="post">
        <label htmlFor="pais_filtro_estado_mais_imigrantes">
          Pais para filtragem:{' '}
        </label>
        <input type="text" name="pais_filtro_estado_mais_imigrantes" />

        <button className="submit_button" type="submit">
          Enviar
        </button>
      </form>
    </div>
  );
};

const Frame8 = () => {
  return (
    <div>
      <h1>Tipo de imigrante mais comum vindo de</h1>
      <form action="/tipo_imigrante_pais" method="post">
        <label htmlFor="pais_filtro_tipo_imigrante_pais">
          Pais para filtragem:{' '}
        </label>
        <input type="text" name="pais_filtro_tipo_imigrante_pais" />

        <button className="submit_button" type="submit">
          Enviar
        </button>
      </form>
    </div>
  );
};

const Frame9 = () => {
  return (
    <div>
      <h1>Quantidade de imigrantes desse país no mês de</h1>
      <form action="/quantidade_pais_maior_periodo_imigracao" method="post">
        <label htmlFor="pais_filtro_pais_imigracao_periodo_popular">
          Pais para filtragem:{' '}
        </label>
        <input type="text" name="pais_filtro_pais_imigracao_periodo_popular" />{' '}
        <br />
        <label htmlFor="mes_filtro_pais_imigracao_periodo_popular">
          Mês para filtragem
        </label>
        <select name="mes_filtro_pais_imigracao_periodo_popular">
          <option value="1">Janeiro</option>
          <option value="2">Fevereiro</option>
          <option value="3">Março</option>
          <option value="4">Abril</option>
          <option value="5">Maio</option>
          <option value="6">Junho</option>
          <option value="7">Julho</option>
          <option value="8">Agosto</option>
          <option value="9">Setembro</option>
          <option value="10">Outubro</option>
          <option value="11">Novembro</option>
          <option value="12">Dezembro</option>
        </select>
        <button className="submit_button" type="submit">
          Enviar
        </button>
      </form>
    </div>
  );
};

const Frame10 = () => {
  return (
    <div>
      <h1>Tipo mais recorrente de imigrante desse país no mês de</h1>
      <form action="/classificacao_imigracao_mais_popular_mes" method="post">
        <label htmlFor="pais_filtro_classificacao_imigracao_mais_popular_mes">
          Pais para filtragem:{' '}
        </label>
        <input
          type="text"
          name="pais_filtro_classificacao_imigracao_mais_popular_mes"
        />{' '}
        <br />
        <label htmlFor="mes_filtro_classificacao_pais_tempo">
          Mês para filtragem
        </label>
        <select name="mes_filtro_classificacao_pais_tempo">
          <option value="1">Janeiro</option>
          <option value="2">Fevereiro</option>
          <option value="3">Março</option>
          <option value="4">Abril</option>
          <option value="5">Maio</option>
          <option value="6">Junho</option>
          <option value="7">Julho</option>
          <option value="8">Agosto</option>
          <option value="9">Setembro</option>
          <option value="10">Outubro</option>
          <option value="11">Novembro</option>
          <option value="12">Dezembro</option>
        </select>
        <button className="submit_button" type="submit">
          Enviar
        </button>
      </form>
    </div>
  );
};

const frames = {
  Frame1,
  Frame2,
  Frame3,
  Frame4,
  Frame5,
  Frame6,
  Frame7,
  Frame8,
  Frame9,
  Frame10,
};

export default frames;
