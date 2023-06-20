from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from dash.dash_table.Format import Format, Scheme
import pandas as pd

# Carregar os dados
estados_df = pd.read_csv("data/processed/covid_estados_dataset.csv", usecols=["data", "estado"])
first_date = estados_df["data"].min()
last_date = estados_df["data"].max()

# Determinar padrões para o spinner
spinner_color = "BurlyWood"
spinner_type = "dot"

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


class TopCardHeader:
    def __init__(self):
        self.element = dbc.Row(
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
                        dcc.Store(id="store-states-on-date"),
                        dcc.Store(id="store-macroregion-on-date"),
                        dcc.Store(id="store-states-until-date")
                    ]
                )
            ],
            className="d-flex align-items-center m-0"
        )


class TopCardBody:
    def __init__(self):
        self.element = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H5("Casos Acumulados"),
                                html.H2(id="casos-acumulados-na-data", style={"color":"#F7A177"}),
                                html.H6(id="novos-casos-texto")
                            ],
                            md=4,
                            sm=12,
                            style={"border-right":"2px solid #515960"}
                        ),
                        dbc.Col(
                            [
                                html.H5("Casos Recuperados"),
                                html.H2(id="total-recuperados", style={"color":"#3FA8CA"}),
                                html.H6(id="em-acompanhamento-texto")   
                            ],
                            md=4,
                            sm=12,
                            style={"border-right":"2px solid #515960"}
                        ),
                        dbc.Col(
                            [
                                html.H5("Óbitos Acumulados"),
                                html.H2(id="obitos-acumulados-na-data", style={"color":"#A93948"}),
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
                                        id="line-chart-casos-br"
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
                                        id="line-chart-obitos-br"
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


class TopCardContent:
    def __init__ (self):
        self.element = dbc.Card(
            [
                dbc.CardHeader(TopCardHeader().element),
                dbc.CardBody(TopCardBody().element)
            ]
        )


class LeftCardHeader():
    def __init__ (self):
        self.element = dbc.Row(
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


class LeftCardBody():
    def __init__ (self):
        self.element = dbc.Row(
            [
                dcc.Loading(
                    dcc.Graph(
                        id="macroregion-chart"
                    ),
                    type = spinner_type,
                    color = spinner_color
                ),
                dcc.Loading(
                    dcc.Graph(
                        id="map-chart"
                    ),
                    type = spinner_type,
                    color = spinner_color
                )
            ]
        )


class MainLeftContent():
    def __init__ (self):
        self.element = dbc.Card(
            [
                dbc.CardHeader(LeftCardHeader().element),
                dbc.CardBody(LeftCardBody().element)
            ],
            className="h-100"
        )


class RightCardContentTop():
    def __init__ (self):
        self.element = dbc.Card(
            [
                dbc.CardHeader(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.P("Selecione uma Macroregião", className="d-flex justify-content-end text-light m-0")),
                                dbc.Col(
                                    [
                                        dcc.Dropdown(
                                            id="dropdown-macroregion",
                                            options = [
                                                {"label":"Norte", "value":"Norte"},
                                                {"label":"Nordeste", "value":"Nordeste"},
                                                {"label":"Centro-Oeste", "value":"Centro-Oeste"},
                                                {"label":"Sudeste", "value":"Sudeste"},
                                                {"label":"Sul", "value":"Sul"}
                                            ],
                                            value="Sudeste",
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
                                        id="subplots-states"
                                    ),
                                    type=spinner_type,
                                    color= spinner_color
                                )
                            ],
                            className="text-center"
                        )
                    ]
                )
            ]
        )
            

class RightCardContentBottom():
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
                                        id="line-chart-state"
                                    ),
                                    type = spinner_type,
                                    color = spinner_color,
                                ),
                                dcc.Loading(
                                    dcc.Graph(
                                        id="stacked-bar-chart"
                                    ),
                                    type=spinner_type,
                                    color= spinner_color
                                )
                            ]
                        )
                    ]
                )
            ]
        )
        

class MainRightContent():
    def __init__ (self):
        self.element = html.Div(
            [
                RightCardContentTop().element,
                html.Br(),
                RightCardContentBottom().element
            ]
        )


class TabsCardContent():
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
                                                                id="scatter-chart-gini"
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
                                            label="Índice de Palma",
                                            children=[
                                                html.Div(
                                                    [
                                                        dcc.Loading(
                                                            dcc.Graph(
                                                                id="scatter-chart-palma"
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
                                                                id="scatter-chart-rendimento"
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
                                                                id="scatter-chart-saude"
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
            ]
        )


class ConfusionMatrixCardContent():
    def __init__(self):
        self.element = dbc.Card(
            [
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Loading(
                                            dcc.Graph(
                                                id="matrix-corr-chart"
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
            ],
            style={"height":"100%"}
        )


class Content:
    @staticmethod
    def create_content():
        content = dbc.Container(
            [
                Header("Coronavírus no Brasil", "Navegando pela pandemia").element,
                TopCardContent().element,
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                MainLeftContent().element
                            ],
                            md=6,
                            sm=12
                            
                        ),
                        dbc.Col(
                            [
                                MainRightContent().element
                            ]
                        )
                    ]
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                TabsCardContent().element
                            ],
                            md=8,
                            sm=12
                        ),
                        dbc.Col(
                            [
                                ConfusionMatrixCardContent().element
                            ],
                            md=4,
                            sm=12
                        )
                    ]
                )
            ]
        )
        return content