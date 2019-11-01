#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
    Arquivo para gravacao das informacoes no banco de dados
    Modelo MVC de construcao

Autor:
    MuriloCunha - mcscunha@yahoo.com.br - 31/10/2019

------------------------------------------------------------------------------
LOG DE ALTERACOES
------------------------------------------------------------------------------
31/10/2019 - Inicio do sistema - Criacao deste arquivo

------------------------------------------------------------------------------
'''
import sqlite3
from pprint import pprint
from util import pverd

class Database(object):
    banco = u'circula_setor.db'
    conexao = sqlite3.connect('')

    @staticmethod
    def conectar_banco():
        Database.conexao = sqlite3.connect(Database.banco)
        print(pverd('[BD      ]'), ': Conexão no banco com sucesso')

    @staticmethod
    def fechar_conexao():
        Database.conexao.close()
        print(pverd('[BD      ]'), ': Conexão com o banco de dados fechada')

    @staticmethod
    def inserir_dado(tabela, campos, dados):
        comando = f'INSERT OR REPLACE INTO {tabela} {campos} VALUES {dados};'
        print(pverd('[BD      ]'), comando)
        Database.conexao.execute(comando)
        Database.conexao.commit()

    @staticmethod
    def apagar_dado(tabela, coluna_id, id_dado):
        comando = f'DELETE FROM {tabela} WHERE {coluna_id} = {id_dado};'
        print(pverd('[BD      ]'), comando)
        Database.conexao.execute(comando)
        Database.conexao.commit()

    @staticmethod
    def recuperar_dados(str_select):
        print(pverd('[BD      ]'), str_select)
        cur = Database.conexao.cursor()
        ex = cur.execute(str_select)
        dados = ex.fetchall()
        pprint(dados)
