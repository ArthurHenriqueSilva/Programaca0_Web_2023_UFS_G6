import React from 'react';

const AppSummary = () => {
  return (
    <section className="appSummary">
      <h2>Resumo do Aplicativo</h2>
      <p>
        Este aplicativo permite que você tenha{' '}
        <strong>
          <u>
            acesso aos números de 2022 referentes aos dados de imigração da
            Polícia Federal
          </u>
        </strong>{' '}
        .
      </p>
      <p>
        Você pode buscar informações filtradas e visualizar dados relevantes
        relacionados aos números de imigração.
      </p>
      <p>
        Utilize as opções de pesquisa para encontrar informações específicas e
        utilize os recursos interativos para explorar os dados em detalhes.
      </p>
    </section>
  );
};

export default AppSummary;
