from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

# Carregar os dados
estados_df = pd.read_csv("data/processed/covid_estados_dataset.csv", usecols=["estado"])
brasil_df = pd.read_csv("data/processed/covid_br_dataset.csv", usecols=["data"])
first_date = brasil_df["data"].min()
last_date = brasil_df["data"].max()

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
                        dcc.Store(id="datepicker-store-states"),
                        dcc.Store(id="datepicker-store-macroregion")
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
                            style={"border-right":"2px solid #515960"}
                        ),
                        dbc.Col(
                            [
                                html.H5("Casos Recuperados"),
                                html.H2(id="total-recuperados", style={"color":"#3FA8CA"}),
                                html.H6(id="em-acompanhamento-texto")   
                            ],
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
                                        id="line-chart-casos-brasil"
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
                                        id="line-chart-obitos-brasil"
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
                            searchable=False
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
                ),
                html.P(id="mapa-texto", className="text-center text-secondary mt-0 mb-0")
            ]
        )


class LeftCardContent():
    def __init__ (self):
        self.element = dbc.Card(
            [
                dbc.CardHeader(LeftCardHeader().element),
                dbc.CardBody(LeftCardBody().element)
            ]
        )


class RightCardHeader():
    def __init__ (self):
        self.element = dbc.Row(
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
                            searchable=False
                        )
                    ]
                )
            ],
            className="d-flex align-items-center"
        )


class RightCardBody():
    def __init__ (self):
        self.element = dbc.Row(
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
        

class RightCardContent():
    def __init__ (self):
        self.element = dbc.Card(
            [
                dbc.CardHeader(RightCardHeader().element),
                dbc.CardBody(RightCardBody().element)
            ]
        )
            

class RowStatesCardHeader():
    def __init__ (self):
        self.element = dbc.Row(
            [
                dbc.Col(html.P("Selecione um Estado", className="d-flex justify-content-end text-light m-0")),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            estados_df["estado"].unique(),
                            value="São Paulo",
                            clearable=False,
                            searchable=False,
                            id="dropdown-estado"
                        )
                    ]
                )
            ],
            className="d-flex align-items-center"
        )


class RowStatesCardBody():
    def __init__ (self):
        self.element = dbc.Row(
            [
                dcc.Loading(
                    dcc.Graph(
                        id="line-chart-estado"
                    ),
                    type = spinner_type,
                    color = spinner_color
                ),
                dcc.Loading(
                    dcc.Graph(
                        id="stacked-bar-chart-on-hover"
                    ),
                    type=spinner_type,
                    color= spinner_color
                )
            ]
        )


class RowStatesCardContent():
    def __init__ (self):
        self.element = dbc.Card(
            [
                dbc.CardHeader(RowStatesCardHeader().element),
                dbc.CardBody(RowStatesCardBody().element)
            ]
        )


class LastCardContent():
    def __init__ (self):
        self.element = dbc.Card(
            [
                dbc.CardHeader(html.H4("Taxa de Letalidade", className="text-center")),
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Loading(
                                            dcc.Graph(
                                                id="taxaLetalidade"
                                            ),
                                            type = spinner_type,
                                            color = spinner_color
                                        )
                                    ]
                                ),
                                dbc.Col(
                                    [
                                        dcc.Loading(
                                            dcc.Graph(
                                                id="alguma-coisa-aqui"
                                            )
                                        )
                                    ]
                                )
                                
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Loading(
                                            dcc.Graph(
                                                id="scatter-plot-letalidade"
                                            ),
                                            type = spinner_type,
                                            color = spinner_color
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
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
                        dbc.Col(LeftCardContent().element),
                        dbc.Col(RightCardContent().element)
                    ]
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(RowStatesCardContent().element)
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(LastCardContent().element)
                    ]
                )
            ]
        )
        return content