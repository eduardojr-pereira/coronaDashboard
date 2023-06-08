import dash_bootstrap_components as dbc
from dash import html
from templates.navbar import LogoInitials, DownloadCvButton


class FooterComponent:
    def criar_footer(self):
        logo_initials = LogoInitials().element
        download_btn = DownloadCvButton().element

        descricao = html.Div(
            [
                html.P(
                    "Sou um profissional com formação em Economia e pós-graduação em ciência de dados. "
                    "Tenho habilidades em programação, análise estatística e aprendizado de máquina, além de experiência "
                    "em bancos de dados, processamento de linguagem natural e análise de imagens.",
                    className="m-2"
                ),
                html.P(
                    "Combinando meu conhecimento em economia e ciência de dados, trago uma perspectiva estratégica "
                    "para projetos de análise de dados e soluções de aprendizado de máquina, buscando fornecer insights "
                    "valiosos para tomadas de decisões informadas.",
                    className="m-2"
                ),
            ]
        )

        leia_mais_btn = dbc.Button(
            "Ler mais",
            href="https://eduardo-pereira.webflow.io/",
            title="Portfólio de Ciência de Dados",
            target="_blank",
            className="btn btn-outline-warning btn-sm mt-2 mb-2",
            style={"width": "175px"}
        )

        col_descricao = dbc.Col(
            [
                logo_initials,
                html.H2("Eduardo Pereira"),
                html.Hr(),
                descricao,
                dbc.Row(
                    [
                        dbc.Col(leia_mais_btn),
                        dbc.Col(download_btn)
                    ],
                    className="text-center"
                )
            ],
            md=6
        )

        col_navegacao = dbc.Col(
            html.Div(
                [
                    html.H6("Navegação")
                ],
                className="m-5"
            )
        )

        footer = html.Div(
            dbc.Container(
                dbc.Card(
                    dbc.CardBody(
                        dbc.Row(
                            [
                                col_descricao,
                                col_navegacao
                            ]
                        )
                    )
                )
            )
        )

        return footer

# Exemplo de uso do FooterComponent
#footer_component = FooterComponent()
#footer = footer_component.criar_footer()
