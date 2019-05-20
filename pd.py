from banco import BANCO
from datetime import datetime as dt


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

        banco = BANCO()

        try:
            c = banco.conexao.cursor()
            c.execute('''   SELECT 
                                *
                            FROM 
                                PDS
                            WHERE
                                MÁQUINA = "%s"
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
                                CORES.DESCRICAO, 
                                CORES.PRIMARIA, 
                                CORES.SECUNDARIA, 
                                CORES.COR_TEXTO
                            FROM
                                PDS
                            LEFT JOIN
                                CORES ON (CORES.PK_CRS = PDS.FK_CRS) 
                            WHERE
                                PK_IQC = "%s"
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
            print(linha)
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