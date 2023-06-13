from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

external_stylesheets=['https://use.fontawesome.com/releases/v5.8.1/css/all.css']
last_update = pd.to_datetime(pd.read_csv("data/processed/covid_br_dataset.csv", usecols=["data"])["data"].max()).strftime("%d/%m/%Y")


class LogoInitials:
    def __init__(self):
        self.element = html.A(
            html.Img(
                src="assets\imagens\logo_initials.png",
                height="75px"
            ),
            href="https://eduardo-pereira.webflow.io/",
            title="Visitar Portfólio",
            target="_blank",
            style={"textDecoration": "none"}
        )


class LogoApp:
    def __init__(self):
        self.element = html.A(
            html.Img(
                src="assets\imagens\logo_app.png",
                height="50px"
            ),
            href="/",
            style={"textDecoration": "none", "marginLeft": "20px", "marginRight": "20px"}
        )


class OpenVisaoGeral:
    def __init__(self):
        self.element = dbc.NavItem(
            dbc.NavLink("Visão Geral", id="open-visaoGeral", style={"cursor": "pointer"})
        )


class OpenObjetivos:
    def __init__(self):
        self.element = dbc.NavItem(
            dbc.NavLink("Objetivos", id="open-objetivos", style={"cursor": "pointer"})
        )


class OpenDados:
    def __init__(self):
        self.element = dbc.NavItem(
            dbc.NavLink("Dados", id="open-dados", style={"cursor": "pointer"})
        )


class OpenFrameworks:
    def __init__(self):
        self.element = dbc.NavItem(
            dbc.NavLink("Frameworks", id="open-frameworks", style={"cursor": "pointer"})
        )


class SocialBar:
    def __init__(self):
        self.element = html.Div(
            [
                html.A(
                    html.Img(
                        src="assets\imagens\gmail_icon.svg",
                        className="mr-2 inverted-icon",
                    ),
                    href="mailto:eduardojr.pereira@gmail.com",
                    target="_blank",
                    title="Enviar email"
                ),
                html.A(
                    html.Img(
                        src="assets\imagens\linkedin_icon.svg",
                        className="mr-2 inverted-icon",
                    ),
                    href="https://www.linkedin.com/in/eduardo-jr-pereira/",
                    target="_blank",
                    title="Ver perfil no Linkedin"
                ),
                html.A(
                    html.Img(
                        src="assets\imagens\github_icon.svg",
                        className="mr-2 inverted-icon",
                    ),
                    href="https://github.com/eduardojr-pereira",
                    target="_blank",
                    title="Visitar repositório no Github"
                ),
                html.A(
                    html.Img(
                        src="assets\imagens\discord_icon.svg",
                        className="mr-2 inverted-icon",
                    ),
                    href="https://discord.com/channels/1095050260964966483/1111074732503203900",
                    target="_blank",
                    title="Chamar no Discord"
                )
            ],
            className="d-flex justify-content-around"
        )


class DownloadCvButton:
    def __init__(self):
        self.element = dbc.Button(
            "Download - CV",
            href="assets\CV_EduardoPereira.pdf",
            download="CV_EduardoPereira",
            external_link=True,
            title="Curriculum Vitae - Eduardo Pereira",
            outline=True,
            className="btn btn-outline-light button-animation",
            style={"width": "175px"}
        )


