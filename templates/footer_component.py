import dash_bootstrap_components as dbc
from dash import html, dcc
from templates.navbar_component import LogoInitials, DownloadCvButton, SocialBar


class FooterComponent:
    def create_footer(self):
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
                        dbc.Button("Incidência", id="open-incidencia", outline=True, className="button-animation"),
                        dbc.Button("Letalidade", id="open-letalidade", outline=True, className="button-animation"),
                        dbc.Button("Mortalidade", id="open-mortalidade", outline=True, className="button-animation"),
                        
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


class ModalComponent:
    @staticmethod
    def create_modal(title, definition, interpretation, usage, restrictions, source, methodology, html_id):
        return dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle(title), className="d-flex justify-content-center"),
                dbc.ModalBody(
                    [
                        html.H5("Conceituação:"),
                        definition,
                        html.Hr(),
                        html.H5("Interpretação:"),
                        interpretation,
                        html.Hr(),
                        html.H5("Uso:"),
                        usage,
                        html.Hr(),
                        html.H5("Limitações:"),
                        restrictions,
                        html.Hr(),
                        html.H5("Fonte:"),
                        source,
                        html.Hr(),
                        html.H5("Método de Cálculo:"),
                        methodology,
                        html.Hr(),
                    ]
                )
            ],
            id=str(html_id),
            is_open=False,
            backdrop=True
        )
    
    def create_modal_incidencia():
        title = "Incidência"
        definition = html.P(
            "Número de óbitos confirmados de COVID-19 em relação ao total de casos confirmados "
            "na população residente em determinado espaço geográfico, no período considerado."
        )
        interpretaion = html.P(
            "Esta taxa dá a idéia de gravidade da doença, pois indica o percentual de pessoas "
            "que morreram dentre os casos confirmados da doença."
        )
        usage = html.P(
            "Relacionar o número de óbitos por determinada causa e o número de pessoas que foram acometidas por tal doença. "
            "Também pode ser utilizada para companhar a qualidade da assistência médica oferecida à população."     
        )
        restrictions = html.P(
            "Depende necessariamente do número de casos diagnosticados, que no caso do COVID-19, depende da "
            "quantidade de exames diagnósticos realizados."
        )
        source = html.Ul(
            [
                html.Li("Ministério da Saúde."),
                html.Li("Secretaria de Vigilância à Saúde (SVS): Guia de vigilância Epidemiológica."),
                html.Li("Secretarias Estaduais e Municipais de Saúde.")
            ]
        )             
        methodology = dcc.Markdown('''
            $$
            \\frac{\\text{Óbitos Confirmados}}{\\text{Casos Confirmados}}\\cdot{100}
            $$
        ''', mathjax=True
        )
        html_id="modal-incidencia"
        
        return ModalComponent.create_modal(title, definition, interpretaion, usage, restrictions, source, methodology, html_id) 

    
    def create_modal_letalidade():
        title = "Taxa de Letalidade"
        definition = html.P(
            "Número de óbitos confirmados de COVID-19 em relação ao total de casos confirmados "
            "na população residente em determinado espaço geográfico, no período considerado."
        )
        interpretaion = html.P(
            "Esta taxa dá a idéia de gravidade da doença, pois indica o percentual de pessoas "
            "que morreram dentre os casos confirmados da doença."
        )
        usage = html.P(
            "Relacionar o número de óbitos por determinada causa e o número de pessoas que foram acometidas por tal doença. "
            "Também pode ser utilizada para companhar a qualidade da assistência médica oferecida à população."     
        )
        restrictions = html.P(
            "Depende necessariamente do número de casos diagnosticados, que no caso do COVID-19, depende da "
            "quantidade de exames diagnósticos realizados."
        )
        source = html.Ul(
            [
                html.Li("Ministério da Saúde."),
                html.Li("Secretaria de Vigilância à Saúde (SVS): Guia de vigilância Epidemiológica."),
                html.Li("Secretarias Estaduais e Municipais de Saúde.")
            ]
        )             
        methodology = dcc.Markdown('''
            $$
            \\frac{\\text{Óbitos Confirmados}}{\\text{Casos Confirmados}}\\cdot{100}
            $$
        ''', mathjax=True
        )
        html_id="modal-letalidade"
        
        return ModalComponent.create_modal(title, definition, interpretaion, usage, restrictions, source, methodology, html_id)
        
        
    def create_modal_mortalidade():
            title = "Mortalidade"
            definition = html.P(
                "Número de óbitos confirmados de COVID-19 em relação ao total de casos confirmados "
                "na população residente em determinado espaço geográfico, no período considerado."
            )
            interpretaion = html.P(
                "Esta taxa dá a idéia de gravidade da doença, pois indica o percentual de pessoas "
                "que morreram dentre os casos confirmados da doença."
            )
            usage = html.P(
                "Relacionar o número de óbitos por determinada causa e o número de pessoas que foram acometidas por tal doença. "
                "Também pode ser utilizada para companhar a qualidade da assistência médica oferecida à população."     
            )
            restrictions = html.P(
                "Depende necessariamente do número de casos diagnosticados, que no caso do COVID-19, depende da "
                "quantidade de exames diagnósticos realizados."
            )
            source = html.Ul(
                [
                    html.Li("Ministério da Saúde."),
                    html.Li("Secretaria de Vigilância à Saúde (SVS): Guia de vigilância Epidemiológica."),
                    html.Li("Secretarias Estaduais e Municipais de Saúde.")
                ]
            )             
            methodology = dcc.Markdown('''
                $$
                \\frac{\\text{Óbitos Confirmados}}{\\text{Casos Confirmados}}\\cdot{100}
                $$
            ''', mathjax=True
            )
            html_id="modal-mortalidade"
            
            return ModalComponent.create_modal(title, definition, interpretaion, usage, restrictions, source, methodology, html_id) 
