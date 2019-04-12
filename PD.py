from BANCO import BANCO

class PD(object):
    
    def __init__(self, ID = 0, REQNUM = 0, PD = 0, CABO = "", DECAPEA = 0, DECAPEB = 0, MEDIDA = 0, ACAB1 = "", ACAB2 = "", OBS = "", PAI = "", QTD = 0, QTD_CORT = 0, ENTREGA = 0, PRIOR = 0, MAQUINA = "", PRI_MEDIDA = 0, ULT_MEDIDA = 0):
        self.info = {}
        self.ID = ID
        self.REQNUM = REQNUM
        self.PD = PD
        self.CABO = CABO
        self.DECAPEA = DECAPEA
        self.DECAPEB = DECAPEB
        self.MEDIDA = MEDIDA
        self.ACAB1 = ACAB1
        self.ACAB2 = ACAB2
        self.OBS = OBS
        self.PAI = PAI
        self.QTD = QTD
        self.QTD_CORT = QTD_CORT
        self.ENTREGA = ENTREGA
        self.PRIOR = PRIOR
        self.MAQUINA = MAQUINA
        self.PRI_MEDIDA = PRI_MEDIDA
        self.ULT_MEDIDA = ULT_MEDIDA

    def buscarPD(self, maquina):

        banco = BANCO()

        try:
            c = banco.conexao.cursor()
            c.execute('SELECT * FROM pds where MAQUINA = "%s" and QTD > QTD_CORT order by CABO, MEDIDA desc limit 1' % maquina)
            for linha in c:
                self.ID = linha[0]
                self.REQNUM = linha[1]
                self.PD = linha[2]
                self.CABO = linha[3]
                self.DECAPEA = linha[4]
                self.DECAPEB = linha[5]
                self.MEDIDA = linha[6]
                self.ACAB1 = linha[7]
                self.ACAB2 = linha[8]
                self.OBS = linha[9]
                self.PAI = linha[10]
                self.QTD = linha[11]
                self.QTD_CORT = linha[12]
                self.ENTREGA = linha[13]
                self.PRIOR = linha[14]
                self.MAQUINA = linha[15]
                self.PRI_MEDIDA = linha[16]
                self.ULT_MEDIDA = linha[17]

            c.close()

            return "Busca feita com sucesso!"

        except:
            return "Ocorreu um erro na busca do PD"

    def STATUS(self, ID):

        banco = BANCO()

        c = banco.conexao.cursor()

        self.ID = ID
        c.execute("SELECT CRT_FINAL FROM pds WHERE ID = %s;" % (self.ID))

        for linha in c:
            self.status = linha[0]

        return self.status

        c.close()

    def atualizaQuantidadeCortada(self, pdID, qtdCortada):

        banco = BANCO()

        c = banco.conexao.cursor()

        c.execute("UPDATE pds SET QTD_CORT = %s WHERE ID = %s;" % (qtdCortada, pdID))

        banco.conexao.commit()
        banco.conexao.close()
