from templates.navbar_component import NavbarComponent, OffCanvas
from templates.content_component import Content
from templates.footer_component import FooterComponent, ModalComponent
from dash import ctx, Dash, html, Input, Output, State 
from plotly.subplots import make_subplots
import plotly.colors 
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import json


# Instanciar APP
app=Dash(
    __name__,
    title="coronaDash - Eduardo Pereira",
    external_stylesheets=[dbc.themes.SLATE,'https://use.fontawesome.com/releases/v5.8.1/css/all.css'],
    meta_tags=[{"name":"viewport","content":"width=device-width, inital-scale=1","http-equiv": "X-UA-Compatible", "content": "IE=9"}]
)


# Carregar os dados
brasil_df = pd.read_csv("data\processed\covid_br_dataset.csv")
estados_df = pd.read_csv("data\processed\covid_estados_dataset.csv")
geo_data = json.load(open("data/raw/brasilGeo.json", "r")) # Geo.json para o mapa do Brasil
#geo_data["features"][0].keys()


# Função para formatar valores a serem exibidos
def formatar_valor(valor):
    if pd.isna(valor):
        return "-"
    return str(f"{int(valor):,}".replace(",", " "))


# Padronizar cores
cores_casos = plotly.colors.sequential.OrRd[:len(estados_df['estado'].unique())]
cores_obitos = plotly.colors.sequential.Brwnyl[:len(estados_df['estado'].unique())]
cores_letalidade = plotly.colors.sequential.amp[:len(estados_df['estado'].unique())]
cores_mortalidade = plotly.colors.sequential.Burg[:len(estados_df['estado'].unique())]
cores_incidencia = plotly.colors.sequential.Redor[:len(estados_df['estado'].unique())]


# Layout do APP
app.layout=html.Div(
    [
        NavbarComponent().create_navbar(),
        OffCanvas().create_offcanvas_visao_geral(),
        OffCanvas().create_offcanvas_objetivos(),
        OffCanvas().create_offcanvas_dados(),
        OffCanvas.create_offcanvas_frameworks(),
        Content.create_content(),
        html.Br(),
        FooterComponent().create_footer(),
        ModalComponent.create_modal_incidencia(),
        ModalComponent.create_modal_letalidade(),
        ModalComponent.create_modal_mortalidade()
    ]
)


# Callback para atualizar CardTop >>> CardsInner 
@app.callback(
        Output("casos-acumulados-na-data", "children"),
        Output("novos-casos-texto", "children"),
        Output("total-recuperados", "children"),
        Output("em-acompanhamento-texto", "children"),
        Output("obitos-acumulados-na-data","children"),
        Output("novos-obitos-texto","children"),
        Output("mapa-texto", "children"),
        Input("datepicker", "date"),
)
def update_card_infos(date):
    dff = brasil_df[brasil_df["data"]==date]
    
    casos_acumulados_na_data = formatar_valor(dff["casosAcumulado"].values[0])
    novos_casos_na_data = formatar_valor(dff["casosNovos"].values[0])
    novos_casos_texto = "Novos casos na data: {}".format(novos_casos_na_data)

    recuperados = formatar_valor(dff["Recuperadosnovos"].values[0])
    em_acompanhamento = formatar_valor(dff["emAcompanhamentoNovos"].values[0])
    em_acompanhamento_texto = "Em acompanhamento: {}".format(em_acompanhamento)

    obitos_acumulados_na_data = formatar_valor(dff["obitosAcumulado"].values[0])
    novos_obitos_na_data = formatar_valor(dff["obitosNovos"].values[0])
    novos_obitos_texto = "Novos óbitos na data: {}".format(novos_obitos_na_data)
    
    
    data_formatada = pd.to_datetime(date).strftime('%d/%m/%Y')
    mapa_texto = "**Valores atualizados até a data selecionada: {}".format(data_formatada)

    return (
        casos_acumulados_na_data,
        novos_casos_texto,
        recuperados,
        em_acompanhamento_texto,
        obitos_acumulados_na_data,
        novos_obitos_texto,
        mapa_texto
    )


