from web_app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'MuriloCunha'}
    return render_template('index.html', title='Sistema de Comunicação Interna', user=user)