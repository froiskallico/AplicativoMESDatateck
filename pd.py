import fdb
from banco import BANCO
from datetime import datetime as dt
import PuxaBDDelphusParaBDLocal as imp


class PD(object):
    
    def __init__(self):
        self.lista = {}
        self.dadosPD = ()
        # self.ID = ID
        # self.REQNUM = REQNUM
        # self.PD = PD
        # self.CABO = CABO
        # self.DECAPEA = DECAPEA
        # self.DECAPEB = DECAPEB
        # self.MEDIDA = MEDIDA
        # self.ACAB1 = ACAB1
        # self.ACAB2 = ACAB2
        # self.OBS = OBS
        # self.PAI = PAI
        # self.QTD = QTD
        # self.QTD_CORT = QTD_CORT
        # self.ENTREGA = ENTREGA
        # self.PRIOR = PRIOR
        # self.MAQUINA = MAQUINA
        # self.PRI_MEDIDA = PRI_MEDIDA
        # self.ULT_MEDIDA = ULT_MEDIDA

    def buscaLista(self, maquina):
        i = imp

        i.atualizaBancoLocal()

        banco = BANCO()

        try:
            c = banco.conexao.cursor()
            c.execute('''   SELECT 
                                *
                            FROM 
                                PDS
                            WHERE
                                PDS.MÁQUINA = "%s" AND
                                PDS."QTD PD REQ" > PDS.QTD_CORTADA
                       ''' % maquina)

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
                                    CORES ON (CORES.PK_CRS = PDS.FK_CRS) 
                                WHERE
                                    PK_IRP = "%s"
                       ''' % ID)

            self.dadosPD = curDados.fetchone()

            return "Busca feita com sucesso!"

        except:
            return "Ocorreu um erro na busca do PD"

    # def atualizaQuantidadeCortada(self, pdID, qtdCortada):
    #
    #     banco = BANCO()
    #
    #     c = banco.conexao.cursor()
    #
    #     c.execute("UPDATE pds SET QTD_CORT = %s WHERE ID = %s;" % (qtdCortada, pdID))
    #
    #     banco.conexao.commit()
    #     banco.conexao.close()

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
        banco.conexao.commit()

    def registraCorteNoBanco(self, ID, qtdCortada):
        try:
            conOrigem = fdb.connect(
                dsn='192.168.1.100:/app/database/DADOS_PCP.FDB',
                user='SYSDBA',
                password='el0perdid0',
                charset='WIN1252')
            curOrigem = conOrigem.cursor()

            try:
                curOrigem.execute("""UPDATE
                                         IRQ_PD
                                     SET
                                         QTD_CORTADA = %d
                                     WHERE
                                         PK_IRP = %d
                                  """ % (qtdCortada, ID))

                conOrigem.commit()
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

            banco.conexao.commit()
        except:
            print('Erro ao registrar quantidade cortada no Banco de Dados Local')
                  