# Callback para filtrar o estados_df e armazená-lo no dcc.Store
@app.callback(
    Output("datepicker-store", "data"),
    Input("datepicker","date")
)
def estados_df_filter_on_date(date):
    dff_on_date = estados_df[estados_df["data"] == date]
    
    df_grouped_on_date = dff_on_date.groupby("siglaUF").agg(
        {
            "estado":"last", 
            "regiao":"last",
            "populacaoTCU2019":"max",
            "casosAcumulado":"max",
            "casosNovos":"sum",
            "obitosAcumulado":"max",
            "obitosNovos":"sum"
        }
    ).reset_index()
    
    df_grouped_on_date["incidencia"] = df_grouped_on_date["casosAcumulado"]/df_grouped_on_date["populacaoTCU2019"]*100000
    df_grouped_on_date["mortalidade"] = df_grouped_on_date["obitosAcumulado"]/df_grouped_on_date["populacaoTCU2019"]*100000       
    df_grouped_on_date["taxaLetalidade"] = df_grouped_on_date["obitosAcumulado"]/df_grouped_on_date["casosAcumulado"]*100

    return df_grouped_on_date.to_json()


# Callback para renderizar gráfico com evolução no Brasil
@app.callback(
    Output("line-chart-casos-brasil", "figure"),
    Output("line-chart-obitos-brasil", "figure"),
    Input("datepicker", "date")
)
def update_ranger_slider_br(date):
    dff_br = brasil_df[brasil_df["data"] <= date]
    #dff_br["data_formatada"]= pd.to_datetime(dff_br["data"], infer_datetime_format=True).dt.strftime("%d/%m/%Y")
        
    lines_chart_casos_br = go.Figure(
        data=[
            go.Scatter(
                x=dff_br["data"],
                y=dff_br["casosAcumulado"],
                mode="lines",
                name="Casos Acumulados",
                fill="tozeroy",
                line={"color": "#E6C1A6"},
                hovertemplate="<b>Data: %{x}</b><br>Casos Acumulados: %{y:,.0f}<extra></extra>",
            ),
            go.Scatter(
                x=dff_br["data"],
                y=dff_br["casosNovos"],
                mode="lines",
                name="Novos Casos na data",
                line={"color": "#D06450"},
                hovertemplate="<b>Data: %{x}</b><br>Novos Casos: %{y:,.0f}<extra></extra>",
            )
        ],
        layout=go.Layout(
            title=dict(text="Casos Registrados - Brasil",font=dict(color="white"), x=0.53),
            xaxis=dict(
                title=dict(text="Data", font=dict(color="white")),
                tickfont=dict(color="white"),
                rangeslider=dict(visible=True),
                gridcolor="rgba(255, 255, 255, 0.1)",
                gridwidth=0.5
            ),
            yaxis=dict(tickfont=dict(color="white"), gridcolor="rgba(255, 255, 255, 0.1)", gridwidth=0.5),
            legend=dict(x=0.5, y=0.985, xanchor="center", yanchor="bottom", orientation="h", font=dict(color="white")),
            paper_bgcolor="rgba(0, 0, 0, 0)",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            margin=dict(t=50, b=50, r=10, l=50),
            separators=", "
        )
    )

    lines_chart_obitos_br = go.Figure(
        data=[
            go.Scatter(
                x=dff_br["data"],
                y=dff_br["obitosAcumulado"],
                mode="lines",
                name="Óbitos Acumulados",
                fill="tozeroy",
                line={"color": "#30242A"},
                hovertemplate="<b>Data: %{x}</b><br>Óbitos Acumulados: %{y:,.0f}<extra></extra>",
            ),
            go.Scatter(
                x=dff_br["data"],
                y=dff_br["obitosNovos"],
                mode="lines",
                name="Novos Óbitos na data",
                line={"color": "#972930"},
                hovertemplate="<b>Data: %{x}</b><br>Novos Óbitos: %{y:,.0f}<extra></extra>",
            )
        ],
        layout=go.Layout(
            title=dict(text="Óbitos Registrados - Brasil", font=dict(color="white"), x=0.54),
            xaxis=dict(
                title=dict(text="Data", font=dict(color="white")),
                tickfont=dict(color="white"),
                rangeslider=dict(visible=True),
                gridcolor="rgba(255, 255, 255, 0.1)",
                gridwidth=0.5
            ),
            yaxis=dict(tickfont=dict(color="white"), gridcolor="rgba(255, 255, 255, 0.1)", gridwidth=0.5),
            legend=dict(x=0.5, y=0.985, xanchor="center", yanchor="bottom", orientation="h", font=dict(color="white")),
            paper_bgcolor="rgba(0, 0, 0, 0)",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            margin=dict(t=50, b=50, r=10, l=50),
            separators=", "
        )
    )

    return lines_chart_casos_br, lines_chart_obitos_br


