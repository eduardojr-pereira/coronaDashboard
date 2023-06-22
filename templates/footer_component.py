import dash_bootstrap_components as dbc
from dash import html, dcc
from templates.navbar_component import LogoInitials, DownloadCvButton, SocialBar


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
            backdrop=True,
            className="modal-animation"
        )
    

    def create_modal_gini():
        title=dcc.Markdown('''Índice de Gini da Distribuição do Rendimento Domiciliar *per capita*''')
        definition = dcc.Markdown(
             '''
                O índice de Gini é uma medida que quantifica a desigualdade de renda ou distribuição de riqueza em uma determinada população. 
                Foi desenvolvido pelo estatístico italiano Corrado Gini em 1912 e varia de 0 a 1.
            '''
        )
        interpretation = dcc.Markdown(
             '''
                A interpretação do índice de Gini baseia-se na análise da curva de Lorenz, que relaciona a proporção cumulativa da renda ou riqueza da população 
                com a proporção cumulativa da população. Quanto mais próxima a curva de Lorenz estiver da linha de igualdade perfeita, menor será o índice de Gini 
                e mais igualitária será a distribuição. Por outro lado, quanto mais a curva de Lorenz se desviar da linha de igualdade, 
                maior será o índice de Gini e mais desigual será a distribuição. 
                <br>
                Em outras palavras, Um valor de 0 indica igualdade perfeita, onde todos os indivíduos possuem a mesma parcela de renda ou riqueza, 
                enquanto um valor de 1 representa desigualdade máxima, em que uma única pessoa detém toda a renda ou riqueza.
            '''
        )
        usage = dcc.Markdown(
            '''
                O índice de Gini é amplamente utilizado para análises socioeconômicas e comparações entre países ou regiões. Ele oferece uma medida 
                resumida da desigualdade e ajuda a identificar disparidades significativas na distribuição de renda ou riqueza. 
                Com base nessa medida, formuladores de políticas, economistas e pesquisadores podem avaliar o impacto de políticas públicas e 
                identificar áreas com maiores níveis de desigualdade.
            '''
        )
        restrictions = dcc.Markdown(
            '''
                Embora seja uma ferramenta útil, o índice de Gini também possui algumas restrições. Ele se baseia na distribuição de renda ou riqueza em um 
                determinado momento, o que significa que não captura mudanças ao longo do tempo. Além disso, o índice de Gini não fornece informações detalhadas 
                sobre as causas subjacentes da desigualdade, limitando sua capacidade de oferecer soluções precisas para reduzir a disparidade econômica.
            '''
        )
        source = dcc.Markdown(
            '''
            - IBGE. Pesquisa Nacional por Amostra de Domicílios Contínua, 2019, acumulado de primeiras visitas.	
            '''
        )
        methodology = dcc.Markdown(
            '''
                 $$
                 G=\sum_{i=1}^{k=n-1}(P_{k+1}-P_k)(R_{k+1}-R_k)
                 $$

                 - G = Coeficiente de Gini;
                 - P = Proporção acumulada da população;
                 - R = Proporção acumulada da renda.
            ''', 
            mathjax=True
        )
        html_id = "modal-gini"

        return ModalComponent.create_modal(title, definition, interpretation, usage, restrictions, source, methodology, html_id) 


    def create_modal_palma():
        title=dcc.Markdown('''Índice de Palma da Distribuição do Rendimento Domiciliar *per capita*''')
        definition = dcc.Markdown(
             '''
                O índice de Palma é uma medida que avalia a desigualdade de renda com base na comparação entre a parcela de renda dos 10% mais ricos e dos 
                40% mais pobres de uma população. Esse indicador foi proposto por José Gabriel Palma, economista chileno, como uma alternativa ao índice de Gini 
                para capturar especificamente a desigualdade entre os estratos mais ricos e mais pobres da sociedade.
            '''
        )
        interpretation = dcc.Markdown(
             '''
                A interpretação do índice de Palma é direta: quanto maior o valor do índice, maior é a desigualdade entre os estratos de alta renda e baixa renda. 
                Ele foca na comparação entre os 10% mais ricos e os 40% mais pobres, destacando a diferença extrema entre esses grupos. Diferentemente do índice de Gini, 
                o índice de Palma não fornece uma visão geral da distribuição de renda, mas se concentra em uma comparação específica.
            '''
        )
        usage = dcc.Markdown(
            '''
                O índice de Palma é utilizado para analisar a desigualdade de renda em diferentes contextos e pode ser aplicado para comparar países ou regiões. Ele oferece 
                uma perspectiva mais focalizada na desigualdade entre os estratos de alta e baixa renda, ajudando a identificar as disparidades mais acentuadas. 
                Isso pode ser útil para orientar políticas públicas e iniciativas de redução da desigualdade, direcionando esforços para as camadas mais vulneráveis da sociedade.
            '''
        )
        restrictions = dcc.Markdown(
            '''
                Assim como o índice de Gini, o índice de Palma também possui algumas limitações. Ele não considera a desigualdade dentro dos estratos intermediários 
                de renda, concentrando-se apenas nas extremidades da distribuição. Além disso, assim como qualquer medida de desigualdade, o índice de Palma não captura 
                totalmente as complexidades socioeconômicas e as diferentes dimensões da desigualdade, como acesso a serviços básicos e oportunidades educacionais.
            '''
        )
        source = dcc.Markdown(
            '''
                - IBGE. Pesquisa Nacional por Amostra de Domicílios Contínua, 2019, acumulado de primeiras visitas.
            '''
        )
        methodology = dcc.Markdown(
            '''
                $$
                \\text{Índice de Palma} = \\frac{{\\text{Parcela de Renda dos 10% mais Ricos}}}{{\\text{Parcela de Renda dos 40% mais Pobres}}}
                $$
            ''', 
            mathjax=True
        )
        html_id = "modal-palma"

        return ModalComponent.create_modal(title, definition, interpretation, usage, restrictions, source, methodology, html_id) 


    def create_modal_incidencia():
        title = "Coeficiente de Incidência"
        definition = dcc.Markdown(
            '''
                Número de casos confirmados de COVID-19 por 100.000 habitantes, na população residente em
                determinado espaço geográfico, no período considerado.
                    
                - A definição de caso confirmado de COVID-19 baseia-se em critérios adotados pelo Ministério da Saúde para orientar as ações de vigilância epidemiológica da doença em todo o país.
            '''
        )
        interpretation = html.P(
            "Estima o risco de ocorrência de casos de COVID-19 numa determinada população num período considerado."
        )
        usage = dcc.Markdown(
            '''
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
            '''
        )           
        methodology = dcc.Markdown(
            '''
                $$
                \\frac{\\text{Casos Confirmados}}{\\text{Pop. Total Residente}}\\cdot{100000}
                $$
            ''', 
            mathjax=True
        )
        html_id="modal-incidencia"
        
        return ModalComponent.create_modal(title, definition, interpretation, usage, restrictions, source, methodology, html_id) 
    
        
    def create_modal_mortalidade():
            title = "Coeficiente de Mortalidade"
            definition = html.P(
                "Número de óbitos por doenças COVID-19, por 100 mil habitantes, na população residente em "
                "determinado espaço geográfico, no ano considerado."
            )
            interpretation = dcc.Markdown(
                '''
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
            source = dcc.Markdown(
                '''
                    - Ministério da Saúde.
                    - Secretaria de Vigilância à Saúde (SVS): Guia de vigilância Epidemiológica.
                    - Secretarias Estaduais e Municipais de Saúde.
                    - População: Estimativas de 2019 utilizadas pelo TCU para determinação das cotas do FPM (sem sexo e faixa etária). 
                '''
            )                
            methodology = dcc.Markdown(
                '''
                    $$
                    \\frac{\\text{Óbitos Confirmados}}{\\text{Pop. Total Residente}}\\cdot{100000}
                    $$
                ''', 
                mathjax=True
            )
            html_id="modal-mortalidade"
            
            return ModalComponent.create_modal(title, definition, interpretation, usage, restrictions, source, methodology, html_id) 


    def create_modal_letalidade():
        title = "Taxa de Letalidade"
        definition = html.P(
            "Número de óbitos confirmados de COVID-19 em relação ao total de casos confirmados "
            "na população residente em determinado espaço geográfico, no período considerado."
        )
        interpretation = html.P(
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
            '''
        )            
        methodology = dcc.Markdown(
            '''
                $$
                \\frac{\\text{Óbitos Confirmados}}{\\text{Casos Confirmados}}\\cdot{100}
                $$
            ''', 
            mathjax=True
        )
        html_id="modal-letalidade"
        
        return ModalComponent.create_modal(title, definition, interpretation, usage, restrictions, source, methodology, html_id)


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
                html.H6("Entenda"),
                dbc.ButtonGroup(
                    [
                        dbc.Button("Índice de Gini", id="open-gini", outline=True, className="button-animation"),
                        dbc.Button("Índice de Palma", id="open-palma", outline=True, className="button-animation"),
                        dbc.Button("Incidência", id="open-incidencia", outline=True, className="button-animation"),
                        dbc.Button("Mortalidade", id="open-mortalidade", outline=True, className="button-animation"),
                        dbc.Button("Letalidade", id="open-letalidade", outline=True, className="button-animation")        
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
                                                dbc.Col([html.H6("Dúvidas/Sugestões", className="text-center text-warning"),row_infos]),
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
