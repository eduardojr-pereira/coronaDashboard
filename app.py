#conda install -c conda-forge dash-bootstrap-components
#conda install -c -conda-forge dash
from templates.navbar import Navbar, OffCanvas
from templates.content_component import Content
from templates.footer_component import FooterComponent
from dash import ctx, Dash, dcc, html, Input, Output, State 
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors 
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
# Geo.json para o mapa do Brasil
geo_data = json.load(open("data/raw/brasilGeo.json", "r"))
geo_data["features"][0].keys()


# Função para formatar valores a serem exibidos
def formatar_valor(valor):
    if pd.isna(valor):
        return "-"
    return str(f"{int(valor):,}".replace(",", "."))


# Função para formatar a data selecionada
def formatar_data(date):
    selected_date = pd.to_datetime(date).strftime('%d/%m/%Y')
    return selected_date


# Padronizar paletas de cores
cores_casos = plotly.colors.sequential.matter[:len(estados_df['estado'].unique())]
cores_obitos = plotly.colors.sequential.Inferno_r[:len(estados_df['estado'].unique())]
cores_letalidade = plotly.colors.sequential.Brwnyl[:len(estados_df['estado'].unique())]


# Layout do APP
app.layout=html.Div(
    [
        Navbar().criar_navbar(),
        OffCanvas().criar_offcanvas_visao_geral(),
        OffCanvas().criar_offcanvas_objetivos(),
        OffCanvas().criar_offcanvas_dados(),
        OffCanvas.criar_offcanvas_frameworks(),
        Content.create_content(),
        html.Br(),
        FooterComponent().criar_footer()
    ]
)


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


# Callbacks para abrir Offcanvas
def register_offcanvas_callback(open_id, open_id_footer, offcanvas_id):
    @app.callback(
        Output(offcanvas_id, "is_open"),
        [
            Input(open_id, "n_clicks"),
            Input(open_id_footer, "n_clicks")
        ],
        [State(offcanvas_id, "is_open")],
        allow_duplicate=True
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

    data_formatada = formatar_data(date)
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


# Callback para filtrar o estados_df NA data e por região (armazená-lo no dcc.Store)
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

    df_grouped_on_date["taxaLetalidade"] = df_grouped_on_date["obitosAcumulado"]/df_grouped_on_date["casosAcumulado"]*100
    df_grouped_on_date["mortalidade"] = df_grouped_on_date["obitosAcumulado"]/df_grouped_on_date["populacaoTCU2019"]*100000       
    
    return df_grouped_on_date.to_json()


# Callback para renderizar o mapa do Brasil
@app.callback(
    Output("map-chart", "figure"),
    Input("dropdown-map", "value"),
    Input("datepicker-store", "data"),
)
def update_map(dropdown_map_v, json_data):
    dff = pd.read_json(json_data)
        
    if dropdown_map_v == "casosAcumulado":
        z_max = int(dff["casosAcumulado"].max())
        colors = cores_casos 
        hover_template = ("<b>%{location}</b>"
                          "<br><span style='color:Gold'><b>Casos Acumulados</b>: %{customdata[0]:.0f}</span>"
                          "<br>Novos casos no dia: %{customdata[1]:.0f}<extra></extra>"
        ) 
        custom_data = dff[["casosAcumulado","casosNovos"]]

    if dropdown_map_v == "obitosAcumulado":
        z_max = int(dff["obitosAcumulado"].max())
        colors = cores_obitos
        hover_template = ("<b>%{location}</b><br>"
                          "<br><span style='color:OrangeRed'><b>Óbitos Acumulados:</b> %{customdata[0]:.0f}</span>"
                          "<br>Óbitos registrados no dia: %{customdata[1]:.0f}<extra></extra>"
        )
        custom_data=dff[["obitosAcumulado", "obitosNovos"]]

    if dropdown_map_v == "taxaLetalidade":
        z_max = float(dff["taxaLetalidade"].max())
        colors = cores_letalidade
        hover_template = ("<b>%{location}</b>"
                          "<br>Casos Acumulados: %{customdata[0]:.0f}"
                          "<br>Óbitos Acumulados: %{customdata[1]:.0f}"
                          "<br><span style='color:red'><b>Taxa de Letalidade*</b>: %{customdata[2]:.2f} %</span><extra></extra>"
        )
        custom_data=dff[["casosAcumulado", "obitosAcumulado", "taxaLetalidade"]]

    if dropdown_map_v == "mortalidade":
        z_max = float(dff["mortalidade"].max())
        colors = cores_letalidade
        hover_template = ("<b>%{location}</b>"
                          "<br>Óbitos Acumulados: %{customdata[0]:.0f}"
                          "<br>População Total: %{customdata[1]:.0f}"
                          "<br><span style='color:red'><b>Mortalidade*</b>: %{customdata[2]:.2f}</span><extra></extra>"
        )
        custom_data=dff[["obitosAcumulado","populacaoTCU2019", "mortalidade"]]

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
            customdata=custom_data
        )
    )
    map_chart.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=2.75,
        mapbox_center={"lat": -17, "lon": -55},
        margin={"r": 0, "l": 0, "t": 0, "b": 0}
    )
    
    return map_chart