# Callback para renderizar gráficos com distibuição de frequência por macroregião
@app.callback(
    Output("subplots-macroregion", "figure"),
    Input("datepicker-store","data")
)
def update_subplots(json_data):
    dff = pd.read_json(json_data)
    dff_macro = dff.groupby("regiao").agg({"casosAcumulado":"sum","obitosAcumulado":"sum"}).reset_index()

    subplots_macroregion = make_subplots(
        rows=1, cols=2, 
        specs=[[{"type":"domain"}, {"type":"domain"}]],
        vertical_spacing=0.01,
        horizontal_spacing=0.01
    )
    
    pie_chart_casos = go.Pie(
        labels=dff_macro.sort_values("casosAcumulado", ascending=True)["regiao"], 
        values=dff_macro.sort_values("casosAcumulado", ascending=True)["casosAcumulado"], 
        marker=dict(colors=cores_casos, line=dict(color="white", width=1)),
        pull=[0,0,0,0,0.05],
        texttemplate="%{label}"+"<br>%{percent}",
        textposition="inside",
        hovertemplate = "<b>Macroregião " + dff_macro.sort_values("casosAcumulado", ascending=True)["regiao"] + 
                        "</b><br>Casos Acumulados: %{value}"
                        "<br></b>Percentual: %{percent}<extra></extra>"
    )
    subplots_macroregion.add_trace(pie_chart_casos, row=1, col=1)
    
    pie_chart_obitos = go.Pie(
        labels=dff_macro.sort_values("obitosAcumulado", ascending=True)["regiao"], 
        values=dff_macro.sort_values("obitosAcumulado", ascending=True)["obitosAcumulado"], 
        marker=dict(colors=cores_obitos, line=dict(color="white", width=1)),
        pull=[0,0,0,0,0.05],
        texttemplate="%{label}"+"<br>%{percent}",
        textposition="inside",
        hovertemplate = "<b>Macroregião " + dff_macro.sort_values("obitosAcumulado", ascending=True)["regiao"] + 
                        "</b><br>Óbitos Acumulados: %{value}"
                        "<br>Percentual: %{percent}<extra></extra>"
    )
    subplots_macroregion.add_trace(pie_chart_obitos, row=1, col=2)
    
    subplots_macroregion.update_layout(
        title_text = "Distribuição de Casos e Óbitos<br>Acumulados por Macroregião",
        title_font=dict(color="white"),
        title_x=0.5,
        title_y=0.95,
        plot_bgcolor="rgba(0, 0, 0, 0)", 
        paper_bgcolor="rgba(0, 0, 0, 0)", 
        margin=dict(t=0, b=0, l=0, r=0), 
        showlegend=False,
        separators=", "
    )
    

    return subplots_macroregion


