from time import time
from banco import BANCO
class TEMPOS():

    def __init__(self, TMP_ID = 0, ID_PD = 0, DATA = 0, TEMPO_SETUP = 0, TEMPO_CICLO = 0, QTD_CORTADA = 0):
        self.info = {}
        self.TMP_ID = TMP_ID
        self.ID_PD = ID_PD
        self.DATA = DATA
        self.TEMPO_SETUP = TEMPO_SETUP
        self.TEMPO_CICLO = TEMPO_CICLO
        self.QTD_CORTADA = QTD_CORTADA

    def setup(self, ID_PD, TEMPO_SETUP):
        banco = BANCO()
        c = banco.conexao.cursor()
        c.execute("SELECT TEMPO_SETUP FROM TEMPOS WHERE ID_PD = %s;" % (ID_PD))
        tempoPD = c.fetchone()
        print (tempoPD)
        c.execute("UPDATE TEMPOS SET TEMPO_SETUP = %s WHERE ID_PD = %s;" % (TEMPO_SETUP, ID_PD))
##        banco.conexao.commit()
        banco.conexao.close()
        
