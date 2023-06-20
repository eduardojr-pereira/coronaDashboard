from templates.navbar_component import NavbarComponent, OffCanvas
from templates.content_component import Content
from templates.footer_component import FooterComponent, ModalComponent
from dash import Dash, html, Input, Output, State, ctx 
from flask_caching import Cache
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
geo_data = json.load(open("data/raw/brasilGeo.json", "r")) 


# Padronizar cores
cores_casos = plotly.colors.sequential.OrRd[:len(estados_df['estado'].unique())]
cores_obitos = plotly.colors.sequential.Brwnyl[:len(estados_df['estado'].unique())]
cores_incidencia = plotly.colors.sequential.Burg[:len(estados_df['estado'].unique())]
cores_mortalidade = plotly.colors.sequential.amp[:len(estados_df['estado'].unique())]
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
        ModalComponent.create_modal_gini(),
        ModalComponent.create_modal_palma(),
        ModalComponent.create_modal_incidencia(),
        ModalComponent.create_modal_mortalidade(),
        ModalComponent.create_modal_letalidade()
    ]
)


# Callback para atualizar CardTop >>> CardsInner 
# Atualizar informações da primeira Card logo abaixo do Header
@app.callback(
        Output("casos-acumulados-na-data", "children"),
        Output("novos-casos-texto", "children"),
        Output("total-recuperados", "children"),
        Output("em-acompanhamento-texto", "children"),
        Output("obitos-acumulados-na-data","children"),
        Output("novos-obitos-texto","children"),
        Output("last-update-texto", "children"),
        Input("datepicker", "date"),
)
def update_card_infos(date):
    dff = brasil_df[brasil_df["data"]==date]
    # Função para formatar valores a serem exibidos
    def formatar_valor(valor):
        if pd.isna(valor):
            return "-"
        return str(f"{int(valor):,}".replace(",", " "))


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
    last_update_texto = "Última atualização {}".format(pd.to_datetime(brasil_df["data"].max()).strftime("%d/%m/%Y"))

    return (
        casos_acumulados_na_data,
        novos_casos_texto,
        recuperados,
        em_acompanhamento_texto,
        obitos_acumulados_na_data,
        novos_obitos_texto,
        last_update_texto
    )


# Callback para filtrar/agrupar dados e armazenás-lo no dcc.Store
@app.callback(
    Output("store-states-on-date", "data"),
    Output("store-macroregion-on-date", "data"),
    Input("datepicker","date")
)
def filter_on_date(date):
    dff_on_date = estados_df[estados_df["data"] == date]
    
    dff_states_on_date = dff_on_date.groupby("siglaUF").agg(
        {
            "estado":"last", 
            "regiao":"last",
            "populacaoTCU2019":"max",
            "casosAcumulado":"max",
            "obitosAcumulado":"max",
            "casosNovos":"sum",
            "obitosNovos":"sum"
        }
    ).reset_index()
    dff_states_on_date["incidencia"] = dff_states_on_date["casosAcumulado"]/dff_states_on_date["populacaoTCU2019"]*100000
    dff_states_on_date["mortalidade"] = dff_states_on_date["obitosAcumulado"]/dff_states_on_date["populacaoTCU2019"]*100000       
    dff_states_on_date["taxaLetalidade"] = dff_states_on_date["obitosAcumulado"]/dff_states_on_date["casosAcumulado"]*100

    df_macroregion = dff_states_on_date.groupby("regiao")[["casosAcumulado","obitosAcumulado","populacaoTCU2019"]].agg(sum).reset_index() 
    df_macroregion["incidencia"] = df_macroregion["casosAcumulado"]/df_macroregion["populacaoTCU2019"]*100000
    df_macroregion["mortalidade"] = df_macroregion["obitosAcumulado"]/df_macroregion["populacaoTCU2019"]*100000       
    df_macroregion["taxaLetalidade"] = df_macroregion["obitosAcumulado"]/df_macroregion["casosAcumulado"]*100   

    return dff_states_on_date.to_json(), df_macroregion.to_json()


