
<div style="align-items:center;">
  <img src="assets/static/corona-dash-logo.png" alt="Logo do App" height="100" style="margin-bottom: 20px;">
</div>

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)](https://forthebadge.com)

## Visão Geral
É de conhecimento geral que a pandemia do coronavírus tem impactado significativamente o Brasil e o mundo. Assim, acompanhar a evolução dos casos, das taxas de transmissão e dos esforços de controle é de extrema importância.

Além disso, a disseminação de informações confiáveis é essencial para combater a desinformação e contribuir para uma compreensão clara da situação atual da pandemia no Brasil.

Nesse sentido, o aplicativo **coronaDash Brasil** visa suprir essa necessidade, fornecendo uma plataforma confiável e acessível para a visualização e análise dos dados relacionados ao COVID-19.
            
Através de ferramentas interativas como gráficos, mapas e análises de dados, o aplicativo permite aos usuários acompanhar de perto e compreender a situação da pandemia em nosso país. A plataforma também oferece a possibilidade de filtrar e selecionar informações específicas, proporcionando uma visão clara e detalhada da evolução da pandemia do coronavírus no Brasil.
<hr>

## Objetivos
Este projeto tem como objetivo principal fornecer informações atualizadas e relevantes sobre a evolução da pandemia no Brasil, de maneira confiável e acessível, para que todos possam se manter informados e tomar decisões bem embasadas diante dessa crise de saúde.

**Objetivos Específicos:**
- Utilizar ferramentas de Ciências de Dados para **fornecer dados atualizados e confiáveis** sobre o COVID-19 no Brasil;
- Permitir a **visualização da evolução da pandemia em diferentes regiões** do país;
- **Oferecer ferramentas interativas** para análise e visualização dos dados, auxiliando na identificação de tendências e padrões;
- **Facilitar a compreensão dos dados** através de gráficos e tabelas interativas;
- **Possibilitar a comparação entre diferentes estados** em relação ao número de casos e óbitos.
<hr>

## Conjunto de Dados
O conjunto de dados utilizado nesse projeto é disponibilizado diariamente pelo Ministério da Saúde através do [Portal Brasileiro de Dados Abertos](https://dados.gov.br/home "Fonte: dataSUS") e as informações contidas no dataset incluem dados sobre casos e óbitos por COVID-19 no Brasil, agregados por estado, município e data.

O dataset fornece informações valiosas para acompanhar a evolução do COVID-19 no Brasil, permitindo análises e visualizações para entender a propagação da doença. Além disso, apresenta um total de 17 colunas que podem ser visualizadas abaixo:

||Variável|Tipo|Descrição|
|:---|:---|:---|:---|
|1|regiao|object|Macroregião do Brasil|
|2|estado|object|Sigla do estado onde aconteceu o registro|
|3|municipio|object|Nome do município onde aconteceu o registro|
|4|coduf|int64|Código númerico que identifica as Unidades Federativas do Brasil|
|5|codmun|float64|Código numérico que identifica os municípios das Unidades Federativas do Brasil|
|6|codRegiaoSaude|float64|Código numérico que identifica as regiões de saúde do Brasil|
|7|nomeRegiaoSaude|object|Nome das regiões de saúde do Brasil|
|8|data|object|Data correspondente aos registros|
|9|semanaEpi|int64|Número da semana epidemiológica|
|10|populacaoTCU2019|float64|População estimada em 2019 para cada região|
|11|casosAcumulado|float64|Número acumulado de casos de COVID-19 até a data|
|12|casosNovos|int64|Número de novos casos de COVID-19 registrados na data|
|13|obitosAcumulado|int64|Número acumulado de óbitos por COVID-19 até a data|
|14|obitosNovos|int64|Número de novos óbitos por COVID-19 registrados na data|
|15|Recuperadosnovos|float64|Número de novos casos que se recuperaram da doença na data|
|16|emAcompanhamentoNovos|float64|Número de casos que estão em acompanhamento na data|
|17|interior/metropolitana|float64|Código binário que indica se uma determinada região é classificada como metropolitana (valor 1) ou interior (valor 0)|

*Fonte dos dados:* [Portal Brasileiro de Dados Abertos](https://dados.gov.br/home "Fonte: dataSUS")
<hr>

## Recursos e tecnologias utilizadas
### Ambiente de desenvolvimento Integrado:
- Jupyter Notebooks - *prototipagem do código*
- Visual Studio Code
### Linguagens de programação:
- HTML e CSS
- Python 
### Frameworks Python utilizados no projeto:
![Python](https://img.shields.io/badge/Python-3.9-informational)
!["Numpy"](https://img.shields.io/badge/NumPy-1.20.3-critical)
![Pandas](https://img.shields.io/badge/Pandas-1.3.0-critical)
![Dash](https://img.shields.io/badge/Dash-1.21.0-critical)
![Dash Bootstrap Components](https://img.shields.io/badge/Dash_Bootstrap_Components-1.0.0-critical)
![Plotly](https://img.shields.io/badge/Plotly-5.11.0-critical)
![Flask](https://img.shields.io/badge/Flask-2.1.0-critical)
<hr>

## Uso
### Instalação:
- Utilize o gerenciador de pacotes [pip](https://pip.pypa.io/en/stable/) para instalar a aplicação.

`pip install -U -r requirements.txt`

### Execução:
- Navegar para o diretório no prompt de comando:

`cd\coronaDashboard\app`

- Definir a variável de ambiente FLASK_APP com o valor "app.py". 

`set FLASK_APP=app.py`
> Essa variável é usada pelo Flask para identificar o arquivo principal da aplicação Flask.

- Iniciar o servidor de desenvolvimento do Flask e executar a aplicação:

`flask run`
> Verifica a variável FLASK_APP definida anteriormente e inicia a execução da aplicação.
<hr>

## Contribuição
Contribuições serão bem-vindas via ***pull requests***. Tenha certeza que os testes foram feitos.
<hr>

## Licença
Utilize o link abaixo para obter mais inforações sobre a licença:

[escolher licença]()
<hr>

## Contato
Se você tiver alguma dúvida, sugestão ou feedback, sinta-se à vontade para entrar em contato utilizando os canais disponíveis.

- Email: [eduardojr.pereira@gmail.com](mailto:eduardojr.pereira@gmail.com "Enviar email")
- [Linkedin](https://www.linkedin.com/in/eduardo-jr-pereira/ "Visitar perfil no Linkedin")

Confira meu [Portfólio de Data Science](https://eduardo-pereira.webflow.io/) para ver outros projetos e obter mais informações sobre meu trabalho.