class DropdownPortfolio:
    def __init__(self):
        self.element = dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.I(className="fas fa-camera", style={"width": "10px"}), width="auto"),
                                dbc.Col("Entry 1", width=True),
                            ],
                            align="center",
                        )
                    ],
                    href="projeto1",
                    target="_blank"
                ),
                dbc.DropdownMenuItem(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.I(className="far fa-file-alt", style={"width": "10px"}), width="auto"),
                                dbc.Col("Entry 2", width=True),
                            ],
                            align="center",
                        )
                    ],
                    href="projeto2",
                    target="_blank"
                ),
                dbc.DropdownMenuItem(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.I(className="fas fa-chart-bar", style={"width": "10px"}), width="auto"),
                                dbc.Col("Entry 3", width=True),
                            ],
                            align="center",
                        )
                    ],
                    href="projeto3",
                    target="_blank"
                ),
                dbc.DropdownMenuItem(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.I(className="fas fa-code", style={"width": "10px"}), width="auto"),
                                dbc.Col("Entry 4", width=True),
                            ],
                            align="center",
                        )
                    ],
                    href="projeto4",
                    target="_blank"
                ),
                dbc.DropdownMenuItem(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.I(className="fas fa-star", style={"width": "10px"}), width="auto"),
                                dbc.Col("Entry 5", width=True),
                            ],
                            align="center",
                        )
                    ],
                    href="projeto5",
                    target="_blank"
                ),
                dbc.DropdownMenuItem(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.I(className="fas fa-book", style={"width": "10px"}), width="auto"),
                                dbc.Col("Blog", width=True),
                            ],
                            align="center",
                        )
                    ],
                    href="/blog",
                    target="_blank"
                ),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem(html.P("Perfil Profissional:", className="text-center text-light"), disabled=True),
                dbc.DropdownMenuItem(SocialBar().element),
                dbc.DropdownMenuItem(
                    html.Div(
                        [
                            DownloadCvButton().element
                        ],
                        className="d-flex justify-content-center align-items-center mt-2 mb-2 w-100"
                    )
                )
            ],
            nav=True,
            in_navbar=True,
            label=[
                html.I(className="fas fa-code", style={"margin-right": "10px"}),
                "Portfólio"
            ]
        )


class NavbarComponent:
    @staticmethod
    def create_navbar():
        navbar = dbc.Navbar(
            dbc.Container(
                [
                    LogoApp().element,
                    dbc.NavbarToggler(id="navbar-toggler", n_clicks=0, style={"marginRight":"20px"}),
                    dbc.Collapse(
                        [
                            dbc.Nav(
                                [
                                    OpenVisaoGeral().element, 
                                    OpenObjetivos().element, 
                                    OpenDados().element, 
                                    OpenFrameworks().element, 
                                    DropdownPortfolio().element
                                 ],
                                className="me-auto",
                                navbar=True,
                            )
                        ],
                        id="navbar-collapse",
                        navbar=True,
                    )
                ]
            ),
            color="dark",
            dark=True
        )
        return navbar

           
