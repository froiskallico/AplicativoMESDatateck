import configparser as cfgprsr
import os
import pandas as pd
from tempo_restante import TempoRestanteAteOFinalDoExpediente as TR
import logger
import banco


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

        self.global_database_dsn = self.configFile['GLOBAL_DATABASE']['dsn']
        self.global_database_user = self.configFile['GLOBAL_DATABASE']['user']
        self.global_database_password = self.configFile['GLOBAL_DATABASE']['password']
        self.global_database_charset = self.configFile['GLOBAL_DATABASE']['charset']

        self.origem()


        # print("Linhas na Origem: %i" % self.dadosLimitados.shape[0])
        # print("Linhas na Destino: %i" % len(dadosDestino))
        # print('FIM')

    def origem(self):
        try:
            conGlobal = banco.GLOBAL_DATABASE().conexao
        except Exception as e:
            logger.logError("Erro na conexao com o banco de dados de origem!    -    Details: {}".format(str(e)))


        if self.filtraLista == 'True':
            try:
                dadosOrigem = pd.read_sql_query("""SELECT
                                                       *
                                                   FROM
                                                       PDS_PENDENTES_CORTE_COR
                                                   WHERE
                                                       "NR_ORDEM_CORTE" in {}
                                                   ORDER BY
                                                       "DATA_ENTREGA",
                                                       "CABO";
                                                """.format(self.ordensCorte),
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
            except Exception as e:
                logger.logError("Erro na obtenção dos dados de origem!    -    Details: {}".format(str(e)))
        else:
            try:
                dadosOrigem = pd.read_sql_query("""SELECT 
                                                    * 
                                                FROM 
                                                    PDS_PENDENTES_CORTE_COR
                                                WHERE
                                                    "DATA_ENTREGA" <= CURRENT_DATE + %i AND
                                                    "MAQUINA" = '%s'
                                                ORDER BY
                                                    "DATA_ENTREGA",
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

            except Exception as e:
                logger.logError("Erro na obtenção dos dados de origem!    -    Details: {}".format(str(e)))

        self.origem2destino()

    def origem2destino(self):
        try:
            conLocal = banco.BANCO().conexao

        except Exception as e:
            logger.logError("Erro na conexao com o banco de dados de destino local!    -    Details: {}".format(str(e)))

        try:
            self.dadosLimitados.insert(32, 'PRIORIDADE', 0)
            self.dadosLimitados.insert(0, 'PK_RCQ', 0)

            labels=['PK_RCQ',
                    'REQUISICAO',
                    'CORTE',
                    'NR_ORDEM_CORTE',
                    'MAQUINA',
                    'CELULA',
                    'DATA_GERACAO',
                    'DATA_ENTREGA',
                    'OBSERVACAO_REQ',
                    'CHICOTE',
                    'PD',
                    'CPD',
                    'CABO',
                    'COR',
                    'VIAS',
                    'BITOLA',
                    'UNIDADE',
                    'NORMA',
                    'QTD_PD_REQ',
                    'QTD_CORTADA',
                    'MEDIDA',
                    'DECAPE_A',
                    'DECAPE_B',
                    'ACABAMENTO_1',
                    'PONTE_1',
                    'ACABAMENTO_2',
                    'PONTE_2',
                    'ACABAMENTO_3',
                    'PONTE_3',
                    'ACABAMENTO_4',
                    'PONTE_4',
                    'OBSERVACAO',
                    'GRAVACAO',
                    'PRIORIDADE']

            types=['TEXT',
                   'INTEGER',
                   'INTEGER',
                   'INTEGER',
                   'TEXT',
                   'TEXT',
                   'TEXT',
                   'TEXT',
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
                   'INTEGER']

            schema = {k:v for k, v in zip(labels, types)}

            self.dadosLimitados['PK_RCQ'] = self.dadosLimitados['REQUISICAO'].astype(str).str.split('.', expand=True) + '|' + self.dadosLimitados['CORTE'].astype(str).str.split('.', expand=True) + '|' + self.dadosLimitados['QTD_PD_REQ'].astype(str).str.split('.', expand=True)

            self.dadosLimitados.to_sql("PDS",
                                       conLocal,
                                       if_exists='replace',
                                       index=False,
                                       dtype=schema)
        except Exception as e:
            logger.logError("Erro ao salvar dados no BD Local    -    Details: {}".format(str(e)))


AtualizaBancoLocal()