import os
import configparser as cfgprsr
from banco import BANCO, GLOBAL_DATABASE
from datetime import datetime as dt
import logger

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
        self.filtaLista = self.configFile['DEFAULT']['filtralista']

    def buscaLista(self):
        banco = BANCO()

        if self.maquinaAutomatica == 'True':
            strOrdenacao = """ORDER BY
                                  PDS.PRIORIDADE,
                                  BITOLA,
                                  (SELECT SUM([QTD_PD_REQ]) FROM PDS P where P.CABO = PDS.CABO GROUP BY CABO) DESC,
                                  MEDIDA DESC"""
        else:
            strOrdenacao = """ORDER BY
                                  BITOLA,
                                  (SELECT SUM([QTD_PD_REQ]) FROM PDS P where P.CABO = PDS.CABO GROUP BY CABO) DESC,
                                  MEDIDA DESC"""

        try:
            c = banco.conexao.cursor()

            if self.filtaLista == 'True':
                c.execute('''SELECT
                               *
                             FROM
                               PDS
                             WHERE
                               PDS."QTD_PD_REQ" > PDS.QTD_CORTADA
                          ''' + strOrdenacao)
            else:
                c.execute('''SELECT
                               *
                             FROM
                               PDS
                             WHERE
                               PDS.MAQUINA = "%s" AND
                               PDS."QTD_PD_REQ" > PDS.QTD_CORTADA
                          ''' % self.maquina + strOrdenacao)

            self.lista = c.fetchall()

            c.close()

            return "Busca feita com sucesso!"

        except Exception as e:
            return "Ocorreu um erro na busca do PD"
            logger.logError("Ocorreu um erro na busca do PD    -    Details: {}".format(str(e)))

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
                                    PK_RCQ = "{}"
                             '''.format(str(ID)))

            self.dadosPD = curDados.fetchone()

            return "Busca feita com sucesso!"

        except Exception as e:
            return "Ocorreu um erro na busca do PD"
            logger.logError("Ocorreu um erro na busca do PD    -    Details: {}".format(str(e)))

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
                                "%s",
                                %i,
                                %d,
                                %i,
                                %i,
                                "%s")""" % (agora,
                                          pdID,
                                          int(linha[1]),
                                          float(linha[2]),
                                          int(linha[3]),
                                          int(linha[4]),
                                          linha[5]))
        banco.conexao.commit()

    def registraCorteNoBanco(self, ID, qtdCortadaEmPecas, qtdCortadaEmMetros):
        try:
            try:
                conOrigem = GLOBAL_DATABASE().conexao
                curOrigem = conOrigem.cursor()
            except Exception as e:
                logger.logError("Erro no metodo: pd.registraCorteNoBanco() -> Erro na conexão com o banco de dados de origem!    -    Details: {}".format(str(e)))
                return False

            try:
                id_array = ID.split('|')
                requisicao = id_array[0]
                corte = id_array[1]
                quantidade = id_array[2]

                curOrigem.execute("EXECUTE PROCEDURE ATUALIZA_IQC({}, {}, {}, {})".format(str(requisicao), str(corte), str(quantidade), str(qtdCortadaEmMetros)))       
            except Exception as e:
                logger.logError("Erro no metodo: pd.registraCorteNoBanco() -> Erro ao tentar transmissao para o Banco de dados Global!    -    Details: {}".format(str(e)))
                return False

            try:
                bancoLocal = BANCO()
                curLocal = bancoLocal.conexao.cursor()
            except Exception as e:
                logger.logError("Erro no metodo: pd.registraCorteNoBanco() -> Erro na conexão com o banco de dados local!    -    Details: {}".format(str(e)))
                return False

            try:
                query = """ 
                            UPDATE
                                PDS
                            SET
                                QTD_CORTADA = {}
                            WHERE
                                PK_RCQ = '{}';
                        """.format(str(qtdCortadaEmPecas), str(ID))
                print(query)
                curLocal.execute(query)
            except Exception as e:
                logger.logError("Erro no metodo: pd.registraCorteNoBanco() -> Erro ao tentar transmissao para o Banco de dados Local!    -    Details: {}".format(str(e)))
                return False

            try:
                conOrigem.commit()
                bancoLocal.conexao.commit()
                conOrigem.close()
                bancoLocal.conexao.close()

                return True
            except Exception as e:
                logger.logError("Erro ao commitar registro de corte nos bancos!    -    Details: {}".format(str(e)))

        except Exception as e:
            logger.logError("Erro ao registrar o corte nos bancos!    -    Details: {} ".format(str(e)))
            return False




        