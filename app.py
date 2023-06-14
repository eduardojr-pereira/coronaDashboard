from templates.navbar_component import NavbarComponent, OffCanvas
from templates.content_component import Content
from templates.footer_component import FooterComponent, ModalComponent
from dash import ctx, Dash, html, Input, Output, State 
from plotly.subplots import make_subplots
import plotly.colors 
import plotly.graph_objects as go
import plotly.express as px
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
cores_incidencia = plotly.colors.sequential.amp[:len(estados_df['estado'].unique())]
cores_mortalidade = plotly.colors.sequential.Burg[:len(estados_df['estado'].unique())]
cores_letalidade = plotly.colors.sequential.Redor[:len(estados_df['estado'].unique())]


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
        Output("last-update-texto", "children"),
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
    mapa_texto = "Valores atualizados até a data selecionada: {}".format(data_formatada)
    last_update_texto = "Última atualização {}".format(pd.to_datetime(brasil_df["data"].max()).strftime("%d/%m/%Y"))

    return (
        casos_acumulados_na_data,
        novos_casos_texto,
        recuperados,
        em_acompanhamento_texto,
        obitos_acumulados_na_data,
        novos_obitos_texto,
        mapa_texto,
        last_update_texto
    )


# Callback para filtrar/agrupar o dataframe estados_df e armazená-lo no dcc.Store
@app.callback(
    Output("datepicker-store-states", "data"),
    Output("datepicker-store-macroregion", "data"),
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

    df_macroregion = df_grouped_on_date.groupby("regiao").agg(
        {
            "casosAcumulado":"sum",
            "obitosAcumulado":"sum",
            "populacaoTCU2019":"sum",
        }
    ).reset_index() 

    df_macroregion["incidencia"] = df_macroregion["casosAcumulado"]/df_macroregion["populacaoTCU2019"]*100000
    df_macroregion["mortalidade"] = df_macroregion["obitosAcumulado"]/df_macroregion["populacaoTCU2019"]*100000       
    df_macroregion["taxaLetalidade"] = df_macroregion["obitosAcumulado"]/df_macroregion["casosAcumulado"]*100

    return df_grouped_on_date.to_json(), df_macroregion.to_json()


# Callback para renderizar gráfico com evolução no Brasil
@app.callback(
    Output("line-chart-casos-brasil", "figure"),
    Output("line-chart-obitos-brasil", "figure"),
    Input("datepicker", "date")
)
def update_ranger_slider_br(date):
    dff_br = brasil_df[brasil_df["data"] <= date]
            
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


# Callback para renderizar gráficos com dados agrupados por macroregião
@app.callback(
    Output("macroregion-chart", "figure"),
    Input("dropdown-map", "value"),
    Input("datepicker-store-macroregion","data")
)
def update_subplots(dropdown_map_v, json_data):
    dff = pd.read_json(json_data)
    
    if dropdown_map_v == "casosAcumulado":
        title_temp="Casos Acumulados por Macroregião"
        subplots_macroregion=go.Figure(
            go.Pie(
                labels=dff.sort_values("casosAcumulado", ascending=True)["regiao"], 
                values=dff.sort_values("casosAcumulado", ascending=True)["casosAcumulado"], 
                marker=dict(colors=cores_casos, line=dict(color="white", width=1)),
                pull=[0,0,0,0,0.05],
                texttemplate="%{label}"+"<br>%{percent}",
                textposition="inside",
                hovertemplate = "<b>Macroregião " + dff.sort_values("casosAcumulado", ascending=True)["regiao"] + 
                                "</b><br>Casos Acumulados: %{value}"
                                "<br></b>Percentual: %{percent}<extra></extra>"
            )
        )

    if dropdown_map_v == "obitosAcumulado": 
        title_temp="Óbitos Acumulados por Macroregião"
        subplots_macroregion=go.Figure(
            go.Pie(
                labels=dff.sort_values("obitosAcumulado", ascending=True)["regiao"], 
                values=dff.sort_values("obitosAcumulado", ascending=True)["obitosAcumulado"], 
                marker=dict(colors=cores_obitos, line=dict(color="white", width=1)),
                pull=[0,0,0,0,0.05],
                texttemplate="%{label}"+"<br>%{percent}",
                textposition="inside",
                hovertemplate = "<b>Macroregião " + dff.sort_values("obitosAcumulado", ascending=True)["regiao"] + 
                                "</b><br>Óbitos Acumulados: %{value}"
                                "<br>Percentual: %{percent}<extra></extra>"
            )
        )
    
    if dropdown_map_v == "incidencia":
        title_temp="Incidência por Macroregião<br>(cada 100 mil habitantes)"
        subplots_macroregion=px.scatter(
            dff,
            x="populacaoTCU2019",
            y="casosAcumulado",
            size="casosAcumulado",
            color="incidencia",
            log_x=True,
            log_y=True,
            size_max=60
        )
        subplots_macroregion.update_layout(
            xaxis=dict(title=dict(text="População - 2019"), gridcolor="rgba(255, 255, 255, 0.1)", gridwidth=0.5),
            yaxis=dict(title=dict(text="Casos Acumulados"), gridcolor="rgba(255, 255, 255, 0.1)", gridwidth=0.5),
            coloraxis=dict(colorbar=dict(title=dict(text="Incidência"), bgcolor="rgba(0,0,0,0)", outlinewidth=0))
        )
        subplots_macroregion.update_traces(
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "População: %{customdata[1]:,.0f}<br>"
                "Casos: %{customdata[2]:,.0f}<br>"
                "Incidência: %{customdata[3]:,.2f}<extra></extra>"
            ),
            customdata=dff[["regiao","populacaoTCU2019","casosAcumulado","incidencia"]]
        )

    if dropdown_map_v == "mortalidade":
        title_temp="Mortalidade por Macroregião<br>(cada 100 mil habitantes)"
        
        
    if dropdown_map_v == "taxaLetalidade":
        title_temp="Taxa de Letalidade por Macroregião"
        subplots_macroregion=go.Figure(
            go.Barpolar(
                r=dff.sort_values("taxaLetalidade", ascending=True)["taxaLetalidade"],
                theta=dff.sort_values("taxaLetalidade", ascending=True)["regiao"],
                marker=dict(color=cores_letalidade, line=dict(color="white", width=1)),
                hovertemplate = "<b>Macroregião %{customdata[0]}</b><br>"+ 
                                "Casos Acumulados: %{customdata[1]:,.0f}<br>"+
                                "Óbitos Acumulados: %{customdata[2]:,.0f}<br>"+
                                "Taxa de Letalidade: %{customdata[3]:,.2f}%<br><extra></extra>",
                customdata=dff[["regiao","casosAcumulado","obitosAcumulado","taxaLetalidade"]]
            )
        )
        subplots_macroregion.update_layout(
            polar=dict(
                radialaxis=dict(gridcolor="#515960", gridwidth=0.5, griddash="dashdot"),
                bgcolor="rgba(0,0,0,0)"
            )
        )

    subplots_macroregion.update_layout(
            font=dict(color="white"),
            plot_bgcolor="rgba(0, 0, 0, 0)", 
            paper_bgcolor="rgba(0, 0, 0, 0)", 
            margin=dict(t=50, b=50, l=0, r=0), 
            showlegend=False,
            separators=", ",
            title=dict(text=title_temp, x=0.5)
        )

    return subplots_macroregion