# Callback para renderizar gráficos da evolução da pandemia no Brasil 
# Casos e Óbitos (novos e acumulados) generalizados para o Brasil
@app.callback(
    Output("line-chart-casos-br", "figure"),
    Output("line-chart-obitos-br", "figure"),
    Input("datepicker", "date")
)
def update_ranger_slider_br(date):
    dff_br = brasil_df[brasil_df["data"] <= date]
            
    lines_casos_br, lines_obitos_br = go.Figure(), go.Figure()

    lines_casos_br.add_trace(
        go.Scatter(
                x=dff_br["data"],
                y=dff_br["casosAcumulado"],
                mode="lines",
                name="Casos Acumulados",
                fill="tozeroy",
                line=dict(color="#E6C1A6"),
                hovertemplate="Casos Acumulados: %{y:,.0f}<extra></extra>",
        )
    )
    lines_casos_br.add_trace(
        go.Scatter(
                x=dff_br["data"],
                y=dff_br["casosNovos"],
                mode="lines",
                name="Novos Casos na data",
                line=dict(color="#D06450"),
                hovertemplate="Novos Casos: %{y:,.0f}<extra></extra>",
        )
    )
    
    lines_obitos_br.add_trace(
        go.Scatter(
                x=dff_br["data"],
                y=dff_br["obitosAcumulado"],
                mode="lines",
                name="Óbitos Acumulados",
                fill="tozeroy",
                line=dict(color="#972930"),
                hovertemplate="Óbitos Acumulados: <b>%{y:,.0f}</b><extra></extra>"
        )
    )
    lines_obitos_br.add_trace(
        go.Scatter(
                x=dff_br["data"],
                y=dff_br["obitosNovos"],
                mode="lines",
                name="Novos Óbitos na data",
                line=dict(color="#30242A"),
                hovertemplate="Novos Óbitos: %{y:,.0f}<extra></extra>"
        )
    )

    layout_config = {
        "font": {"color": "white"},
        "xaxis": {"title": "Data", "rangeslider": {"visible": True}, "gridcolor": "rgba(255, 255, 255, 0.1)", "gridwidth": 0.5},
        "yaxis": {"gridcolor": "rgba(255, 255, 255, 0.1)", "gridwidth": 0.5},
        "legend": {"x": 0.5, "y": 0.985, "xanchor": "center", "yanchor": "bottom", "orientation": "h"},
        "margin": {"t": 50, "b": 50, "r": 10, "l": 50},
        "hoverlabel":{"bgcolor":"#515960"},
        "hovermode": "x unified",
        "paper_bgcolor": "rgba(0, 0, 0, 0)",
        "plot_bgcolor": "rgba(0, 0, 0, 0)",
        "separators": ", "
    }
    
    lines_casos_br.update_layout(
        title=dict(text="Evolução dos Casos Registrados - Brasil", x=0.53),
        **layout_config
    )
    lines_obitos_br.update_layout(
        title=dict(text="Evolução dos Óbitos Registrados - Brasil", x=0.53),
        **layout_config
    )
    
    return lines_casos_br, lines_obitos_br


