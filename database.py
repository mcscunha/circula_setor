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


class CirculaSetor(object):
    banco_dados = 'circula_setor.db'


    @staticmethod
    def conectar_banco():
        sqlite3.connect(CirculaSetor.banco_dados)


    @staticmethod
    def gravar_dados():
        pass


    @staticmethod
    def apagar_dados():
        pass


    @staticmethod
    def recuperar_dado(self, id_dado):
        #return 
        pass


    @staticmethod
    def recuperar_dados(self):
        #return
        pass