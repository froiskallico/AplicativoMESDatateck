import sqlite3

class BANCO():

    def __init__(self):
        self.conexao = sqlite3.connect('database/TESTEPDS.db')
        # self.conexao.text_factory = lambda x: str(x, 'cp1252')
        self.createTable()

    def createTable(self):
        c = self.conexao.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS TEMPOS (
                     PK_TEM                 integer primary key autoincrement,
                     DATA                   integer,
                     FK_ID                  integer,
                     FK_TTM                 integer,
                     FK_USU                 integer,
                     MAQUINA                text,
                     FK_MOT                 integer,
                     FOREIGN KEY(FK_ID)     REFERENCES PDS(ID),
                     FOREIGN KEY(FK_TTM)    REFERENCES TIPOS_TEMPOS(PK_TTM),
                     FOREIGN KEY(FK_USU)    REFERENCES USUARIOS(PK_USU),
                     FOREIGN KEY(FK_MOT)    REFERENCES MOTIVOS_PARADA(PK_MOT))""")

        c.execute("""CREATE TABLE IF NOT EXISTS TIPOS_TEMPOS (
                     PK_TTM         integer primary key autoincrement,
                     DESCRICAO      text,
                     INICIO_FIM     text)""")

        c.execute("""CREATE TABLE IF NOT EXISTS USUARIOS (
                     PK_USU         integer primary key autoincrement,
                     NOME           text,
                     SENHA          text)""")

        c.execute("""CREATE TABLE IF NOT EXISTS TIPOS_REGISTROS (
                     PK_TRG         integer primary key autoincrement,
                     DESCRICAO      text,
                     ORIGEM         text)""")

        c.execute("""CREATE TABlE IF NOT EXISTS REGISTROS_QUALIDADE (
                     PK_RGQ                 integer primary key autoincrement,
                     DATA                   integer,
                     FK_ID			        integer,
                     FK_TRG			        integer,
                     VALOR_REGISTRO	        real,
                     LADO			        text,
                     FK_USU			        integer,
                     MAQUINA		        text,
                     FOREIGN KEY(FK_ID)     REFERENCES PDS(PK_IQC),
                     FOREIGN KEY(FK_TRG)	REFERENCES TIPOS_REGISTROS(PK_TRG),
                     FOREIGN KEY(FK_USU) 	REFERENCES USUARIOS(PK_USU))""")

        c.execute("""CREATE TABLE IF NOT EXISTS MOTIVOS_DIVERGENCIAS (
                     PK_MDV         integer primary key autoincrement,
                     DESCRICAO      text)""")

        c.execute("""CREATE TABLE IF NOT EXISTS MOTIVOS_PARADA (
                     PK_MOT            INTEGER PRIMARY KEY ASC AUTOINCREMENT,
                     DESCRICAO         TEXT,
                     ATIVO             TEXT,
                     PARADA_PROGRAMADA TEXT)""")



        self.conexao.commit()
        c.close()


