<p style="text-align: center; font-size: 15px; font-weight: bold;">
  <img src="assets\imagens\logo_app.png" alt="Logo do App" height="100">
  <br>
  Evolução do coronavírus no Brasil
</p>
<p style="display: flex; justify-content: center; gap: 50px;">
  <img src="https://forthebadge.com/images/badges/made-with-python.svg" alt="Made with Python" height="32">
  <img src="https://forthebadge.com/images/badges/powered-by-coffee.svg" alt="Powered by Coffee" height="32">
</p>
<hr>
<p style="display: flex; justify-content: space-around;">
  <a href="#visão-geral">Visão Geral</a> •
  <a href="#objetivos">Objetivos</a> •
  <a href="#conjunto-de-dados">Dados</a> •
  <a href="#recursos-e-tecnologias-utilizadas">Frameworks</a> •
  <a href="#estrutura-de-diretórios">Estrutura</a> •
  <a href="#uso">Uso</a> •
  <a href="#contribuição">Contribuição</a> •
  <a href="#licença">Licença</a> •
  <a href="#contato">Contato</a>
</p>
<hr>

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
### Ambientes de desenvolvimento Integrado (*IDE*) utilizados:
- Jupyter Notebooks - *prototipagem do código*
- Visual Studio Code
### Linguagens de programação:
- HTML e CSS
- Python 
### Frameworks Python utilizados no projeto:
![Python](https://img.shields.io/badge/Python-3.9-informational)
!["Numpy"](https://img.shields.io/badge/NumPy-1.20.3-critical)
![Pandas](https://img.shields.io/badge/Pandas-1.3.0-critical)
![Dash](https://img.shields.io/badge/Dash-2.10.2-critical)
![Dash Bootstrap Components](https://img.shields.io/badge/Dash_Bootstrap_Components-1.4.1-critical)
![Plotly](https://img.shields.io/badge/Plotly-5.11.0-critical)
![Flask](https://img.shields.io/badge/Flask-2.1.0-critical)
<hr>

## Estrutura de diretórios
```bash
coronaDashboard/
│
├── app.py 
├── README.md
├── requirements.txt
├── .gitignore
├── .gitattributes
│   
├── assets/
│   ├── imagens/
│   │   ├── discord_icon.svg    
│   │   ├── favicon.ico
│   │   ├── github_icon.svg    
│   │   ├── gmail_icon.svg    
│   │   ├── linkedin_icon.svg    
│   │   ├── logo_app.png    
│   │   └── logo_initials.png    
│   ├── custom_datepicker.css
│   ├── custom_dropdown.css
│   ├── custon_icon.css
│   └── CV_EduardoPereira.pdf
│
├── data/
│   ├── processed/
│   │   ├── covid_br_dataset.csv    
│   │   └── covid_estados_dataset.csv
│   └── raw/
│       ├── brasilGeo.json    
│       ├── HIST_PAINEL_COVIDBR_02jun2023.zip    
│       ├── HIST_PAINEL_COVIDBR_2020_Parte1_02jun2023.csv
│       ├── HIST_PAINEL_COVIDBR_2020_Parte2_02jun2023.csv
│       ├── HIST_PAINEL_COVIDBR_2021_Parte1_02jun2023.csv
│       ├── HIST_PAINEL_COVIDBR_2021_Parte2_02jun2023.csv
│       ├── HIST_PAINEL_COVIDBR_2022_Parte1_02jun2023.csv
│       ├── HIST_PAINEL_COVIDBR_2022_Parte2_02jun2023.csv
│       └── HIST_PAINEL_COVIDBR_2023_Parte1_02jun2023.csv
│
├── notebooks/
│   └── data_generation.ipynb
│
├── templates/
│   ├── navbar.py
│   └── footer_component.py
│
└── tests/
    └── test_app.py
```

<hr>

## Uso
### Instalação:
- Utilize o gerenciador de pacotes [pip](https://pip.pypa.io/en/stable/) para instalar a aplicação.
```bash
pip install -U -r requirements.txt
```

### Execução:
- Navegar para o diretório no prompt de comando:
```bash
cd\coronaDashboard\app
```

- Definir a variável de ambiente FLASK_APP com o valor "app.py". 

```bash
set FLASK_APP=app.py
```
> Essa variável é usada pelo Flask para identificar o arquivo principal da aplicação Flask.

- Iniciar o servidor de desenvolvimento do Flask e executar a aplicação:
```bash
flask run
```
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

Confira também meu [Portfólio](https://eduardo-pereira.webflow.io/) para ver outros projetos e obter mais informações sobre meu trabalho.
<p style="display: flex; justify-content: center; gap: 30px;">
  <a href="https://eduardo-pereira.webflow.io/"><img src="assets\imagens\logo_initials.png" alt="Logo com iniciais EP" height="100"></a></p>
<p style="display: flex; justify-content: center; gap: 30px;">
  <a href="mailto:eduardojr.pereira@gmail.com"><img src="assets\imagens\gmail_icon.svg" alt="gmail" height="30"></a>
  <a href="https://www.linkedin.com/in/eduardo-jr-pereira/"><img src="assets\imagens\linkedin_icon.svg" alt="linkedin" height="30"></a>
  <a href="https://github.com/eduardojr-pereira"><img src="assets\imagens\github_icon.svg" alt="github" height="30"></a>
  <a href="https://discord.com/channels/1095050260964966483/1111074732503203900"><img src="assets\imagens\discord_icon.svg" alt="discord" height="30"></a></p>
<hr>
<p style="display: flex; justify-content: center; gap: 10px">
  •<a href="#visão-geral">Voltar para o incício</a>•
  
</p>
<hr>

