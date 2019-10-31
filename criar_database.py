#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
    Arquivo a ser executado sozinho e UMA UNICA VEZ.
    O objetivo é criar o banco de dados e todas as suas tabelas
    Nao executar se o banco de dados já foi criado anteriormente,
isso pode ocasionar perda de dados de forma irreversivel.

Autor:
    MuriloCunha - mcscunha@yahoo.com.br - 31/10/2019
------------------------------------------------------------------------------
LOG DE ALTERACOES
------------------------------------------------------------------------------
31/10/2019 - Inicio do sistema - Criacao deste arquivo

------------------------------------------------------------------------------
'''

import sqlite3


try:
    database = sqlite3.connect('./circula_setor.db')
    cursor = database.cursor()
    print('Banco de dados criado com sucesso!')

except sqlite3.Error as error:
    print('Erro ao criar o banco de dados:\n', error)

try:
    with open('./criar_tabelas.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    cursor.executescript(sql_script)
    print('Script de criacao das tabelas executado com sucesso')
    cursor.close()
    database.commit()

except sqlite3.Error as error:
    print('Erro na criacao das tabelas iniciais:\n', error)

finally:
    if (database):
        database.close()
        print('O banco de dados foi fechado com sucesso')    