# Callback para cria gráfico de barras filtrado por data e macroregiao
@app.callback(
    Output("macroregiao-texto", "children"),
    Output("badge-texto", "children"),
    Output("bar-chart-macroregion", "figure"),
    Input("dropdown-macroregion", "value"),
    Input("dropdown-map","value"),
    Input("datepicker-store", "data")
)
def update_bar_chart_macroregion(dropdown_macroregion_v, dropdown_map_v, json_data):
    dff = pd.read_json(json_data)
    dff_macro = dff[dff["regiao"]==dropdown_macroregion_v]

    if dropdown_map_v == "casosAcumulado":
        macro_title = "Casos Acumulados - {}".format(dropdown_macroregion_v)
        badge_str = "Total: {}".format(formatar_valor(dff_macro["casosAcumulado"].sum()))

        bar_chart = go.Figure(
            data=go.Bar(
                x=dff_macro.sort_values("casosAcumulado", ascending=True)["siglaUF"],
                y=dff_macro.sort_values("casosAcumulado", ascending=True)["casosAcumulado"],
                marker=dict(color=cores_casos, line=dict(color="white", width=1)),
                hovertemplate = "<b>" + dff_macro.sort_values("casosAcumulado", ascending=True)["estado"] +
                                "</b><br>Casos Acumulados: %{y:,.0f}<extra></extra>",
                customdata=dff_macro.sort_values("casosAcumulado", ascending=True)["siglaUF"]
            ),
            layout=go.Layout(
                xaxis=dict(
                    title=dict(
                        text="Estados",
                        font=dict(color="white")
                    ),
                    tickfont=dict(color="white")
                ),
                yaxis=dict(
                    title=dict(
                        text="Casos Acumulados",
                        font=dict(color="white")
                    ),
                    tickfont=dict(color="white"),
                    gridcolor="rgba(255, 255, 255, 0.1)",
                    gridwidth=0.5
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=0, b=50, r=10, l=50),
                showlegend=False,
                separators=", "
            )
        )

    if dropdown_map_v == "obitosAcumulado":
        macro_title = "Óbitos Acumulados - {}".format(dropdown_macroregion_v)
        badge_str = "Total: {}".format(formatar_valor(dff_macro["obitosAcumulado"].sum()))

        bar_chart = go.Figure(
        data=go.Bar(
            x=dff_macro.sort_values("obitosAcumulado", ascending=True)["siglaUF"],
            y=dff_macro.sort_values("obitosAcumulado", ascending=True)["obitosAcumulado"],
            marker=dict(color=cores_obitos, line=dict(color="white", width=1)),
            hovertemplate = "<b>" + dff_macro.sort_values("obitosAcumulado", ascending=True)["estado"] +
                            "</b><br>Óbitos Acumulados: %{y:,.0f}<extra></extra>",
            customdata=dff_macro.sort_values("obitosAcumulado", ascending=True)["siglaUF"]
        ),
        layout=go.Layout(
            xaxis=dict(
                title=dict(
                    text="Estados",
                    font=dict(color="white")
                ),
                tickfont=dict(color="white")
            ),
            yaxis=dict(
                title=dict(
                    text="Óbitos Acumulados",
                    font=dict(color="white")
                ),
                tickfont=dict(color="white"),
                gridcolor="rgba(255, 255, 255, 0.1)",
                gridwidth=0.5
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=0, b=50, r=10, l=50),
            showlegend=False,
            separators=", "
        )
    )

    if dropdown_map_v == "incidencia":
        macro_title = "Incidência - {}".format(dropdown_macroregion_v)
        badge_str = "Incidência Média: {:.2f}".format(dff_macro["incidencia"].mean()).replace(".", ",")

        bar_chart = go.Figure(
            data=go.Bar(
                x=dff_macro.sort_values("incidencia", ascending=True)["siglaUF"],
                y=dff_macro.sort_values("incidencia", ascending=True)["incidencia"],
                marker=dict(color=cores_incidencia, line=dict(color="white", width=1)),
                text=[str(round(y, 2)).replace(".", ",") for y in dff_macro.sort_values("incidencia", ascending=True)["incidencia"]],
                hovertemplate = "<b>" + dff_macro.sort_values("incidencia", ascending=True)["estado"] +
                                "</b><br>incidencia: %{y:.2f}<extra></extra>",
                customdata=dff_macro.sort_values("incidencia", ascending=True)["siglaUF"]
            ),
            layout=go.Layout(
                xaxis=dict(
                    title=dict(
                        text="Estados",
                        font=dict(color="white")
                    ),
                    tickfont=dict(color="white")
                ),
                yaxis=dict(
                    title=dict(
                        text="Incidência",
                        font=dict(color="white")
                    ),
                    tickfont=dict(color="white"),
                    gridcolor="rgba(255, 255, 255, 0.1)",
                    gridwidth=0.5
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=0, b=50, r=10, l=50),
                showlegend=False,
                separators=",."
            )
        )
        
        bar_chart.add_trace(
            go.Scatter(
                x=dff_macro["siglaUF"],
                y=[dff_macro["incidencia"].mean()] * len(dff_macro),
                mode="lines",
                line=dict(color="white", dash="dashdot"),
                hovertemplate="<b>{}</b><extra></extra>".format(badge_str)
            )
        )

    if dropdown_map_v == "mortalidade":
        macro_title = "Mortalidade - {}".format(dropdown_macroregion_v)
        badge_str = "Mortalidade Média: {:.2f}".format(dff_macro["mortalidade"].mean()).replace(".", ",")

        bar_chart = go.Figure(
            data=go.Bar(
                x=dff_macro.sort_values("mortalidade", ascending=True)["siglaUF"],
                y=dff_macro.sort_values("mortalidade", ascending=True)["mortalidade"],
                marker=dict(color=cores_mortalidade, line=dict(color="white", width=1)),
                text=[str(round(y, 2)).replace(".", ",") for y in dff_macro.sort_values("mortalidade", ascending=True)["mortalidade"]],
                hovertemplate = "<b>" + dff_macro.sort_values("mortalidade", ascending=True)["estado"] +
                                "</b><br>Mortalidade: %{y:.2f}<extra></extra>",
                customdata=dff_macro.sort_values("mortalidade", ascending=True)["siglaUF"]
            ),
            layout=go.Layout(
                xaxis=dict(
                    title=dict(
                        text="Estados",
                        font=dict(color="white")
                    ),
                    tickfont=dict(color="white")
                ),
                yaxis=dict(
                    title=dict(
                        text="Mortalidade",
                        font=dict(color="white")
                    ),
                    tickfont=dict(color="white"),
                    gridcolor="rgba(255, 255, 255, 0.1)",
                    gridwidth=0.5
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=0, b=50, r=10, l=50),
                showlegend=False,
                separators=",."
            )
        )
        
        bar_chart.add_trace(
            go.Scatter(
                x=dff_macro["siglaUF"],
                y=[dff_macro["mortalidade"].mean()] * len(dff_macro),
                mode="lines",
                line=dict(color="white", dash="dashdot"),
                hovertemplate="<b>{}</b><extra></extra>".format(badge_str)
            )
        )

    if dropdown_map_v == "taxaLetalidade":
        macro_title = "Taxa de Letalidade - {}".format(dropdown_macroregion_v)
        badge_str = "Taxa de Letalidade Média: {:.2f} %".format(dff_macro["taxaLetalidade"].mean()).replace(".", ",")

        bar_chart = go.Figure(
            data=go.Bar(
                x=dff_macro.sort_values("taxaLetalidade", ascending=True)["siglaUF"],
                y=dff_macro.sort_values("taxaLetalidade", ascending=True)["taxaLetalidade"],
                marker=dict(color=cores_letalidade, line=dict(color="white", width=1)),
                text=[str(round(y, 2)).replace(".", ",") + "%" for y in dff_macro.sort_values("taxaLetalidade", ascending=True)["taxaLetalidade"]],
                hovertemplate = "<b>" + dff_macro.sort_values("taxaLetalidade", ascending=True)["estado"] +
                                "</b><br>Taxa de Letalidade: %{y:.2f} %<extra></extra>",
                customdata=dff_macro.sort_values("taxaLetalidade", ascending=True)["siglaUF"]
            ),
            layout=go.Layout(
                xaxis=dict(
                    title=dict(
                        text="Estados",
                        font=dict(color="white")
                    ),
                    tickfont=dict(color="white")
                ),
                yaxis=dict(
                    title=dict(
                        text="Taxa de Letalidade*",
                        font=dict(color="white")
                    ),
                    tickfont=dict(color="white"),
                    gridcolor="rgba(255, 255, 255, 0.1)",
                    gridwidth=0.5
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=0, b=50, r=10, l=50),
                showlegend=False,
                separators=",."
            )
        )
        
        bar_chart.add_trace(
            go.Scatter(
                x=dff_macro["siglaUF"],
                y=[dff_macro["taxaLetalidade"].mean()] * len(dff_macro),
                mode="lines",
                line=dict(color="red", dash="dashdot"),
                hovertemplate="<b>{}</b><extra></extra>".format(badge_str)
            )
        )

    return macro_title, badge_str, bar_chart


