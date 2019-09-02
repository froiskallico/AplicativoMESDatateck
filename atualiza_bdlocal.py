import fdb
import sqlite3
import configparser as cfgprsr
import os
import pandas as pd
from tempo_restante import TempoRestanteAteOFinalDoExpediente as TR


class AtualizaBancoLocal:
    def __init__(self):

        self.diretorio = os.path.dirname(os.path.abspath(__file__))
        self.configFile = cfgprsr.ConfigParser()
        self.configFile.read(self.diretorio + '/config.ini')
        self.limiteHorizonte = self.configFile['DEFAULT']['Limite Horizonte']
        self.limiteDiarioCircuitos = self.configFile['DEFAULT']['LimiteDiarioCircuitos']
        self.maquina = self.configFile['DEFAULT']['maquina']
        self.limiteCircuitos = int(
            int(self.limiteDiarioCircuitos) * TR().percentRestante())
        self.filtraLista = self.configFile['DEFAULT']['filtraLista']
        self.ordensCorte = self.configFile['DEFAULT']['ordens']

        self.origem()


        # print("Linhas na Origem: %i" % self.dadosLimitados.shape[0])
        # print("Linhas na Destino: %i" % len(dadosDestino))
        # print('FIM')

    def origem(self):
        try:
            conGlobal = fdb.connect(dsn='192.168.1.100:/app/database/DADOS.FDB',
                                    user='SYSDBA',
                                    password='el0perdid0',
                                    charset='WIN1252')
        except:
            print ("Erro na conexão com o banco de dados de origem!")

        if self.filtraLista == 'True':
            try:
                dadosOrigem = pd.read_sql_query("""SELECT
                                                       *
                                                   FROM
                                                       PDS_PENDENTES_CORTE_NEW
                                                   WHERE
                                                       "NR. ORDEM CORTE" in %s AND
                                                       "MÁQUINA" = '%s'
                                                   ORDER BY
                                                       "DATA ENTREGA",
                                                       "CABO";
                                                """ % (self.ordensCorte,
                                                          self.maquina),
                                                conGlobal)

                self.dadosLimitados = dadosOrigem

                self.aplicavelOrigem = pd.read_sql_query("""SELECT 
                                                              PRO.COD_FABRIC as "ACABAMENTO",
                                                              PRO.APLICAVEL 
                                                            FROM 
                                                              PRODUTOS PRO
                                                            WHERE
                                                              PRO.FK_CAD != 13;
                                                         """,
                                                         conGlobal)
            except :
                print("Erro na obtenção dos dados de origem!")
        else:
            try:
                dadosOrigem = pd.read_sql_query("""SELECT 
                                                    * 
                                                FROM 
                                                    PDS_PENDENTES_CORTE_NEW
                                                WHERE
                                                    "DATA ENTREGA" <= CURRENT_DATE + %i AND
                                                    "MÁQUINA" = '%s'
                                                ORDER BY
                                                    "DATA ENTREGA",
                                                    "CABO";
                                                """ % (int(self.limiteHorizonte),
                                                             self.maquina),
                                                conGlobal)

                dadosOrdenados = dadosOrigem.sort_values(
                    by='DATA ENTREGA').reset_index(drop=True)

                qtdAcumulada = pd.Series(dadosOrdenados['QTD PD REQ'].cumsum())

                self.dadosLimitados = dadosOrdenados[:qtdAcumulada.where(qtdAcumulada <= int(self.limiteCircuitos)).idxmax(skipna=True)]

                self.aplicavelOrigem = pd.read_sql_query("""SELECT 
                                                         PRO.COD_FABRIC as "ACABAMENTO",
                                                         PRO.APLICAVEL 
                                                       FROM 
                                                         PRODUTOS PRO
                                                       WHERE
                                                         PRO.FK_CAD != 13;
                                                    """, conGlobal)

            except :
                print("Erro na obtenção dos dados de origem!")

        self.origem2destino()

    def origem2destino(self):
        try:
            conLocal = sqlite3.connect(database=self.diretorio + '/database/DADOS.db')
            # conLocal.text_factory = lambda x: str(x, 'cp1252')

        except:
            print("Erro na conexao com o banco de dados de destino local!")


        try:
            self.dadosLimitados.insert(31, 'PRIORIDADE', 0)

            labels=['PK_IRP',
                     'REQUISICAO',
                     'CELULA',
                     'DATA GERAÇÃO',
                     'DATA ENTREGA',
                     'OBSERVAÇÃO REQ',
                     'CHICOTE',
                     'PD',
                     'CPD',
                     'CABO',
                     'COR',
                     'VIAS',
                     'BITOLA',
                     'UNIDADE',
                     'NORMA',
                     'QTD PD REQ',
                     'QTD_CORTADA',
                     'MEDIDA',
                     'DECAPE A',
                     'DECAPE B',
                     'ACABAMENTO 1',
                     'PONTE 1',
                     'ACABAMENTO 2',
                     'PONTE 2',
                     'ACABAMENTO 3',
                     'PONTE 3',
                     'ACABAMENTO 4',
                     'PONTE 4',
                     'OBSERVAÇÃO',
                     'GRAVAÇÃO',
                     'MÁQUINA',
                     'NR. ORDEM CORTE',
                     'PRIORIDADE']

            types=['INTEGER',
                   'INTEGER',
                   'TEXT',
                   'INTEGER',
                   'INTEGER',
                   'TEXT',
                   'TEXT',
                   'INTEGER',
                   'INTEGER',
                   'TEXT',
                   'INTEGER',
                   'TEXT',
                   'INTEGER',
                   'TEXT',
                   'TEXT',
                   'INTEGER',
                   'INTEGER',
                   'INTEGER',
                   'TEXT',
                   'TEXT',
                   'TEXT',
                   'TEXT',
                   'TEXT',
                   'TEXT',
                   'TEXT',
                   'TEXT',
                   'TEXT',
                   'TEXT',
                   'TEXT',
                   'TEXT',
                   'TEXT',
                   'INTEGER',
                   'INTEGER']

            schema = {k:v for k, v in zip(labels, types)}

            self.dadosLimitados.to_sql("PDS",
                                       conLocal,
                                       if_exists='replace',
                                       index=False,
                                       dtype=schema)
        except e:
            print("Erro ao salvar dados no BD Local")


AtualizaBancoLocal()