from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

# Carregar os dados
estados_df = pd.read_csv("data/processed/covid_estados_dataset.csv", usecols=["data", "estado"])
first_date = estados_df["data"].min()
last_date = estados_df["data"].max()

# Determinar padrões para o spinner
spinner_color = "BurlyWood"
spinner_type = "dot"

<<<<<<< HEAD
# Determinar padrão para a modebar nos gráficos (Apenas Botão de Download)
modebar_config={
    "modeBarButtonsToRemove": [
        "sendDataToCloud",
        "zoom2d",
        "pan2d",
        "select2d",
        "lasso2d",
        "zoomIn2d",
        "zoomOut2d",
        "resetScale2d",
        "hoverClosestCartesian",
        "hoverCompareCartesian",
        "toggleSpikelines",
        "autoScale2d"
    ]
}


=======
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
class Header:
    def __init__(self, title, *subtitle):
        self.title = title
        self.subtitle = subtitle
        self.element = html.Div(
            [
                html.H1(self.title),
                html.H3(self.subtitle)
            ],
            className="text-center text-light"
        )


class TopContent:
    def __init__(self):
        self.element = dbc.Card(
            [
                dbc.CardHeader(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.P("Selecione uma data", className="d-flex justify-content-end text-light m-0")),
                                dbc.Col(
                                    [
                                        dcc.DatePickerSingle(
                                            id="datepicker",
                                            min_date_allowed = first_date,
                                            max_date_allowed=last_date,
                                            initial_visible_month=last_date,
                                            date=last_date,
                                            display_format="DD/MM/YYYY"   
                                        ),
                                        dcc.Store(id="store-states-on-date")
                                    ]
                                )
                            ],
                            className="d-flex align-items-center m-0"
                        )
                    ]
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H5("Casos Acumulados"),
<<<<<<< HEAD
                                        html.H2(id="casos-acumulados-na-data", style={"color":"#E6C1A6"}),
=======
                                        html.H2(id="casos-acumulados-na-data", style={"color":"#F7A177"}),
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
                                        html.H6(id="novos-casos-texto")
                                    ],
                                    md=4,
                                    sm=12,
                                    style={"border-right":"2px solid #515960"}
                                ),
                                dbc.Col(
                                    [
                                        html.H5("Casos Recuperados"),
<<<<<<< HEAD
                                        html.H2(id="total-recuperados", style={"color":"#508186"}),
=======
                                        html.H2(id="total-recuperados", style={"color":"#3FA8CA"}),
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
                                        html.H6(id="em-acompanhamento-texto")   
                                    ],
                                    md=4,
                                    sm=12,
                                    style={"border-right":"2px solid #515960"}
                                ),
                                dbc.Col(
                                    [
                                        html.H5("Óbitos Acumulados"),
<<<<<<< HEAD
                                        html.H2(id="obitos-acumulados-na-data", style={"color":"#972930"}),
=======
                                        html.H2(id="obitos-acumulados-na-data", style={"color":"#A93948"}),
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
                                        html.H6(id="novos-obitos-texto")
                                    ]
                                )
                            ],
                            className="text-center"
                        ),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Loading(
                                            dcc.Graph(
<<<<<<< HEAD
                                                id="line-chart-casos-br",
                                                config=modebar_config
=======
                                                id="line-chart-casos-br"
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
                                            ),
                                            type=spinner_type,
                                            color=spinner_color
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dcc.Loading(
                                            dcc.Graph(
<<<<<<< HEAD
                                                id="line-chart-obitos-br",
                                                config=modebar_config
=======
                                                id="line-chart-obitos-br"
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
                                            ),
                                            type=spinner_type,
                                            color=spinner_color
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )


class LeftContent():
    def __init__ (self):
        self.element = dbc.Card(
            [
                dbc.CardHeader(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.P("Selecione uma opção", className="d-flex justify-content-end text-light m-0")),
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            id="dropdown-map",
                                            options = [
                                                {"label":"Casos Acumulados", "value":"casosAcumulado"},
                                                {"label":"Óbitos Acumulados", "value":"obitosAcumulado"},
                                                {"label":"Incidência", "value":"incidencia"},
                                                {"label":"Mortalidade", "value":"mortalidade"},         
                                                {"label":"Taxa de Letalidade", "value":"taxaLetalidade"}
                                            ],
                                            value="casosAcumulado",
                                            clearable=False,
                                            searchable=False,
                                            className="custom-dropdown"
                                        )
                                    ]
                                )
                            ],
                            className="d-flex align-items-center"
                        )
                    ]
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dcc.Loading(
                                    dcc.Graph(
<<<<<<< HEAD
                                        id="macroregion-chart",
                                        config=modebar_config
=======
                                        id="macroregion-chart"
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
                                    ),
                                    type = spinner_type,
                                    color = spinner_color
                                ),
                                dcc.Loading(
                                    dcc.Graph(
<<<<<<< HEAD
                                        id="map-chart",
                                        config=modebar_config
=======
                                        id="map-chart"
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
                                    ),
                                    type = spinner_type,
                                    color = spinner_color
                                )
                            ]
                        )
                    ]
                )
            ],
            className="h-100"
        )


