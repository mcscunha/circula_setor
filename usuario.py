#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
    Classe que controla os dados de USUARIOS no sistema


Autor:
    MuriloCunha - mcscunha@yahoo.com.br - 31/10/2019

------------------------------------------------------------------------------
LOG DE ALTERACOES
------------------------------------------------------------------------------
31/10/2019 - Inicio do sistema - Criacao deste arquivo

------------------------------------------------------------------------------
'''
from database import Database


class Usuario(object):

    def __init__(self):
        self.tabela = 'usuario'
        self.colunas = ('usuario', 'nome', 'senha', 'email', 'data_cadastro')
        self.id_usuario = 'id'

    def gravar_usuario(self, tup_dados):
        Database.inserir_dado(self.tabela, self.colunas, tup_dados)

    def excluir_usuario(self, id_):
        Database.apagar_dado(self.tabela, self.id_usuario, id_)
