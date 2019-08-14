import fdb
import sqlite3
import configparser as cfgprsr
import os
import pandas as pd

diretorio = os.path.dirname(os.path.abspath(__file__))

configFile = cfgprsr.ConfigParser()
configFile.read(diretorio + '/config.ini')
limiteHorizonte = configFile['DEFAULT']['Limite Horizonte']
maquina = configFile['DEFAULT']['Maq']


def origem():
    try:
        conOrigem = fdb.connect(dsn='192.168.1.100:/app/database/DADOS.FDB',
                                user='SYSDBA',
                                password='el0perdid0',
                                charset='WIN1252')
        curOrigem = conOrigem.cursor()
    except:
        print ("Erro na conexão com o banco de dados de origem!")

    try:
        curOrigem.execute("""SELECT 
                                 * 
                             FROM 
                                 PDS_PENDENTES_CORTE
                             WHERE
                                 "DATA ENTREGA" <= CURRENT_DATE + %i
                                 AND "MÁQUINA" = '%s'
                             ORDER BY
                                 "DATA ENTREGA",
                                 "CABO"
                          """ % (int(limiteHorizonte), maquina))
        global dadosOrigem
        dadosOrigem = curOrigem.fetchall()

        curOrigem.close()

        global aplicavelOrigem
        aplicavelOrigem = pd.read_sql_query("""SELECT 
                                                    PRO.COD_FABRIC as "ACABAMENTO",
                                                    PRO.APLICAVEL 
                                                FROM 
                                                    PRODUTOS PRO
                                                WHERE
                                                    PRO.FK_CAD != 13;
                                            """,
                                            conOrigem)


    except:
        print("Erro na obtenção dos dados de origem!")


def origem2destino():
    try:
        conDestino = sqlite3.connect(database=diretorio + '/database/DADOS.db')
        conDestino.text_factory = lambda x: str(x, 'cp1252')
        curDestino = conDestino.cursor()
    except:
        print("Erro na conexao com o banco de dados de destino local!")

    global dadosDestino
    dadosDestino = []

    try:
        for linhaOrigem in dadosOrigem:
            linhaDestino = []
            for c in range(len(linhaOrigem)):
                linhaDestino.append(str(linhaOrigem[c]))
            try:
                temp_prioridade = curDestino.execute("""SELECT
                                                            PRIORIDADE
                                                        FROM
                                                            PDS
                                                        WHERE 
                                                            PK_IRP = %s""" % linhaOrigem[0]).fetchone()
                if temp_prioridade is None:
                    temp_prioridade = 0
                else:
                    temp_prioridade = temp_prioridade[0]
            except:
                temp_prioridade = 0

            linhaDestino.append(temp_prioridade)

            dadosDestino.append(tuple(linhaDestino))

        for linha in dadosDestino:
            curDestino.execute("""REPLACE INTO PDS (
                                      PK_IRP,
                                      REQUISICAO,
                                      CELULA,
                                      [DATA GERAÇÃO],
                                      [DATA ENTREGA],
                                      [OBSERVAÇÃO REQ],
                                      CHICOTE,
                                      PD,
                                      CPD,
                                      CABO,
                                      FK_CRS,
                                      VIAS,
                                      BITOLA,
                                      UNIDADE,
                                      [QTD PD REQ],
                                      QTD_CORTADA,
                                      MEDIDA,
                                      [DECAPE A],
                                      [DECAPE B],
                                      [ACABAMENTO 1],
                                      [PONTE 1],
                                      [ACABAMENTO 2],
                                      [PONTE 2],
                                      [ACABAMENTO 3],
                                      [PONTE 3],
                                      [ACABAMENTO 4],
                                      [PONTE 4],
                                      OBSERVAÇÃO,
                                      GRAVAÇÃO,
                                      MÁQUINA,
                                      [NR. ORDEM CORTE],
                                      PRIORIDADE)
                                  VALUES
                                      %s""" % str(linha))
        conDestino.commit()

        aplicavelOrigem.to_sql('APLICAVEL',
                               conDestino,
                               if_exists='replace',
                               index=False)

        conDestino.commit()

        conDestino.close()

    except Exception as e:
        print(e)
        print("Erro ao inserir dados no banco de dados de destino local!")


def atualizaBancoLocal():
    origem()
    origem2destino()

    print("Linhas na Origem: %i" % len(dadosOrigem))
    print("Linhas na Destino: %i" % len(dadosDestino))
    print('FIM')

atualiza = atualizaBancoLocal()
del atualiza
