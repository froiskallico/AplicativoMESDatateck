import os
import fdb
import configparser as cfgprsr
from banco import BANCO
from datetime import datetime as dt

class PD(object):

    def __init__(self):
        self.Definicoes()
        self.lista = {}
        self.dadosPD = ()

    def Definicoes(self):
        self.diretorio = os.path.dirname(os.path.abspath(__file__))
        self.configFile = cfgprsr.ConfigParser()
        self.configFile.read(self.diretorio + '/config.ini')
        self.maquina = self.configFile['DEFAULT']['maquina']
        self.maquinaAutomatica = self.configFile['DEFAULT']['MaqAutomatica']

    def buscaLista(self):
        banco = BANCO()

        if self.maquinaAutomatica:
            strOrdenacao = """ORDER BY
                                  PDS.PRIORIDADE,
                                  BITOLA,
                                  (SELECT SUM([QTD PD REQ]) FROM PDS P where P.CABO = PDS.CABO GROUP BY CABO) DESC,
                                  MEDIDA DESC"""
        else:
            strOrdenacao = """ORDER BY
                                  BITOLA,
                                  (SELECT SUM([QTD PD REQ]) FROM PDS P where P.CABO = PDS.CABO GROUP BY CABO) DESC,
                                  MEDIDA DESC"""

        try:
            c = banco.conexao.cursor()
            c.execute('''SELECT
                           *
                         FROM
                           PDS
                         WHERE
                           PDS.MÁQUINA = "%s" AND
                           PDS."QTD PD REQ" > PDS.QTD_CORTADA
                      ''' % self.maquina + strOrdenacao)

            self.lista = c.fetchall()

            c.close()

            return "Busca feita com sucesso!"

        except:
            return "Ocorreu um erro na busca do PD"

    def buscaPD(self, ID):
        banco = BANCO()

        try:
            curDados = banco.conexao.cursor()
            curDados.execute('''SELECT
                                    PDS.*, 
                                    COALESCE(CORES.DESCRICAO, 'SEM COR'),
                                    COALESCE(CORES.PRIMARIA, '#000000'),
                                    COALESCE(CORES.SECUNDARIA, '#000000'),
                                    COALESCE(CORES.COR_TEXTO, '#FFFFFF')
                                FROM
                                    PDS
                                LEFT JOIN
                                    CORES ON (CORES.PK_CRS = PDS.COR) 
                                WHERE
                                    PK_IRP = %i
                             ''' % ID)

            self.dadosPD = curDados.fetchone()

            return "Busca feita com sucesso!"

        except e:
            return "Ocorreu um erro na busca do PD"

    def registraRQSetup(self, pdID, dados=()):
        banco = BANCO()
        agora = dt.now()

        cur = banco.conexao.cursor()

        for linha in dados:
            cur.execute("""REPLACE INTO REGISTROS_QUALIDADE (
                                DATA,
                                FK_ID,
                                FK_TRG,
                                VALOR_REGISTRO,
                                LADO,
                                FK_USU,
                                MAQUINA)
                            VALUES
                                ("%s",
                                %i,
                                %i,
                                %d,
                                %i,
                                %i,
                                "%s")""" % (agora,
                                          int(linha[0]),
                                          int(linha[1]),
                                          float(linha[2]),
                                          int(linha[3]),
                                          int(linha[4]),
                                          linha[5]))
        # banco.conexao.commit()

    def registraCorteNoBanco(self, ID, qtdCortada):
        try:
            conOrigem = fdb.connect(
                dsn='192.168.1.100:/app/database/DADOS.FDB',
                user='SYSDBA',
                password='el0perdid0',
                charset='WIN1252')
            curOrigem = conOrigem.cursor()

            try:
                curOrigem.execute("""EXECUTE PROCEDURE ATUALIZA_QTD_CORTADA(%s, %s)""" % (ID, qtdCortada))
                # Todo descomentar abaixo
                # conOrigem.commit()
            except:
                print("Erro na gravação dos dados na origem!")

        except:
            print("Erro na conexão com o banco de dados de origem!")


        banco = BANCO()

        cur = banco.conexao.cursor()

        try:
            cur.execute(""" UPDATE
                                PDS
                            SET
                                QTD_CORTADA = %d
                            WHERE
                                PK_IRP = %d
                        """ % (qtdCortada, ID))
            # Todo descomentar abaixo
            # banco.conexao.commit()
        except:
            print('Erro ao registrar quantidade cortada no Banco de Dados Local')
                  