class OffCanvas:
    @staticmethod
    def create_offcanvas_visao_geral():
        offcanvas_visao_geral = dbc.Offcanvas(
            id="offcanvas-visaoGeral",
            className= "offcanvas-animation",
            children=[
                html.H3("Visão Geral", className="text-center text-white"),
                html.Hr(),
                html.P(
                    "É de conhecimento geral que a pandemia do coronavírus tem impactado significativamente o Brasil e o mundo. Assim, acompanhar a "
                    "evolução dos casos, das taxas de transmissão e dos esforços de controle é de extrema importância." 
                ),
                html.Br(),
                html.P(
                    "Além disso, a disseminação de informações confiáveis é essencial para combater a desinformação e contribuir para uma " 
                    "compreensão clara da situação atual da pandemia no Brasil."
                ),
                html.Br(),
                dcc.Markdown('''
                    Nesse sentido, o aplicativo **coronaDash** visa suprir essa necessidade, fornecendo uma plataforma confiável e acessível
                    para a visualização e análise dos dados relacionados ao COVID-19.
                '''
                ),
                html.Br(),
                html.P(
                    "Através de ferramentas interativas como gráficos, mapas e análises de dados, o aplicativo permite aos usuários acompanhar de perto " 
                    "e compreender a situação da pandemia em nosso país. A plataforma também oferece a possibilidade de filtrar e selecionar informações "
                    "específicas, proporcionando uma visão clara e detalhada da evolução da pandemia do coronavírus no Brasil."
                )
            ]
        )
        return offcanvas_visao_geral

    @staticmethod
    def create_offcanvas_objetivos():
        objetivos =[
            "Utilizar ferramentas de Ciências de Dados para fornecer dados atualizados e confiáveis sobre o COVID-19 no Brasil;",
            "Permitir a visualização da evolução da pandemia em diferentes regiões do país;",
            "Oferecer ferramentas interativas para análise e visualização dos dados, auxiliando na identificação de tendências e padrões;",
            "Facilitar a compreensão dos dados através de gráficos e tabelas interativas;",
            "Possibilitar a comparação entre diferentes estados e municípios em relação ao número de casos e óbitos."
        ]
        
        offcanvas_objetivos = dbc.Offcanvas(
            id="offcanvas-objetivos",
            className= "offcanvas-animation",
            children=[
                html.H3("Objetivos", className="text-center text-white"),
                html.Hr(),
                html.H5("Objetivo principal:"),
                html.P(
                    "Este projeto tem como objetivo principal fornecer informações atualizadas e relevantes sobre a evolução da pandemia no Brasil, "
                    "de maneira confiável e acessível, para que todos possam se manter informados e tomar decisões bem embasadas diante dessa crise de saúde."
                ),
                html.Br(),
                html.H5("Objetivos específicos:"),
                html.Ol([html.Li(objetivo) for objetivo in objetivos])
            ]
        )
        return offcanvas_objetivos

    @staticmethod
    def create_offcanvas_dados():
        offcanvas_dados = dbc.Offcanvas(
            id="offcanvas-dados",
            className= "offcanvas-animation",
            children=[
                html.H3("Conjunto de Dados", className="position-relative text-center text-white"),
                html.Div(
                    [
                        dbc.Badge(f"Atualizado em: {last_update}", color="light")
                    ],
                    className="text-center w-100"
                ),
                html.Hr(),
                html.P(
                    "O conjunto de dados utilizado nesse projeto é disponibilizado diariamente " 
                    "pelo Ministério da Saúde através do Portal Brasileiro de Dados Abertos " 
                    "e as informações contidas no dataset incluem dados sobre casos e óbitos " 
                    "por COVID-19 no Brasil, agregados por estado, município e data."
                ),
                html.Br(),
                html.P(
                    "O dataset fornece informações valiosas para acompanhar a evolução do " 
                    "COVID-19 no Brasil, permitindo análises e visualizações para entender "
                    "a propagação da doença."
                ),
                html.Br(),
                html.P(
                    "Esse conjunto de dados apresenta um total de 6.406.528 registros " 
                    "e 17 colunas, além disso a memória utilizada pelo DataFrame é " 
                    "de aproximadamente 879,8MB"
                ),
                html.Br(),
                html.Div(
                    [                  
                        dbc.Button(
                            "Portal de Dados Abertos",
                            href="https://dados.gov.br/home",
                            title="Fonte dos dados para o Covid-19",
                            target="_blank",
                            outline=True,
                            className="btn btn-outline-light button-animation"
                        ),
                        dbc.Button(
                            "Download",
                            href="data//raw//HIST_PAINEL_COVIDBR_25mai2023.zip",                       
                            download="covid_dataset.zip",
                            external_link=True,
                            title="Baixar os dados brutos",
                            outline=True,
                            className="btn btn-outline-light button-animation"
                        ) 
                    ],
                    className="d-flex justify-content-between"
                )
            ]
        )
        return offcanvas_dados

    @staticmethod
    def create_offcanvas_frameworks():
        frameworks = [
            {"item": "Numpy", "descricao": "biblioteca Python para realizar cálculos numéricos eficientes."},
            {"item": "Pandas", "descricao": "biblioteca Python para análise e manipulação de dados."},
            {"item": "Dash", "descricao": "framework Python para a criação de aplicativos web interativos."},
            {"item": "Dash Bootstrap Components", "descricao": "conjunto de componentes Bootstrap para uso no Dash."},
            {"item": "Plotly", "descricao": "biblioteca Python para a criação de gráficos interativos."},
            {"item": "HTML e CSS", "descricao": "Linguagens de marcação e estilo para construir a interface do aplicativo Dash."},
            {"item": "JSON", "descricao": "biblioteca Python para trabalhar com dados no formato JSON."},
            {"item": "Jupyter Notebooks", "descricao": "ambiente para escrever e executar código Python de forma exploratória."},
            {"item": "Visual Studio Code", "descricao": "Ambiente de desenvolvimento integrado (IDE) para escrever, depurar e executar o código Python."}
        ]

        offcanvas_frameworks = dbc.Offcanvas(
            id="offcanvas-frameworks",
            className= "offcanvas-animation",
            children=[
                html.H3("Recursos e Frameworks utilizados", className="text-center text-white"),
                html.Hr(),
                html.Ul([html.Li([html.B(item["item"]+": ", className="text-white"), html.Span(item["descricao"])]) for item in frameworks]),
                html.Br(),
                html.P(
                    "Optou-se pela utilização das ferramentas supracitadas, especialmente por serem open-source e de fácil replicação.")
            ]
        )
        return offcanvas_frameworks


