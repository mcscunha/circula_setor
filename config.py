#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Software:
    CIRCULA_SETOR
Objetivo:
    Arquivo para configuracao do sistema
Linguagem:
    Python 3.7 (Pacote Anaconda3)
    Flask (Framework Python para Web)
    Bootstrap 4 (HTML + CSS + JQuery + JavaScript)
    Jinja
    GIT
    SQLite3 (banco de dados)
Ambiente:
    Web (navegadores Firefox e Chrome)
    Linux (Ubuntu e derivados)
    Windows (7 e 10)
Autor:
    MuriloCunha - mcscunha@yahoo.com.br - 31/10/2019

------------------------------------------------------------------------------
LOG DE ALTERACOES
------------------------------------------------------------------------------
31/10/2019 - Inicio do sistema - Criacao deste arquivo

------------------------------------------------------------------------------
'''

import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # SECRET_KEY é uma variavel do Flask para compor o TOKEN da pagina
    SECRET_KEY = 'bpMfF7XbQuoAP89'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, u'circula_setor.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuracao para envio de emails automatico
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    MAIL_SERVER='localhost'
    MAIL_PORT=8025
    
    # MAIL_SERVER=smtp.googlemail.com
    # MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME='username'
    MAIL_PASSWORD='senha'
    
    POSTS_PER_PAGE = 3