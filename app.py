#conda install -c conda-forge dash-bootstrap-components
#conda install -c -conda-forge dash
from dash import ctx, Dash, dcc, html, Input, Output, State 
import dash_bootstrap_components as dbc
from templates.navbar import *
from templates.footer_component import FooterComponent

# Instanciar APP
app=Dash(
    __name__,
    title="coronaDash - Eduardo Pereira",
    external_stylesheets=[dbc.themes.SLATE,'https://use.fontawesome.com/releases/v5.8.1/css/all.css'],
    meta_tags=[{"name":"viewport","content":"width=device-width, inital-scale=1","http-equiv": "X-UA-Compatible", "content": "IE=9"}]
)


# Layout do APP
app.layout=html.Div(
    [
        Navbar().criar_navbar(),
        OffCanvas().criar_offcanvas_visao_geral(),
        OffCanvas().criar_offcanvas_objetivos(),
        OffCanvas().criar_offcanvas_dados(),
        OffCanvas.criar_offcanvas_frameworks(),
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


# Callbacks para abrir os offcanvas
def toggle_offcanvas_callback(open_id, offcanvas_id):
    @app.callback(
        Output(offcanvas_id, "is_open"),
        Input(open_id, "n_clicks"),
        State(offcanvas_id, "is_open"),
    )
    def toggle_offcanvas(n_clicks, is_open):
        if ctx.triggered:
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]
            if button_id == open_id:
                return not is_open
        return is_open

toggle_offcanvas_callback("open-visaoGeral", "offcanvas-visaoGeral")

toggle_offcanvas_callback("open-objetivos", "offcanvas-objetivos")

toggle_offcanvas_callback("open-frameworks", "offcanvas-frameworks")

toggle_offcanvas_callback("open-dados", "offcanvas-dados")


if __name__ == "__main__":
    app.run_server(debug=True)