class RightContent():
    def __init__ (self):
        self.element = dbc.Card(
            [
                dbc.CardHeader(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.P("Selecione um Estado", className="d-flex justify-content-end text-light m-0")),
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            options=[{"label": estado, "value": estado} for estado in sorted(estados_df["estado"].unique())],
                                            value="São Paulo",
                                            clearable=False,
                                            searchable=False,
                                            id="dropdown-state"
                                        )
                                    ]
                                )
                            ],
                            className="d-flex align-items-center"
                        )
                    ]
                ),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dcc.Loading(
                                    dcc.Graph(
<<<<<<< HEAD
                                        id="lines-chart-state",
                                        config=modebar_config
=======
                                        id="lines-chart-state"
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
                                    ),
                                    type = spinner_type,
                                    color = spinner_color,
                                ),
                                html.Div(
                                    [
                                        dcc.Loading(
                                            dcc.Graph(
<<<<<<< HEAD
                                                id="stacked-bar-chart",
                                                config=modebar_config
=======
                                                id="stacked-bar-chart"
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
                                            ),
                                            type=spinner_type,
                                            color= spinner_color
                                        ),        
                                    ],
<<<<<<< HEAD
                                    style={"marginTop":"30px", "marginBottom":"50px"}
                                ),
                                dcc.Loading(
                                    dcc.Graph(
                                        id="lines-chart-state-new",
                                        config=modebar_config
=======
                                    style={"marginTop":"50px", "marginBottom":"50px"}
                                ),
                                dcc.Loading(
                                    dcc.Graph(
                                        id="lines-chart-state-new"
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
                                    ),
                                    type=spinner_type,
                                    color=spinner_color
                                )
                            ]
                        )
                    ]
                )
            ]
        )


