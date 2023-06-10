from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

# Carregar os dados
brasil_df = pd.read_csv("data\processed\covid_br_dataset.csv")
estados_df = pd.read_csv("data\processed\covid_estados_dataset.csv")

spinner_color = "BurlyWood"
spinner_type = "dot"

class Header:
    def __init__(self, title, *subtitle):
        self.title = title
        self.subtitle = subtitle
        self.element = html.Div(
            [
                html.H1(self.title),
                html.H3(self.subtitle, className="hide-on-smal-screen")
            ],
            className="text-center text-light"
        )


class DatePicker:
    def __init__(self):
        self.element = dbc.Row(
            [
                dbc.Col(html.P("Selecione uma data", className="d-flex justify-content-end text-light m-0")),
                dbc.Col(
                    [
                        dcc.DatePickerSingle(
                            id="datepicker",
                            min_date_allowed = brasil_df['data'].min(),
                            max_date_allowed=brasil_df["data"].max(),
                            initial_visible_month=brasil_df["data"].max(),
                            date=brasil_df["data"].max(),
                            display_format="DD/MM/YYYY"   
                        ),
                        dcc.Store(id="datepicker-store")
                    ]
                )
            ],
            className="d-flex align-items-center m-0"
        )


class TopCardsInner:
    def __init__(self):
        left_card_tittle = html.H5("Casos Acumulados")
        left_card_subtitle = html.H2(id="casos-acumulados-na-data", style={"color":"#F7A177"})
        left_card_caption = html.H6(id="novos-casos-texto")

        middle_card_tittle = html.H5("Casos Recuperados")
        middle_card_subtitle = html.H2(id="total-recuperados", style={"color":"#3FA8CA"})
        middle_card_caption = html.H6(id="em-acompanhamento-texto")

        right_card_tittle = html.H5("Óbitos Acumulados")
        right_card_subtitle = html.H2(id="obitos-acumulados-na-data", style={"color":"#A93948"})
        right_card_caption = html.H6(id="novos-obitos-texto")

        self.element = dbc.Row(
            [
                dbc.Col(
                    [
                        left_card_tittle,
                        left_card_subtitle,
                        left_card_caption
                    ],
                    style={"border-right":"2px solid #515960"}
                ),
                dbc.Col(
                    [
                        middle_card_tittle,
                        middle_card_subtitle,
                        middle_card_caption   
                    ],
                    style={"border-right":"2px solid #515960"}
                ),
                dbc.Col(
                    [
                        right_card_tittle,
                        right_card_subtitle,
                        right_card_caption
                    ]
                )
            ],
            className="text-center"
        )


class TopCard:
    def __init__ (self):
        self.element = dbc.Card(
            [
                dbc.CardHeader(DatePicker().element),
                dbc.CardBody(TopCardsInner().element)
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
                                {"label":"Taxa de Letalidade*", "value":"taxaLetalidade"},
                                {"label":"Mortalidade*", "value":"mortalidade"}
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
                        id="map-chart"
                    ),
                    type = spinner_type,
                    color = spinner_color
                ),
                dcc.Loading(
                    dcc.Graph(
                        id="stacked-bars-br"
                    ),
                    type = spinner_type,
                    color = spinner_color
                ),
                html.P(id="mapa-texto", className="text-center text-secondary mt-3 mb-3"),
                html.Hr(),
                dcc.Loading(
                    dcc.Graph(
                        id="lines-chart-casos-brasil"
                    ),
                    type = spinner_type,
                    color = spinner_color
                ),
                dcc.Loading(
                    dcc.Graph(
                        id="lines-chart-obitos-brasil"
                    ),
                    type = spinner_type,
                    color = spinner_color
                ),
                html.P("**Clique nas legendas e utilize o rangeslider para filtrar.", className="text-center text-secondary mt-3 mb-3"),
            ]
        )
        

class LeftCardContent():
    def __init__ (self):
        self.element = html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardHeader(LeftCardHeader().element),
                        dbc.CardBody(LeftCardBody().element)
                    ],
                    className="h-100"
                ),
                html.Br()
            ]
        )


class RightCardHeaderTop():
    def __init__ (self):
        self.element = dbc.Row(
            [
                dbc.Col(html.P("Selecione uma Macroregião", className="d-flex justify-content-end text-light m-0")),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            id="dropdown-region",
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


class RightCardBodyTop():
    def __init__ (self):
        self.element = html.Div(
            [
                html.P(id="macroregiao-texto", className="text-light m-0", style={"font-size":"18px"}),
                dbc.Badge(id="badge-texto", color="light", className="text-center"),
                dcc.Loading(
                    dcc.Graph(
                        id="bar-chart-casos-obitos",
                        hoverData={"points":[{"customdata":"SP"}]}
                    ),
                    type=spinner_type,
                    color= spinner_color
                )
            ],
            className="text-center"
        )


class RightCardTopContent():
    def __init__ (self):
        self.element = dbc.Card(
            [
                dbc.CardHeader(RightCardHeaderTop().element),
                dbc.CardBody(RightCardBodyTop().element)
            ]
        )


class RightCardHeaderBottom():
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


class RightCardBodyBototm():
    def __init__ (self):
        self.element = dbc.Row(
            [
                dcc.Loading(
                    dcc.Graph(
                        id="lines-chart-estado"
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


class RightCardBottomContent():
    def __init__ (self):
        self.element = dbc.Card(
            [
                dbc.CardHeader(RightCardHeaderBottom().element),
                dbc.CardBody(RightCardBodyBototm().element)
            ]
        )


class RightCardContent():
    def __init__(self):
        self.element =html.Div(
            [
                RightCardTopContent().element, 
                html.Br(), 
                RightCardBottomContent().element,
                html.Br()
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
                TopCard().element,
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(LeftCardContent().element),
                        dbc.Col(RightCardContent().element)
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