# Callback para renderizar gráfico com evolução no Brasil
@app.callback(
    Output("lines-chart-casos-brasil", "figure"),
    Output("lines-chart-obitos-brasil", "figure"),
    Input("datepicker", "date")
)
def update_ranger_slider_br(date):
    dff_br = brasil_df[brasil_df["data"] <= date]
      
    lines_chart_casos_br = {
        "data": [
            {
                "x": dff_br["data"],
                "y": dff_br["casosAcumulado"],
                "type": "area",
                "name": "Casos Acumulados",
                "fill": "tozeroy",
                "line": {"color": "#E6C1A6"}
            },
            {
                "x": dff_br["data"],
                "y": dff_br["casosNovos"],
                "type": "line",
                "name": "Novos Casos na data",
                "line": {"color": "#D06450"}
            }
        ],
        "layout": {
            "title":{
                "text": f"Casos Registrados - Brasil",
                "font": {"color": "white"},
                "x":0.53
            },
            "xaxis": {
                "title": {
                    "text": "Data",
                    "font": {"color": "white"}
                },
                "tickfont": {"color": "white"},
                "rangeslider": {"visible": True},
                "gridcolor": "rgba(255, 255, 255, 0.1)",
                "gridwidth": 0.5
            },
            "yaxis": {
                "tickfont": {"color": "white"},
                "gridcolor": "rgba(255, 255, 255, 0.1)",
                "gridwidth": 0.5
            },
            "legend": {
                "x": 0.5,
                "y": 0.985,
                "xanchor": "center",
                "yanchor": "bottom",
                "orientation": "h",
                "font": {"color": "white"}
            },
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "margin":{"t":50, "b":50, "r":10, "l":50}
        }
    }

    lines_chart_obitos_br = {
        "data": [
            {
                "x": dff_br["data"],
                "y": dff_br["obitosAcumulado"],
                "type": "area",
                "name": "Óbitos Acumulados",
                "fill": "tozeroy",
                "line": {"color": "#30242A"}
            },
            {
                "x": dff_br["data"],
                "y": dff_br["obitosNovos"],
                "type": "line",
                "name": "Óbitos na data",
                "line": {"color": "#972930"}
            }
        ],
        "layout": {
            "title":{
                "text": f"Óbitos Registrados - Brasil",
                "font": {"color": "white"},
                "x":0.54
            },
            "xaxis": {
                "title": {
                    "text": "Data",
                    "font": {"color": "white"}
                },
                "tickfont": {"color": "white"},
                "rangeslider": {"visible": True},
                "gridcolor": "rgba(255, 255, 255, 0.1)",
                "gridwidth": 0.5
            },
            "yaxis": {
                "tickfont": {"color": "white"},
                "gridcolor": "rgba(255, 255, 255, 0.1)",
                "gridwidth": 0.5
            },
            "legend": {
                "x": 0.5,
                "y": 0.985,
                "xanchor": "center",
                "yanchor": "bottom",
                "orientation": "h",
                "font": {"color": "white"}
            },
            "paper_bgcolor": "rgba(0, 0, 0, 0)",
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "margin":{"t":50, "b":50, "r":10, "l":50}
        }
    }

    #stacked_bars_br = 

    return lines_chart_casos_br, lines_chart_obitos_br


