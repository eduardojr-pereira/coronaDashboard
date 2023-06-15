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
                        dbc.Button("Mortalidade", id="open-mortalidade", outline=True, className="button-animation")        
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
        title = "Coeficiente de Incidência"
        definition = dcc.Markdown('''
            Número de casos confirmados de COVID-19 por 100.000 habitantes, na população residente em
            determinado espaço geográfico, no período considerado.
            
            > A definição de caso confirmado de COVID-19 baseia-se em critérios adotados pelo Ministério da Saúde para orientar as ações de vigilância epidemiológica da doença em todo o país.
        '''
        )
        interpretaion = html.P(
            "Estima o risco de ocorrência de casos de COVID-19 numa determinada população num período considerado."
        )
        usage = dcc.Markdown('''
            - Analisar variações populacionais, geográficas e temporais da distribuição dos casos confirmados de COVID-19, como parte do conjunto de ações de vigilância epidemiológica da doença.
            - Contribuir na avaliação dos níveis de saúde da população, prestando-se para comparações nacionais e internacionais.
            - Subsidiar processos de planejamento, gestão e avaliação de políticas e ações de saúde direcionadas para a o enfrentamento do COVID-19 no contexto da prevenção e controle das doenças.
        '''
        )
        restrictions = html.P(
            "Depende das condições técnico-operacionais do sistema de vigilância epidemiológica, em cada área geográfica, "
            "para detectar, notificar, investigar e realizar testes laboratoriais específicos para a confirmação diagnóstica de casos de COVID-19."
        )
        source = dcc.Markdown(
             '''
                - Ministério da Saúde.
                - Secretaria de Vigilância à Saúde (SVS): Guia de vigilância Epidemiológica.
                - Secretarias Estaduais e Municipais de Saúde.
                - População: Estimativas de 2019 utilizadas pelo TCU para determinação das cotas do FPM (sem sexo e faixa etária). 

                > Disponível em: [DataSus.gov](https://datasus.saude.gov.br/populacao-residente/)
             '''
        )           
        methodology = dcc.Markdown('''
            $$
            \\frac{\\text{Casos Confirmados}}{\\text{Pop. Total Residente}}\\cdot{100000}
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
        source = dcc.Markdown(
             '''
                - Ministério da Saúde.
                - Secretaria de Vigilância à Saúde (SVS): Guia de vigilância Epidemiológica.
                - Secretarias Estaduais e Municipais de Saúde.
                - População: Estimativas de 2019 utilizadas pelo TCU para determinação das cotas do FPM (sem sexo e faixa etária). 

                    > Disponível em: [DataSus.gov](https://datasus.saude.gov.br/populacao-residente/)
             '''
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
            title = "Coeficiente de Mortalidade"
            definition = html.P(
                "Número de óbitos por doenças COVID-19, por 100 mil habitantes, na população residente em "
                "determinado espaço geográfico, no ano considerado."
            )
            interpretaion = dcc.Markdown('''
                - Estima o risco de morte pela COVID-19 consideradas e dimensiona a sua magnitude como problema de saúde pública.
                - Reflete também a efetividade de medidas de prevenção e controle, bem como as condições de diagnóstico e da assistência médica dispensada.
                - A taxa de mortalidade específica não padronizada por idade está sujeita à influência de variações na composição etária da população, o que exige cautela nas comparações entre áreas geográficas e para períodos distintos.
            '''
            )
            usage = html.P(
                "Analisar variações populacionais, geográficas e temporais da mortalidade por COVID-19 em segmentos populacionais, "
                "identificando situações de desigualdade e tendências que demandem ações e estudos específicos."
            )
            restrictions = html.P(
                "Apresenta restrição de uso sempre que ocorra elevada proporção de óbitos sem assistência médica ou por causas mal definidas."
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
                \\frac{\\text{Óbitos Confirmados}}{\\text{Pop. Total Residente}}\\cdot{100000}
                $$
            ''', mathjax=True
            )
            html_id="modal-mortalidade"
            
            return ModalComponent.create_modal(title, definition, interpretaion, usage, restrictions, source, methodology, html_id) 