class TabsContent():
    def __init__(self):
        self.element = dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.P("Indicadores Socioeconômicos no Contexto da Pré-Pandemia de Covid-19", style={"font-size":"20px", "margin":10})
                    ],
                    className="text-center text-light m-0 p-0"
                ),
                dbc.CardBody(
                    [
                        dcc.Store(id="indices-store"),
                        html.Div(
                            [
                                dcc.Tabs(
                                    [
                                        dcc.Tab(
                                            label="Índice de Gini",
                                            children=[
                                                html.Div(
                                                    [
                                                        dcc.Loading(
                                                            dcc.Graph(
<<<<<<< HEAD
                                                                id="scatter-chart-gini",
                                                                config=modebar_config
=======
                                                                id="scatter-chart-gini"
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
                                                            ),
                                                            type=spinner_type,
                                                            color=spinner_color
                                                        )
                                                    ]
                                                )
                                            ],
                                            className="custom-tab",
<<<<<<< HEAD
                                            selected_className='custom-tab--selected',
=======
                                            selected_className='custom-tab--selected'
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
                                        ),
                                        dcc.Tab(
                                            label="Índice de Palma",
                                            children=[
                                                html.Div(
                                                    [
                                                        dcc.Loading(
                                                            dcc.Graph(
<<<<<<< HEAD
                                                                id="scatter-chart-palma",
                                                                config=modebar_config
=======
                                                                id="scatter-chart-palma"
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
                                                            ),
                                                            type=spinner_type,
                                                            color=spinner_color
                                                        )
                                                    ]
                                                )
                                            ],
                                            className="custom-tab",
                                            selected_className='custom-tab--selected'
                                        ),
                                        dcc.Tab(
                                            label="Rendimento Médio per capita",
                                            children=[
                                                html.Div(
                                                    [
                                                        dcc.Loading(
                                                            dcc.Graph(
<<<<<<< HEAD
                                                                id="scatter-chart-rendimento",
                                                                config=modebar_config
=======
                                                                id="scatter-chart-rendimento"
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
                                                            ),
                                                            type=spinner_type,
                                                            color=spinner_color
                                                        )
                                                    ]
                                                )
                                            ],
                                            className="custom-tab",
                                            selected_className='custom-tab--selected'
                                        ),
                                        dcc.Tab(
                                            label="Despesa Média com Saúde",
                                            children=[
                                                html.Div(
                                                    [
                                                        dcc.Loading(
                                                            dcc.Graph(
<<<<<<< HEAD
                                                                id="scatter-chart-saude",
                                                                config=modebar_config
=======
                                                                id="scatter-chart-saude"
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
                                                            ),
                                                            type=spinner_type,
                                                            color=spinner_color
                                                        )
                                                    ]
                                                )
                                            ],
                                            className="custom-tab",
                                            selected_className='custom-tab--selected'
                                        ),
                                        dcc.Tab(
                                            label="Correlação",
                                            children=[
                                                html.Div(
                                                    [
                                                        dcc.Loading(
                                                            dcc.Graph(
<<<<<<< HEAD
                                                                id="confusion-matrix-chart",
                                                                config=modebar_config
=======
                                                                id="confusion-matrix-chart"
>>>>>>> 5f235899277fb8f0ee4b45bce750955fd4587af8
                                                            ),
                                                            type=spinner_type,
                                                            color=spinner_color
                                                        )
                                                    ]
                                                )
                                            ],
                                            className="custom-tab",
                                            selected_className='custom-tab--selected'
                                        )
                                     ]
                                )
                            ]
                        )
                    ]
                )
            ],
            className="h-100"
        )


class TabsAlertContent():
    def __init__(self):
        self.element = dbc.Card(
            [
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        [
                                            html.H5([html.I(className="fas fa-sticky-note"), " Notas"], className="text-center text-warning"),
                                            html.Hr(className="my-2"),
                                            html.P("Sobre os índices utilizados:", className="text-center text-light"),
                                            dcc.Markdown(
                                                '''
                                                    - Dados selecionados para 2019, ou seja, levou-se em consideração o cenário pré-pandêmico do Brasil.
                                                    - Rendimentos deflacionados para reais médios do próprio ano.
                                                    - Exclusive as pessoas cuja condição no arranjo domiciliar era pensionista, empregado doméstico ou parente do empregado doméstico.
                                                '''
                                            ),
                                            html.P("Fonte:", className="text-center text-light"),
                                            dcc.Markdown(
                                                '''
                                                    IBGE. Pesquisa Nacional por Amostra de Domicílios Contínua, 2019, acumulado de primeiras visitas. 	
                                                '''
                                            ),
                                            html.Span("Disponível em: "),
                                            html.A("IBGE", href="https://www.ibge.gov.br/", target="_blank", title="Fonte PNAD Contínua-2019"),
                                            html.Hr(className="my-2")
                                        ],
                                        className="h-100 p-5 bg-dark rounded-5",
                                    )
                                )  
                            ]
                        )
                    ]
                )
            ],
            style={"height":"100%"}
        )


class Content:
    @staticmethod
    def create_content():
        content = dbc.Container(
            [
                Header("Coronavírus no Brasil", "Navegando pela pandemia").element,
                TopContent().element,
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                LeftContent().element
                            ],
                            md=6,
                            sm=12
                            
                        ),
                        dbc.Col(
                            [
                                RightContent().element
                            ]
                        )
                    ]
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                TabsContent().element
                            ],
                            md=8,
                            sm=12
                        ),
                        dbc.Col(
                            [
                                TabsAlertContent().element
                            ],
                            md=4,
                            sm=12
                        )
                    ]
                )
            ]
        )
        return content