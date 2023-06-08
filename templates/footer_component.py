import dash_bootstrap_components as dbc
from dash import html
from templates.navbar import LogoInitials, DownloadCvButton, SocialBar


class FooterComponent:
    def criar_footer(self):
        logo_initials = LogoInitials().element
        donwload_btn = html.Div(DownloadCvButton().element, className="mb-3")

        about_me = html.P(
            "Sou um profissional com formação em Economia e pós-graduação em Ciência de Dados. "
            "Tenho habilidades em programação, análise estatística e aprendizado de máquina, além de experiência "
            "em bancos de dados, processamento de linguagem natural e também em análise e classificação de imagens."
        )

        button_group_offcanvas = html.Div(
            [
                html.H6("Sobre o APP"),
                dbc.ButtonGroup(
                    [
                        dbc.Button("Vião Geral", id="open-visaoGeral-footer", outline=True, className="button-animation"),
                        dbc.Button("Objetivos", id="open-objetivos-footer", outline=True, className="button-animation"),
                        dbc.Button("Conjunto de Dados", id="open-dados-footer", outline=True, className="button-animation"),
                        dbc.Button("Frameworks utilizados", id="open-frameworks-footer", outline=True, className="button-animation")
                    ],
                    vertical=True
                )
            ],
            className="text-center text-warning"
        )
        
        button_group_modal = html.Div(
            [
                html.H6("Saiba mais"),
                dbc.ButtonGroup(
                    [
                        dbc.Button("Taxa de Letalidade", id="open-modal-letalidade", outline=True, className="button-animation"),
                        dbc.Button("Taxa de Incidência", id="open-modal-incidencia", outline=True, className="button-animation"),
                    ],
                    vertical=True
                )
            ],
            className="text-center text-warning mb-3"
        )
        
        social_bar = html.Div(SocialBar().element, className="mt-2 mb-2")

        row_infos = html.Div(
            [ 
                dbc.Row(
                    [
                        dbc.Col(html.I(className="fas fa-phone"), width="auto"),
                        dbc.Col("+55 35 991751101", className="ml-2")
                    ],
                    className="align-items-center mt-2 mb-2"
                ),
                dbc.Row(
                    [
                        social_bar
                    ]
                )
            ],
            style={"border":"1px solid #515960", "border-radius":"8px", "padding":"8px"}
        )

        footer = dbc.Container(
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                 dbc.Col(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(logo_initials, width="auto"),
                                                dbc.Col(html.H2("Eduardo Pereira"), width=True),
                                            ],
                                            align="center"
                                        ),
                                        html.Hr(),
                                        about_me,
                                        donwload_btn
                                    ],
                                    md=6
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(button_group_offcanvas),
                                                dbc.Col(button_group_modal),
                                                dbc.Col([html.H6("Contato", className="text-center text-warning"),row_infos]),
                                            ]
                                        )
                                    ]
                                )
                            ],
                            justify="between",
                            className="m-4"
                        )
                    ]
                )
            )
        )

        return footer
    
# Exemplo de uso do FooterComponent
#footer_component = FooterComponent()
#footer = footer_component.criar_footer()
#className="d-flex justify-content-end"