# Callback para renderizar o mapa do Brasil
# @app.callback(
#     Output("map-chart", "figure"),
#     Input("dropdown-map", "value"),
#     Input("datepicker-store", "data"),
# )
# def update_map(dropdown_map_v, json_data):
#     dff = pd.read_json(json_data)
        
#     if dropdown_map_v == "casosAcumulado":
#         z_max = int(dff["casosAcumulado"].max())
#         colors = cores_casos 
#         hover_template = ("<b>%{location}</b>"
#                           "<br><span style='color:Gold'><b>Casos Acumulados</b>: %{customdata[0]:.0f}</span>"
#                           "<br>Novos casos no dia: %{customdata[1]:.0f}<extra></extra>"
#         ) 
#         custom_data = dff[["casosAcumulado","casosNovos"]]

#     if dropdown_map_v == "obitosAcumulado":
#         z_max = int(dff["obitosAcumulado"].max())
#         colors = cores_obitos
#         hover_template = ("<b>%{location}</b><br>"
#                           "<br><span style='color:OrangeRed'><b>Óbitos Acumulados:</b> %{customdata[0]:.0f}</span>"
#                           "<br>Óbitos registrados no dia: %{customdata[1]:.0f}<extra></extra>"
#         )
#         custom_data=dff[["obitosAcumulado", "obitosNovos"]]

