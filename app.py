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

if __name__ == "__main__":
    app.run_server(debug=True)