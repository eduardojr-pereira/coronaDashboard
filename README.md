<!-- Back to top link -->
<a name="readme-top"></a>

<!-- SHIELDS -->
<div align="center">
<img src="https://forthebadge.com/images/badges/made-with-python.svg" 
  alt="Made with Python" height="32">
<img src="https://forthebadge.com/images/badges/powered-by-coffee.svg" alt="Powered by Coffee" height="32">
</div>

<br />

<!-- PROJECT LOGO -->
<div align= "center">
  <img src="assets\imagens\logo_app.png" alt="Logo do App" height="100"> <h3>Evolução do coronavírus no Brasil</h3>
</div>

<hr>

<!-- CONTENT -->
<h4 align="center">Nessa Página:</h4>

<p align= "center">
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

- Fornecer dados atualizados e confiáveis.
- Permitir a visualização da evolução da pandemia em diferentes regiões do país.
- Oferecer ferramentas interativas para análise e visualização dos dados.
  - Facilitar a compreensão dos dados através de gráficos e tabelas interativas.
  - Auxiliar na identificação de tendências e padrões.
- Possibilitar a comparação entre diferentes estados em relação ao número de casos e óbitos.


<p align="right"><a href="#readme-top">• VOLTAR PARA O TOPO •</a></p>

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

*Fonte dos dados:* [Ministério da Saúde](https://www.gov.br/saude/pt-br/composicao/seidigi/demas/covid19 "Fonte dos dados")

<p align="right"><a href="#readme-top">• VOLTAR PARA O TOPO •</a></p>

<hr>

## Recursos e tecnologias utilizadas

### Ambientes de desenvolvimento Integrado (*IDE*) utilizados:

- Jupyter Notebooks - *prototipagem do código*
- Visual Studio Code

### Linguagens de programação:

- HTML e CSS
- Python 

### Frameworks Python utilizados no projeto:

<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.9-informational"></a>
<a href="https://plotly.com/"><img src="https://img.shields.io/badge/Plotly-5.9.0-critical"></a>
<a href="https://plotly.com/dash/"><img src="https://img.shields.io/badge/Dash-2.10.2-critical"></a>
<a href="https://dash-bootstrap-components.opensource.faculty.ai/"><img src="https://img.shields.io/badge/Dash_Bootstrap_Components-1.4.1-critical"></a>
<a href="https://pandas.pydata.org/"><img src="https://img.shields.io/badge/Pandas-1.5.3-critical"></a>


<p align="right"><a href="#readme-top">• VOLTAR PARA O TOPO •</a></p>

<hr>

## Estrutura de arquivos e pastas

```bash
coronaDashboard/
│
├── 📄 .gitattributes
├── 📄 .gitignore
├── 📄 app.py 
├── 📄 README.md
├── 📄 requirements.txt
│   
├── 📂 assets/
│   ├── 📂 imagens/
│   │   ├── 📄 discord_icon.svg    
│   │   ├── 📄 favicon.ico
│   │   ├── 📄 github_icon.svg    
│   │   ├── 📄 gmail_icon.svg    
│   │   ├── 📄 linkedin_icon.svg    
│   │   ├── 📄 logo_app.png    
│   │   └── 📄 logo_initials.png    
│   ├── 📄 custom_animation.css
│   ├── 📄 custom_datepicker.css
│   ├── 📄 custom_dropdown.css
│   ├── 📄 custon_icon.css
│   ├── 📄 custon_tabs.css
│   └── 📄 CV_EduardoPereira.pdf
│
├── 📂 data/
│   ├── 📂 processed/
│   │   ├── 📄 covid_br_dataset.csv    
│   │   ├── 📄 covid_estados_dataset.csv
│   │   └── 📄 indices_dataset.csv
│   └── 📂 raw/
│       ├── 📄 brasilGeo.json    
│       ├── 📄 HIST_PAINEL_COVIDBR.zip
│       └── 📄 indicesSocioeconomicos.zip
│
├── 📂 notebooks/
│   └── 📄 data_clean.ipynb
│
├── 📂 templates/
│   ├── 📄 content_component.py
│   ├── 📄 footer_component.py
│   └── 📄 navbar_component.py
│
└── 📂 tests/
    └── 📄 test_app.py
```

<p align="right"><a href="#readme-top">• VOLTAR PARA O TOPO •</a></p>

<hr>

## Uso

### 1. Clonar o Repositório
- Clonar este repositório para o seu ambiente local:

```bash
git clone https://github.com/eduardojr-pereira/coronaDashboard.git
```

### 2. Configurar o ambiente

- Acesse o diretório do projeto e crie um ambiente virtual

```bash
cd seu-repositorio
python -m -venv venv
```

- Ative o ambiente virtual
> No Windows:
```bash
venv\Scripts\activate
```
> No macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Instalar as dependências necessárias

- Instale as bibliotecas necessárias usando o gerenciador de pacotes do Python [pip](https://pip.pypa.io/en/stable/).

```bash
pip install -U -r requirements.txt
```

> Essa atualização garante que todas as dependências necessárias sejam instaladas corretamente a partir do arquivo requirements.txt.

### 4. Execução:

- Navegar para o diretório no prompt de comando e executar o algoritmo com o código abaixo:

```bash
python nome_do_arquivo.py
```

> Substitua ***nome_do_arquivo.py*** pelo nome do arquivo Python que contém o código do seu algoritmo.

<p align="right"><a href="#readme-top">• VOLTAR PARA O TOPO •</a></p>

<hr>

## Contribuição

Contribuições serão bem-vindas via ***pull requests***. Tenha certeza que os testes foram feitos.

<p align="right"><a href="#readme-top">• VOLTAR PARA O TOPO •</a></p>

<hr>

## Possíveis implementações futuras

- [ ] Web Scraping para realizar a atualização automática dos dados.
- [ ] Configurar o set.locale no plotly.js e traduzir as datas para pt-br.
- [ ] Utilizar _Clustering Models_ para identificar padrões intrínsecos nos dados.

<p align="right"><a href="#readme-top">• VOLTAR PARA O TOPO •</a></p>

<hr>

## Licença

Utilize o link abaixo para obter mais inforações sobre a licença:

[ainda nao definida - ***atenção escolher licença***]()

<p align="right"><a href="#readme-top">• VOLTAR PARA O TOPO •</a></p>

<hr>

## Contato

Se você tiver alguma dúvida, sugestão ou feedback, por favor, não hesite em entrar em contato utilizando o email abaixo. Estou à disposição para ajudar e receber seus comentários.

```
eduardojr.pereira@gmail.com
```

- [Linkedin](https://www.linkedin.com/in/eduardo-jr-pereira/ "Visitar perfil no Linkedin")

  > Confira também meu [Portfólio](https://eduardo-pereira.webflow.io/) para ver outros projetos e obter mais informações sobre meu trabalho.

<div align="center">
  
  <a href="https://eduardo-pereira.webflow.io/"><img src="assets\imagens\logo_initials.png" alt="Logo com iniciais EP" height="100"></a>
  
  <a href="mailto:eduardojr.pereira@gmail.com"><img src="assets\imagens\gmail_icon.svg" alt="gmail" height="25"></a>
  <a href="https://www.linkedin.com/in/eduardo-jr-pereira/"><img src="assets\imagens\linkedin_icon.svg" alt="linkedin" height="25"></a>
  <a href="https://github.com/eduardojr-pereira"><img src="assets\imagens\github_icon.svg" alt="github" height="25"></a>
  <a href="https://discord.com/channels/1095050260964966483/1111074732503203900"><img src="assets\imagens\discord_icon.svg" alt="discord" height="25"></a></p>
</div>

<p align="right"><a href="#readme-top">• VOLTAR PARA O TOPO •</a></p>

<hr>