#     if dropdown_map_v == "incidencia":
#         z_max = float(dff["incidencia"].max())
#         colors = cores_incidencia
#         hover_template = ("<b>%{location}</b>"
#                           "<br>Casos Acumulados: %{customdata[0]:.0f}"
#                           "<br>População Total: %{customdata[1]:.0f}"
#                           "<br><span style='color:red'><b>Incidência</b>: %{customdata[2]:.2f}</span><extra></extra>"
#         )
#         custom_data=dff[["casosAcumulado","populacaoTCU2019", "incidencia"]]

#     if dropdown_map_v == "mortalidade":
#         z_max = float(dff["mortalidade"].max())
#         colors = cores_mortalidade
#         hover_template = ("<b>%{location}</b>"
#                           "<br>Óbitos Acumulados: %{customdata[0]:.0f}"
#                           "<br>População Total: %{customdata[1]:.0f}"
#                           "<br><span style='color:red'><b>Mortalidade*</b>: %{customdata[2]:.2f}</span><extra></extra>"
#         )
#         custom_data=dff[["obitosAcumulado","populacaoTCU2019", "mortalidade"]]

#     if dropdown_map_v == "taxaLetalidade":
#         z_max = float(dff["taxaLetalidade"].max())
#         colors = cores_letalidade
#         hover_template = ("<b>%{location}</b>"
#                           "<br>Casos Acumulados: %{customdata[0]:.0f}"
#                           "<br>Óbitos Acumulados: %{customdata[1]:.0f}"
#                           "<br><span style='color:red'><b>Taxa de Letalidade*</b>: %{customdata[2]:.2f} %</span><extra></extra>"
#         )
#         custom_data=dff[["casosAcumulado", "obitosAcumulado", "taxaLetalidade"]]

#     map_chart = go.Figure(
#         go.Choroplethmapbox(
#             geojson=geo_data,
#             locations=dff["siglaUF"],
#             z=dff[dropdown_map_v],
#             colorscale=colors,
#             zmin=0,
#             zmax=z_max,
#             marker_opacity=0.7,
#             marker_line_width=0.5,
#             hovertemplate=hover_template,
#             customdata=custom_data
#         )
#     )
#     map_chart.update_layout(
#         mapbox_style="carto-positron",
#         mapbox_zoom=2.75,
#         mapbox_center={"lat": -17, "lon": -55},
#         margin={"r": 0, "l": 0, "t": 0, "b": 0}
#     )
    
    return map_chart


# Callback para o toggle da navbar em telas menores
@app.callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open"),
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# Callbacks para abrir/registrar Offcanvas (Visão Geral, Objetivos, Frameworks, Dados)
def register_offcanvas_callback(open_id, open_id_footer, offcanvas_id):
    @app.callback(
        Output(offcanvas_id, "is_open"),
        Input(open_id, "n_clicks"),
        Input(open_id_footer, "n_clicks"),
        State(offcanvas_id, "is_open"),
        allow_duplicate=True # Acessível da navbar e do footer
    )
    def toggle_offcanvas_visibility(n_clicks, n_clicks_footer, is_open):
        if ctx.triggered:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]
            if button_id == open_id:
                return not is_open
            elif button_id == open_id_footer:
                return not is_open
        return is_open

register_offcanvas_callback("open-visaoGeral", "open-visaoGeral-footer", "offcanvas-visaoGeral")
register_offcanvas_callback("open-objetivos", "open-objetivos-footer", "offcanvas-objetivos")
register_offcanvas_callback("open-frameworks", "open-frameworks-footer", "offcanvas-frameworks")
register_offcanvas_callback("open-dados", "open-dados-footer", "offcanvas-dados")


# Callbacks para abrir/registrar Modal´s (Incidência, Letalidade, Mortalidade)
def register_modal_callback(open_id, modal_id):
    @app.callback(
        Output(modal_id, "is_open"),
        Input(open_id, "n_clicks"),
        State(modal_id, "is_open")
    )
    def toggle_modal_visibility(n_clicks, is_open):
        if ctx.triggered:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]
            if button_id == open_id:
                return not is_open
        return is_open

register_modal_callback("open-incidencia","modal-incidencia")
register_modal_callback("open-letalidade","modal-letalidade")
register_modal_callback("open-mortalidade","modal-mortalidade")


# Iniciar o servidor do aplicativo Dash
if __name__ == "__main__": 
    app.run_server(debug=True)
   