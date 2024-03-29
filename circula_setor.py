#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Software:
    CIRCULA_SETOR
Objetivo:
    Sistema de troca de comunicados entre setores de uma empresa.
    Pode ser usado para divulgacao de CIRCULARES, AVISOS, NOTIFICACOES
        e outras informacoes que se deseja passar na empresa.
    Semelhante a um chat na rede LAN, no entanto, as informacoes devem 
        ser mais formais, pois sao gravadas em banco e podem ser usadas
        como prova material de alguma infracao.
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


versao = 1.0


from database import Database
from datetime import date
from usuario import Usuario
from web_app import app



'''
Database.conectar_banco()
tup_dados = ('murilo',
             'MuriloCunha',
             '123',
             'mcscunha@yahoo.com.br',
             date.today().strftime('%d/%m/%Y')
)
u = Usuario()
u.gravar_usuario(tup_dados)
Database.recuperar_dados('SELECT * FROM usuario')
Database.fechar_conexao()
'''