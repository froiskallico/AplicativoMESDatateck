from banco import BANCO
from datetime import datetime as dt

class MOTIVOS(object):

    def __init__(self):
        self.listaMotivos = []

    def buscaListaMotivosDivergencia(self):
        banco = BANCO()

        try:
            c = banco.conexao.cursor()
            c.execute('''SELECT 
                             DESCRICAO
                         FROM 
                             MOTIVOS_DIVERGENCIAS
                         ORDER BY
                             PK_MDV
                       ''')

            linhas = c.fetchall()

            for linha in linhas:
                self.listaMotivos.append(linha[0])

            c.close()

            return self.listaMotivos
        except:
            print("Ocorreu um erro na busca dos motivos")

    def buscaListaMotivosParada(self):
        banco = BANCO()

        try:
            c = banco.conexao.cursor()
            c.execute('''SELECT 
                             DESCRICAO
                         FROM 
                             MOTIVOS_PARADA
                         ORDER BY
                             PK_MOT
                       ''')

            linhas = c.fetchall()

            for linha in linhas:
                self.listaMotivos.append(linha[0])

            c.close()

            return self.listaMotivos
        except:
            print("Ocorreu um erro na busca dos motivos")