# Callback para renderizar gráficos com dados agrupados por macroregião
# Dados generalizados por Macroregião
@app.callback(
    Output("macroregion-chart", "figure"),
    Input("dropdown-map", "value"),
    Input("store-macroregion-on-date","data")
)
def update_subplots_macro(dropdown_map_v, json_data):
    df_macroregion = pd.read_json(json_data)

    x = df_macroregion.sort_values(dropdown_map_v, ascending=True)["regiao"]
    y = df_macroregion.sort_values(dropdown_map_v, ascending=True)[dropdown_map_v]
    
    if dropdown_map_v == "casosAcumulado":
        title_temp="Casos Acumulados por Macroregião"
        subplots_macroregion=go.Figure(
            go.Pie(
                labels=x, values=y, 
                marker=dict(colors = cores_casos, line=dict(color="white", width=1)),
                pull=[0,0,0,0,0.05],
                texttemplate="%{label}"+"<br>%{percent}", textposition="inside",
                hovertemplate = "<b>%{label}</b><br>Casos Acumulados: %{value}<br></b>Percentual: %{percent}<extra></extra>"
            )
        )

    if dropdown_map_v == "obitosAcumulado": 
        title_temp="Óbitos Acumulados por Macroregião"
        subplots_macroregion=go.Figure(
            go.Pie(
                labels=x, values=y, 
                marker=dict(colors = cores_obitos, line=dict(color="white", width=1)),
                pull=[0,0,0,0,0.05],
                texttemplate="%{label}"+"<br>%{percent}", textposition="inside",
                hovertemplate = "<b>%{label}</b><br>Casos Acumulados: %{value}<br></b>Percentual: %{percent}<extra></extra>"
            )
        )
    
    if dropdown_map_v == "incidencia":
        title_temp="Taxa de Ocorrência por 100 mil Habitantes<br>para cada Macroregião"
        subplots_macroregion=go.Figure(
            go.Bar(
                x=x, y=y,
                marker=dict(color = cores_incidencia, line=dict(color="white", width=1)),
                texttemplate="%{y:,.2f}",
                hovertemplate = "<b>%{x}</b><br>Incidência: %{y:,.2f}<extra></extra>"
            )
        )
        subplots_macroregion.update_layout(
            xaxis=dict(title="Macroregiões"),
            yaxis=dict(title="Incidência por 100 mil habitantes",gridcolor="rgba(255, 255, 255, 0.1)", gridwidth=0.5, griddash="dashdot")
        )

    if dropdown_map_v == "mortalidade":
        title_temp="Taxa de Óbitos por 100 mil Habitantes<br>para cada Macroregião"
        subplots_macroregion=go.Figure(
            go.Bar(
                x=x, y=y,
                marker=dict(color = cores_mortalidade, line=dict(color="white", width=1)),
                texttemplate="%{y:,.2f}",
                hovertemplate = "<b>%{x}</b><br>Mortalidade: %{y:,.2f}<extra></extra>"
            )
        )  

        subplots_macroregion.update_layout(
            xaxis=dict(title="Macroregiões"),
            yaxis=dict(title="Mortalidade por 100 mil habitantes",gridcolor="rgba(255, 255, 255, 0.1)", gridwidth=0.5, griddash="dashdot")
        )

    if dropdown_map_v == "taxaLetalidade":
        title_temp="Taxa de Letalidade por Macroregião"
        subplots_macroregion=go.Figure(
            go.Barpolar(
                theta=x, 
                r=y,
                marker=dict(color = cores_letalidade, line=dict(color="white", width=1)),
                hovertemplate = "<b>%{theta}</b>"
                                "<br>Casos Acumulados: %{customdata[0]:,.0f}"
                                "<br>Óbitos Acumulados: %{customdata[1]:,.0f}"
                                "<br>Taxa de Letalidade: %{r:,.2f}%<extra></extra>",
                customdata=df_macroregion.sort_values(dropdown_map_v, ascending=True)[["casosAcumulado","obitosAcumulado"]]
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
            title=dict(text=title_temp, x=0.5),
            margin=dict(t=50, b=50, l=0, r=0), 
            showlegend=False,
            plot_bgcolor="rgba(0, 0, 0, 0)", 
            paper_bgcolor="rgba(0, 0, 0, 0)", 
            separators=", "
            
        )

    return subplots_macroregion


# Callback para renderizar gráficos com dados filtrados por macroregião
# Gráficos dos Estados de cada Macroregião
@app.callback(
    Output("subplots-states", "figure"),
    Input("dropdown-macroregion", "value"),
    Input("dropdown-map","value"),
    Input("store-states-on-date", "data")
)
def update_subplots_states(dropdown_macroregion_v, dropdown_map_v, json_data):
    df_states_on_date = pd.read_json(json_data)
    dff = df_states_on_date[df_states_on_date["regiao"]==dropdown_macroregion_v] #Estados por macroregião
    
    x = dff.sort_values(dropdown_map_v, ascending=True)["siglaUF"]
    y = dff.sort_values(dropdown_map_v, ascending=True)[dropdown_map_v]

    if dropdown_map_v == "casosAcumulado":
        subplots_estados=go.Figure(
            go.Bar(
                x=x, y=y,
                marker=dict(color=cores_casos, line=dict(color="white", width=1)),
                texttemplate="%{y:,.0f}",
                customdata=dff.sort_values(dropdown_map_v, ascending=True)["estado"],
                hovertemplate = "<b>%{customdata}</b><br>Casos Acumulados: %{y:,.0f}<extra></extra>"
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
                x=x, y=y,
                marker=dict(color=cores_obitos, line=dict(color="white", width=1)),
                texttemplate="%{y:,.0f}",
                customdata=dff.sort_values(dropdown_map_v, ascending=True)["estado"],
                hovertemplate = "<b>%{customdata}</b><br>Óbitos Acumulados: %{y:,.0f}<extra></extra>"
            )
        )
        subplots_estados.update_layout(
            title=dict(text=f"Óbitos Acumulados por Estados - {dropdown_macroregion_v}", x=0.5),
            xaxis=dict(title="Estados"),
            yaxis=dict(title="Óbitos Acumulados",gridcolor="rgba(255, 255, 255, 0.1)", gridwidth=0.5, griddash="dashdot")
        )
        
    if dropdown_map_v == "incidencia":
        subplots_estados=px.scatter(
            data_frame=dff,
            x="populacaoTCU2019",
            y="casosAcumulado",
            size="casosAcumulado",
            color="incidencia",
            color_continuous_scale=cores_incidencia,
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
            customdata=dff["estado"],
            hovertemplate=("<b>%{customdata}</b><br>População: %{x:,.0f}<br>Casos: %{y:,.0f}<br>Incidência: %{marker.color:,.2f}<extra></extra>")
        )
        
    if dropdown_map_v == "mortalidade":
        subplots_estados=px.scatter(
            data_frame=dff,
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
            customdata=dff["estado"],
            hovertemplate=("<b>%{customdata}</b><br>População: %{x:,.0f}<br>Obitos: %{y:,.0f}<br>Mortalidade: %{marker.color:,.2f}<extra></extra>")
        )
  
    if dropdown_map_v == "taxaLetalidade":
        subplots_estados=go.Figure(
            go.Barpolar(
                theta=x, 
                r=y,
                marker=dict(color=cores_letalidade, line=dict(color="white", width=1)),
                hovertemplate = "<b>%{customdata[0]}</b>"
                                "<br>Casos Acumulados: %{customdata[1]:,.0f}"
                                "<br>Óbitos Acumulados: %{customdata[2]:,.0f}"
                                "<br>Taxa de Letalidade: %{r:,.2f}%<extra></extra>",
                customdata=dff.sort_values(dropdown_map_v, ascending=True)[["estado","casosAcumulado","obitosAcumulado"]]
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
        margin=dict(t=50, b=50, l=0, r=0),
        showlegend=False,
        plot_bgcolor="rgba(0, 0, 0, 0)", 
        paper_bgcolor="rgba(0, 0, 0, 0)",
        separators=", ",
    )
    return subplots_estados


# Callback para renderizar gráficos com dados filtrados por estado
# Gráficos de cada Estado ISOLADO
@app.callback(
    Output("stacked-bar-chart", "figure"),
    Output("line-chart-state", "figure"),
    Input("dropdown-state", "value"),
    Input("datepicker", "date")
)
def update_ranger_slider_state(dropdown_state_v, date):
    dff = estados_df[(estados_df["data"] <= date) & (estados_df["estado"]==dropdown_state_v)]
    
    # Criar df somente com os valores de novos ocorrências de CASOS e separar os totais/metropolitana/interiror    
    novos_casos_df = dff[dff["casosNovos"] != 0].sort_values("casosAcumulado", ascending=True)
    total_casos = novos_casos_df["casosAcumulado"].max()
    casos_metropolitana = novos_casos_df[novos_casos_df["interior/metropolitana"] == 1]["casosAcumulado"].max()
    casos_interior = total_casos - casos_metropolitana
    
    # Criar df somente com os valores de novos ocorrências de ÓBITOS e separar os totais/metropolitana/interiror
    novos_obitos_df = dff[dff["obitosNovos"] != 0].sort_values("obitosAcumulado", ascending=True)
    total_obitos = novos_obitos_df["obitosAcumulado"].max()
    obitos_metropolitana = novos_obitos_df[novos_obitos_df["interior/metropolitana"] == 1]["obitosAcumulado"].max()
    obitos_interior = total_obitos - obitos_metropolitana
    
    # Agrupar dados por data de casos e obitos acumulados e calcular taxa de letalidade para o estado filtrado
    dff_by_state = dff.groupby("data")[["casosAcumulado", "obitosAcumulado"]].agg(max).reset_index()
    dff_by_state["taxaLetalidade"]=dff_by_state["obitosAcumulado"]/dff_by_state["casosAcumulado"]*100

    bars_state = go.Figure()
    bars_state.add_trace(
        go.Bar(
            x=[casos_metropolitana, obitos_metropolitana], y=["Casos", "Óbitos"], 
            orientation="h", 
            name="Metropolitana",
            marker = dict(color="#EDBBA7"), 
            customdata=[casos_metropolitana, obitos_metropolitana],
            hovertemplate = "<br><b>%{label} - Região Metropolitana</b>"
                            "<br>Percentual: %{x:,.2f}%"
                            "<br>Total de Registros: %{customdata:,.0f}<extra></extra>"
        )
    )
    bars_state.add_trace(
        go.Bar(
            x=[casos_interior, obitos_interior], y=["Casos", "Óbitos"], 
            orientation="h", 
            name="Interior",
            marker = dict(color="#9CB8A0"),
            customdata=[casos_interior, obitos_interior],
            hovertemplate = "<br><b>%{label} - Áreas do Interior</b>"
                            "<br>Percentual: %{x:,.2f}%:"
                            "<br>Total de Registros: %{customdata:,.0f}<extra></extra>"
        )
    )
    bars_state.update_layout(
        font=dict(color="white"),
        title=dict(text=f"Distribuição Regional - {dropdown_state_v}", x=0.5, y=0.9, xanchor="center", yanchor="top"),
        xaxis=dict(visible=False),
        yaxis=dict(showticklabels=True),
        legend=dict(x=0.475, y=1.375, xanchor="center", yanchor="top", orientation="h"),
        margin=dict(t=60, b=0, r=0, l=0, pad=10),
        hoverlabel=dict(bgcolor="#515960"),
        barmode="stack",
        barnorm="percent",
        height=140,
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        separators=", "
    ) 

    lines_state = go.Figure()
    lines_state.add_trace(
        go.Scatter(
            x=dff_by_state["data"],
            y=dff_by_state["obitosAcumulado"],
            name="Óbitos Acumulados",
            fill="tonextx",
            line=dict(color="#972930"),
            hovertemplate="Óbitos Acumulados: %{y:,.0f}      Taxa de Letalidade: %{customdata:,.2f}%<extra></extra>",
            customdata=dff_by_state["taxaLetalidade"]
        )
    )
    lines_state.add_trace(
        go.Scatter(
            x=dff_by_state["data"],
            y=dff_by_state["casosAcumulado"],
            name="Casos Acumulados",
            fill="tonexty",
            line=dict(color="#E6C1A6"),
            hovertemplate="Casos Acumulados: %{y:,.0f}<extra></extra>",
            yaxis="y2" 
        )
    )
    lines_state.update_layout(
        font=dict(color="white"),
        title=dict(text=f"Dinâmica dos Casos<br>e Óbitos Acumulados - {dropdown_state_v}", x=0.5, y=0.95, xanchor="center", yanchor="top"),
        xaxis=dict(title=dict(text="Data"), rangeslider=dict(visible=True), gridcolor="rgba(255,255,255,0.1)", gridwidth=0.5),
        yaxis=dict(gridcolor="rgba(255,255,255,0.1)", gridwidth=0.5),
        yaxis2=dict(overlaying="y", side="right", gridcolor="rgba(255,255,255,0.1)", gridwidth=0.5),  
        legend=dict(x=0.5, y=1.15, xanchor="center", yanchor="top", orientation="h"),
        margin=dict(t=80, b=60, r=0, l=0),
        hoverlabel=dict(bgcolor="#515960"),
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        separators=", "
    )

    return bars_state, lines_state


# Callback para renderizar o mapa do Brasil
@app.callback(
    Output("map-chart", "figure"),
    Input("dropdown-map", "value"),
    Input("store-states-on-date", "data"),
)
def update_map(dropdown_map_v, json_data):
    dff = pd.read_json(json_data)
        
    if dropdown_map_v == "casosAcumulado":
        z_max = int(dff["casosAcumulado"].max())
        colors = cores_casos
        colorbar_title = "Casos" 
        custom_data = dff[["estado","casosAcumulado","casosNovos"]]
        hover_template = ("<b>%{location} - %{customdata[0]}</b>"
                          "<br>Casos Acumulados: %{customdata[1]:,.0f}"
                          "<br>Novos casos no dia: %{customdata[2]:,.0f}<extra></extra>"
        ) 

    if dropdown_map_v == "obitosAcumulado":
        z_max = int(dff["obitosAcumulado"].max())
        colors = cores_obitos
        colorbar_title = "Óbitos" 
        custom_data=dff[["estado","obitosAcumulado", "obitosNovos"]]
        hover_template = ("<b>%{location} - %{customdata[0]}</b>"
                          "<br>Óbitos Acumulados: %{customdata[1]:,.0f}"
                          "<br>Óbitos registrados no dia: %{customdata[2]:,.0f}<extra></extra>"
        )

    if dropdown_map_v == "incidencia":
        z_max = float(dff["incidencia"].max())
        colors = cores_incidencia
        colorbar_title = "Incidência" 
        custom_data=dff[["estado","casosAcumulado","populacaoTCU2019", "incidencia"]]
        hover_template = ("<b>%{location} - %{customdata[0]}</b>"
                          "<br>Casos Acumulados: %{customdata[1]:,.0f}"
                          "<br>População Total: %{customdata[2]:,.0f}"
                          "<br><b>Incidência: %{customdata[3]:,.2f}</b><extra></extra>"
        )

    if dropdown_map_v == "mortalidade":
        z_max = float(dff["mortalidade"].max())
        colors = cores_mortalidade
        colorbar_title = "Mortalidade" 
        custom_data=dff[["estado","obitosAcumulado","populacaoTCU2019", "mortalidade"]]
        hover_template = ("<b>%{location} - %{customdata[0]}</b>"
                          "<br>Óbitos Acumulados: %{customdata[1]:,.0f}"
                          "<br>População Total: %{customdata[2]:,.0f}"
                          "<br><b>Mortalidade: %{customdata[3]:,.2f}</b><extra></extra>"
        )

    if dropdown_map_v == "taxaLetalidade":
        z_max = float(dff["taxaLetalidade"].max())
        colors = cores_letalidade
        colorbar_title = "Letalidade" 
        custom_data=dff[["estado","casosAcumulado", "obitosAcumulado", "taxaLetalidade"]]
        hover_template = ("<b>%{location} - %{customdata[0]}</b>"
                          "<br>Casos Acumulados: %{customdata[1]:,.0f}"
                          "<br>Óbitos Acumulados: %{customdata[2]:,.0f}"
                          "<br><b>Taxa de Letalidade: %{customdata[3]:,.2f}%</b><extra></extra>"
        )
        

    map_chart = go.Figure(
        go.Choroplethmapbox(
            geojson=geo_data,
            locations=dff["siglaUF"],
            z=dff[dropdown_map_v],
            colorscale=colors,
            zmin=0,
            zmax=z_max,
            marker_opacity=0.7,
            marker_line_width=0.5,
            hovertemplate=hover_template,
            customdata=custom_data,
            colorbar=dict(title=dict(text=colorbar_title, side="top"), orientation="h", xanchor="center", yanchor="bottom", x=0.5, y=-0.15)
        )
    )
    map_chart.update_layout(
        font=dict(color="white"),
        margin=dict(r=0, l=0, t=0, b=0),
        mapbox_center=dict(lat=-15, lon=-54),
        mapbox_style="carto-positron",
        mapbox_zoom=3.35,
        height=700,
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        separators=", "
    )
    map_chart.update_geos(framecolor="rgba(0,0,0,0)")

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
register_modal_callback("open-gini","modal-gini")
register_modal_callback("open-palma","modal-palma")
register_modal_callback("open-incidencia","modal-incidencia")
register_modal_callback("open-mortalidade","modal-mortalidade")
register_modal_callback("open-letalidade","modal-letalidade")


# Iniciar o servidor do aplicativo Dash
if __name__ == "__main__": 
    app.run_server(debug=True)
   