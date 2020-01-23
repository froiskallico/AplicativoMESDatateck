import sqlite3
import os
import configparser as cfgprsr
import fdb
import logger

diretorio = os.path.dirname(os.path.abspath(__file__))

configFile = cfgprsr.ConfigParser()
configFile.read(diretorio + '/config.ini')

class BANCO():
    def __init__(self):
        try:
            self.conexao = sqlite3.connect(diretorio + '/database/DADOS.db')
        except Exception as e:
            logger.logError("Erro ao conectar ao banco de dados local.    -    Details: {}".format(str(e)))

#        self.conexao.text_factory = lambda x: str(x, 'cp1252')
            self.createTable()

    def createTable(self):
        c = self.conexao.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS TEMPOS (
                     PK_TEM                 integer primary key autoincrement,
                     DATA                   real,
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
                     FK_ID                  integer,
                     FK_TRG                 integer,
                     VALOR_REGISTRO         real,
                     LADO                   text,
                     FK_USU                 integer,
                     MAQUINA                text,
                     FOREIGN KEY(FK_ID)     REFERENCES PDS(PK_IRP),
                     FOREIGN KEY(FK_TRG)    REFERENCES TIPOS_REGISTROS(PK_TRG),
                     FOREIGN KEY(FK_USU)    REFERENCES USUARIOS(PK_USU))""")

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


class GLOBAL_DATABASE():
    def __init__(self):
        try:
            self.global_database_dsn = configFile['GLOBAL_DATABASE']['dsn']
            self.global_database_user = configFile['GLOBAL_DATABASE']['user']
            self.global_database_password = configFile['GLOBAL_DATABASE']['password']
            self.global_database_charset = configFile['GLOBAL_DATABASE']['charset']
        except Exception as e:
            logger.logError("Erro ao ler as variáveis de ambiente.    -    Details: {}".format(str(e)))

        try:
            self.conexao = fdb.connect(dsn=self.global_database_dsn,
                                   user=self.global_database_user,
                                   password=self.global_database_password,
                                   charset=self.global_database_charset)
        except Exception as e:
            logger.logError("Erro ao abrir a conexão com o banco global (Delphus).    -    Details: {}".format(str(e)))