# Callback para renderizar gráficos com dados filtrados por macroregião
@app.callback(
    Output("subplots-states", "figure"),
    Input("dropdown-macroregion", "value"),
    Input("dropdown-map","value"),
    Input("datepicker-store-states", "data")
)
def update_bar_chart_macroregion(dropdown_macroregion_v, dropdown_map_v, json_data):
    dff = pd.read_json(json_data)
    dff_macro = dff[dff["regiao"]==dropdown_macroregion_v]
    
    if dropdown_map_v == "casosAcumulado":
        subplots_estados=go.Figure(
            go.Bar(
                x=dff_macro.sort_values("casosAcumulado", ascending=True)["siglaUF"],
                y=dff_macro.sort_values("casosAcumulado", ascending=True)["casosAcumulado"],
                marker=dict(color=cores_casos, line=dict(color="white", width=1)),
                texttemplate="%{y:,.0f}",
                hovertemplate = "<b>" + dff_macro.sort_values("casosAcumulado", ascending=True)["estado"] +
                                "</b><br>Casos Acumulados: %{y:,.0f}<extra></extra>",
                customdata=dff_macro.sort_values("casosAcumulado", ascending=True)["siglaUF"]
            )
        )
        subplots_estados.update_layout(
            title=dict(text=f"Casos Acumulados por Estados - {dropdown_macroregion_v}", x=0.5),
            xaxis=dict(title="Estados"),
            yaxis=dict(title="Casos Acumulados",gridcolor="rgba(255, 255, 255, 0.1)", gridwidth=0.5, griddash="dashdot")
        )

    if dropdown_map_v == "obitosAcumulado":
        subplots_estados=go.Figure(
            go.Bar(
                x=dff_macro.sort_values("obitosAcumulado", ascending=True)["siglaUF"],
                y=dff_macro.sort_values("obitosAcumulado", ascending=True)["obitosAcumulado"],
                marker=dict(color=cores_obitos, line=dict(color="white", width=1)),
                texttemplate="%{y:,.0f}",
                hovertemplate = "<b>" + dff_macro.sort_values("obitosAcumulado", ascending=True)["estado"] +
                                "</b><br>Óbitos Acumulados: %{y:,.0f}<extra></extra>",
                customdata=dff_macro.sort_values("obitosAcumulado", ascending=True)["siglaUF"]
            )
        )
        subplots_estados.update_layout(
            title=dict(text=f"Óbitos Acumulados por Estados - {dropdown_macroregion_v}", x=0.5),
            xaxis=dict(title="Estados"),
            yaxis=dict(title="Óbitos Acumulados",gridcolor="rgba(255, 255, 255, 0.1)", gridwidth=0.5, griddash="dashdot")
        )
        
    if dropdown_map_v == "incidencia":
        subplots_estados=px.scatter(
            dff_macro,
            x="populacaoTCU2019",
            y="casosAcumulado",
            size="casosAcumulado",
            color="incidencia",
            log_x=True,
            log_y=True,
            size_max=60  
        )
        subplots_estados.update_layout(
            title=dict(text=f"Incidência por Estados - {dropdown_macroregion_v}<br>(cada 100 mil habitantes)", x=0.5),
            xaxis=dict(title="População - 2019", gridcolor="rgba(255, 255, 255, 0.1)", gridwidth=0.5),
            yaxis=dict(title="Casos Acumulados", gridcolor="rgba(255, 255, 255, 0.1)", gridwidth=0.5),
            coloraxis=dict(colorbar=dict(title=dict(text="Incidência"),bgcolor="rgba(0,0,0,0)",outlinewidth=0))
        )
        subplots_estados.update_traces(
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "População: %{customdata[1]:,.0f}<br>"
                "Casos: %{customdata[2]:,.0f}<br>"
                "Incidência: %{customdata[3]:,.2f}<extra></extra>"
            ),
            customdata=dff_macro[["estado","populacaoTCU2019","casosAcumulado","incidencia"]]
        )
        
    if dropdown_map_v == "mortalidade":
        subplots_estados=px.scatter(
            dff_macro,
            x="populacaoTCU2019",
            y="obitosAcumulado",
            size="obitosAcumulado",
            color="mortalidade",
            color_continuous_scale=cores_mortalidade,
            log_x=True,
            log_y=True,
            size_max=60
        )
        subplots_estados.update_layout(
            title=dict(text=f"Mortalidade por Estados - {dropdown_macroregion_v}<br>(cada 100 mil habitantes)", x=0.5),
            xaxis=dict(title="População - 2019", gridcolor="rgba(255, 255, 255, 0.1)", gridwidth=0.5),
            yaxis=dict(title="Óbitos Acumulados", gridcolor="rgba(255, 255, 255, 0.1)", gridwidth=0.5),
            coloraxis=dict(colorbar=dict(title=dict(text="Mortalidade"),bgcolor="rgba(0,0,0,0)",outlinewidth=0))
        )
        subplots_estados.update_traces(
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>" 
                "População: %{customdata[1]:,.0f}<br>"
                "Obitos: %{customdata[2]:,.0f}<br>"
                "Mortalidade: %{customdata[3]:,.2f}<extra></extra>"
            ),
            customdata=dff_macro[["estado","populacaoTCU2019","obitosAcumulado","mortalidade"]]
        )
  
    if dropdown_map_v == "taxaLetalidade":
        subplots_estados=go.Figure(
            go.Barpolar(
                r=dff_macro.sort_values("taxaLetalidade", ascending=True)["taxaLetalidade"],
                theta=dff_macro.sort_values("taxaLetalidade", ascending=True)["estado"],
                marker=dict(color=cores_letalidade, line=dict(color="white", width=1)),
                hovertemplate = "<b>%{customdata[0]}</b><br>" 
                                "Casos Acumulados: %{customdata[1]:,.0f}<br>"
                                "Óbitos Acumulados: %{customdata[2]:,.0f}<br>"
                                "Taxa de Letalidade: %{customdata[3]:,.2f}%<br><extra></extra>",
                customdata=dff_macro[["estado","casosAcumulado","obitosAcumulado","taxaLetalidade"]]
            )
        )
        subplots_estados.update_layout(
            title=dict(text=f"Letalidade por Estados - {dropdown_macroregion_v}", x=0.5),
            polar=dict(
                radialaxis=dict(gridcolor="#515960", gridwidth=0.5, griddash="dashdot"),
                bgcolor="rgba(0,0,0,0)"
            )
        )

    subplots_estados.update_layout(
        font=dict(color="white"),
        plot_bgcolor="rgba(0, 0, 0, 0)", 
        paper_bgcolor="rgba(0, 0, 0, 0)", 
        margin=dict(t=50, b=50, l=0, r=0), 
        showlegend=False,
        separators=", ",
    )
    return subplots_estados


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
   