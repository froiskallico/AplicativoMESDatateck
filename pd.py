from banco import BANCO

class PD(object):
    
    def __init__(self, ID = 0, REQNUM = 0, PD = 0, CABO = "", DECAPEA = 0, DECAPEB = 0, MEDIDA = 0, ACAB1 = "", ACAB2 = "", OBS = "", PAI = "", QTD = 0, QTD_CORT = 0, ENTREGA = 0, PRIOR = 0, MAQUINA = "", PRI_MEDIDA = 0, ULT_MEDIDA = 0):
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


    def atualizaQuantidadeCortada(self, pdID, qtdCortada):

        banco = BANCO()

        c = banco.conexao.cursor()

        c.execute("UPDATE pds SET QTD_CORT = %s WHERE ID = %s;" % (qtdCortada, pdID))

        banco.conexao.commit()
        banco.conexao.close()

