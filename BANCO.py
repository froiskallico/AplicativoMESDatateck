import sqlite3

class BANCO():

    def __init__(self):
        self.conexao = sqlite3.connect('TESTEPDS.db')
        self.conexao.text_factory = lambda x: str(x, 'cp1252')
        self.createTable()

    def createTable(self):
        c = self.conexao.cursor()

        c.execute("""create table if not exists pds (
                     ID integer primary key autoincrement,
                     REQNUM integer,
                     PD integer,
                     CABO text,
                     DECAPEA integer,
                     DECAPEB integer,
                     MEDIDA integer,
                     ACAB1 text,
                     ACAB2 text,
                     OBS text,
                     PAI text,
                     QTD integer,
                     QTD_CORT integer,
                     ENTREGA integer,
                     PRIOR integer,
				     MAQUINA text,
				     PRI_MEDIDA integer,
				     ULT_MEDIDA interger)""")

        c.execute("""create table if not exists tempos (
                     TMP_ID integer primary key autoincrement,
                     ID_PD integer,
                     DATA integer,
                     TEMPO_SETUP integer,
                     TEMPO_CICLO integer,
                     QTD_CORTADA integer)""")

        self.conexao.commit()
        c.close()


