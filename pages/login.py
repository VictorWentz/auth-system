import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from flask_login import login_user

from werkzeug.security import check_password_hash

from app import *

import numpy as np
import plotly.express as px



card_style = {
    'width': '300px',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
    'align-self': 'center'
}



def render_layout(message):
    message = 'Ocorreu algum erro durante o Login' if message == 'error' else message
    
    login = dbc.Card([
        html.Legend('Login'),
        dbc.Input(id='user-login', placeholder = 'Username', type='text'),
        dbc.Input(id='pwd-login', placeholder = 'password', type='password'),
        dbc.Button('Login', id='button-register'),
        html.Span(message, style={'text-align': 'center'}),
        html.Div([
            html.Label('Ou', style={'margin-right': '5px'}),
            dcc.Link('Registre-se', href='/register'),

        ], style={'padding': '20px', 'justify-content': 'center', 'display': 'flex'})


        
    ], style=card_style)

    return login



@app.callback(
    Output('login-state', 'data'),
    Input('button-register', 'n_clicks'),

    [
        State('user-login', 'value'),
        State('pwd-login', 'value')
    ]
)
def login_succeful(n_clicks, username, password):
    if n_clicks is None:
        raise PreventUpdate

    user = Users.query.filter_by(username=username).first()

    if user and password is not None:
        if check_password_hash(user.password, password):
            login_user(user)
            return 'success'
        else:
            return 'error'
    else:
        return 'error'
