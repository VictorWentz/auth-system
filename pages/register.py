import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import numpy as np


from dash.exceptions import PreventUpdate


from werkzeug.security import generate_password_hash, check_password_hash


from app import *


card_style = {
    'width': '300px',
    'min-height': '300px',
    'padding-top': '25px',
    'padding-right': '25px',
    'padding-left': '25px',
    'align-self': 'center'
}



def render_layout(message):

    message = 'Ocorreu algum erro durante o registro.' if message == 'error' else message

    register = dbc.Card([
        html.Legend('Registrar'),
        dbc.Input(id='user-register', placeholder = 'Username', type='text'),
        dbc.Input(id='pwd-register', placeholder = 'Password', type='password'),
        dbc.Input(id='email-register', placeholder = 'Email', type='email'),
        dbc.Button('Registrar', id='button-register-complete'),
        html.Span(message, style={'text-align': 'center'}),
        html.Div([
            html.Label('Ou', style={'margin-right': '5px'}),
            dcc.Link('Faça-login', href='/login'),

        ], style={'padding': '20px', 'justify-content': 'center', 'display': 'flex'})


        
    ], style=card_style)

    return register

@app.callback(

    Output('register-state', 'data'),
    Input('button-register-complete', 'n_clicks'),

    [
        State('user-register','value'),
        State('pwd-register', 'value'),
        State('email-register', 'value')
    ]
)
def register(n_clicks, username, password, email):
    if n_clicks is None:
        raise PreventUpdate

    if username is not None and password is not None and email is not None:
        hased_pwd = generate_password_hash(password, method='sha256')
        ins = Users_tbl.insert().values(username=username, 
        password=hased_pwd, email=email)
        conn = engine.connect()
        conn.execute(ins)
        conn.close()
        
        return ''
    else:
        
        return 'error'