# Callback para criar gráficos filtrados por data e agrupados por macroregiao
@app.callback(
    Output("macroregiao-texto", "children"),
    Output("badge-texto", "children"),
    Output("bar-chart-casos-obitos", "figure"),
    Input("dropdown-region", "value"),
    Input("dropdown-map","value"),
    Input("datepicker-store", "data"),
    Input("datepicker","date")
)
def update_charts_on_date_by_region(dropdown_region_v, dropdown_map_v, json_data, date):
    dff = pd.read_json(json_data)
    dff_macro = dff[dff["regiao"]==dropdown_region_v]

    if dropdown_map_v == "casosAcumulado":
        macro_title = "Casos Acumulados - Macroregião {}".format(dropdown_region_v)
        badge_str = "Total: {}".format(formatar_valor(dff_macro["casosAcumulado"].sum()))

        bar_chart = {
            "data":[
                {
                    "x": dff_macro.sort_values("casosAcumulado", ascending=True)["siglaUF"],
                    "y": dff_macro.sort_values("casosAcumulado", ascending=True)["casosAcumulado"],
                    "type": "bar",
                    "marker": {"color": cores_casos},
                    "hovertemplate": "<b>" + dff_macro.sort_values("casosAcumulado", ascending=True)["estado"] +
                                     "</b><br>Casos Acumulados: %{y:.0f}<extra></extra>",
                    "customdata": dff_macro.sort_values("casosAcumulado", ascending=True)["siglaUF"]
                }
            ],
            "layout": {
                "xaxis": {
                    "title": {
                        "text": "Estados",
                        "font": {"color": "white"}
                    },
                    "tickfont": {"color": "white"}
                },
                "yaxis": {
                    "title": {
                        "text": "Casos Acumulados",
                        "font": {"color": "white"}
                    },
                    "tickfont": {"color": "white"},
                    "gridcolor": "rgba(255, 255, 255, 0.1)",
                    "gridwidth": 0.5
                },
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "margin":{"t": 0, "b": 50},
                "showlegend": False
            }
        }

    if dropdown_map_v == "obitosAcumulado":
        macro_title = "Óbitos Acumulados - Macroregião {}".format(dropdown_region_v)
        badge_str = "Total: {}".format(formatar_valor(dff_macro["obitosAcumulado"].sum()))

        bar_chart = {
            "data":[
                {
                    "x": dff_macro.sort_values("obitosAcumulado", ascending=True)["siglaUF"],
                    "y": dff_macro.sort_values("obitosAcumulado", ascending=True)["obitosAcumulado"],
                    "type": "bar",
                    "marker": {"color": cores_obitos},
                    "hovertemplate": "<b>" + dff_macro.sort_values("obitosAcumulado", ascending=True)["estado"] +
                                     "</b><br>Óbitos Acumulados: %{y:.0f}<extra></extra>",
                    "customdata": dff_macro.sort_values("obitosAcumulado", ascending=True)["siglaUF"]
                }
            ],
            "layout": {
                "xaxis": {
                    "title": {
                        "text": "Estados",
                        "font": {"color": "white"}
                    },
                    "tickfont": {"color": "white"}
                },
                "yaxis": {
                    "title": {
                        "text": "Óbitos Acumulados",
                        "font": {"color": "white"}
                    },
                    "tickfont": {"color": "white"},
                    "gridcolor": "rgba(255, 255, 255, 0.1)",
                    "gridwidth": 0.5
                },
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "margin":{"t":0, "b":50},
                "showlegend": False
            }
        }

    if dropdown_map_v == "taxaLetalidade":
        macro_title = "Taxa de Letalidade - Macroregião {}".format(dropdown_region_v)
        badge_str = "Taxa de Letalidade Média: {:.2f} %".format(dff_macro["taxaLetalidade"].mean())

        bar_chart = {
            "data":[
                {
                    "x": dff_macro.sort_values("taxaLetalidade", ascending=True)["siglaUF"],
                    "y": dff_macro.sort_values("taxaLetalidade", ascending=True)["taxaLetalidade"],
                    "type": "bar",
                    "marker": {"color": cores_letalidade},
                    "hovertemplate": "<b>" + dff_macro.sort_values("taxaLetalidade", ascending=True)["estado"] +
                                     "</b><br>Taxa de Letalidade*: %{y:.5f} %<extra></extra>",
                    "customdata": dff_macro.sort_values("taxaLetalidade", ascending=True)["siglaUF"]
                },
                {   
                    "x": dff_macro.sort_values("taxaLetalidade", ascending=True)["siglaUF"],
                    "y": [dff_macro["taxaLetalidade"].mean()] * len(dff_macro),
                    "type": "scatter",
                    "mode": "lines",
                    "name": "Taxa de Letalidade Média",
                    "line": {"color": "#8B0000", "dash": "dashdot"},
                    "hoverinfo":None,
                    "hovertemplate":" "
                }
            ],
            "layout": {
                "xaxis": {
                    "title": {
                        "text": "Estados",
                        "font": {"color": "white"}
                    },
                    "tickfont": {"color": "white"}
                },
                "yaxis": {
                    "title": {
                        "text": "Taxa de Letalidade*",
                        "font": {"color": "white"}
                    },
                    "tickfont": {"color": "white"},
                    "gridcolor": "rgba(255, 255, 255, 0.1)",
                    "gridwidth": 0.5
                },
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "margin":{"t":0, "b":50},
                "showlegend": False
            }
        }

    if dropdown_map_v == "mortalidade":
        macro_title = "Mortalidade - Macroregião {}".format(dropdown_region_v)
        badge_str = "Mortalidade média: {:.2f}".format(dff_macro["mortalidade"].mean())

        bar_chart = {
            "data":[
                {
                    "x": dff_macro.sort_values("mortalidade", ascending=True)["siglaUF"],
                    "y": dff_macro.sort_values("mortalidade", ascending=True)["mortalidade"],
                    "type": "bar",
                    "marker": {"color": cores_letalidade},
                    "hovertemplate": "<b>" + dff_macro.sort_values("mortalidade", ascending=True)["estado"] +
                                     "</b><br>Mortalidade*: %{y:.2f}<extra></extra>",
                    "customdata": dff_macro.sort_values("mortalidade", ascending=True)["siglaUF"]
                },
                {   
                    "x": dff_macro.sort_values("mortalidade", ascending=True)["siglaUF"],
                    "y": [dff_macro["mortalidade"].mean()] * len(dff_macro),
                    "type": "scatter",
                    "mode": "lines",
                    "name": "Mortalidade Média",
                    "line": {"color": "#8B0000", "dash": "dashdot"},
                    "hoverinfo":None,
                    "hovertemplate":" "
                }
            ],
            "layout": {
                "xaxis": {
                    "title": {
                        "text": "Estados",
                        "font": {"color": "white"}
                    },
                    "tickfont": {"color": "white"}
                },
                "yaxis": {
                    "title": {
                        "text": "Taxa de Mortalidade*",
                        "font": {"color": "white"}
                    },
                    "tickfont": {"color": "white"},
                    "gridcolor": "rgba(255, 255, 255, 0.1)",
                    "gridwidth": 0.5
                },
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "margin":{"t":0, "b":50},
                "showlegend": False
            }
        }

    return macro_title, badge_str, bar_chart







if __name__ == "__main__":
    app.run_server(debug=True)
   