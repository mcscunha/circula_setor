#!/usr/bin/python3
# -*- coding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.validators import Length
from web_app.models import User


#   Classe HERDADA de FLASKFORM, entao, vem com algumas propriedades e metodos
# adicionais que nao vemos listadas aqui!
class LoginForm(FlaskForm):
    username = StringField('Nome Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar me')
    submit = SubmitField('Logar')


class RegistrationForm(FlaskForm):
    # Inserindo VALIDATORS=[DATAREQUIRED()] obriga a construcao deste
    # metodo de validacao
    username = StringField('Nome Usuário', validators=[DataRequired()])
    # Inserindo VALIDATORS=[Email] o flask validara automaticamente
    # se o conteudo confere com um endereco eletronico
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    # Inserindo VALIDATORS=[EQUALTO(???)] ele faz uma comparacao deste campo
    # com o outro informado em ???
    password2 = PasswordField(
        'Repetir Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')

    # Quando um metodo é criado com a estrutura VALIDATE_<FIELDNAME>
    # O WTForms adiciona este metodo ao VALIDATOR do campo e executa-o
    # para verificacao
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Usuário já cadastrado. ' + \
                'Por favor use outro nome.')

    # Quando um metodo é criado com a estrutura VALIDATE_<FIELDNAME>
    # O WTForms adiciona este metodo ao VALIDATOR do campo e executa-o
    # para verificacao
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email já cadastrado. ' + \
                'Por favor use outro endereço eletrônico.')


class EditProfileForm(FlaskForm):
    username = StringField('Nome Usuário', validators=[DataRequired()])
    about_me = TextAreaField('Sobre mim', validators=[Length(min=0, max=140)])
    submit = SubmitField('Enviar')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Por favor use um outro nome de usuário')