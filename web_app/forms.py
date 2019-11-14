#!/usr/bin/python3
# -*- coding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


#   Classe HERDADA de FLASKFORM, entao, vem com algumas propriedades e metodos
# adicionais que nao vemos listadas aqui!
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')