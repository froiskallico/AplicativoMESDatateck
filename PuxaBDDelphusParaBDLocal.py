import fdb
import sqlite3
import configparser as cfgprsr

configFile = cfgprsr.ConfigParser()
configFile.read('./config.ini')
limiteHorizonte = configFile['DEFAULT']['Limite Horizonte']

def origem(limiteHorizonte):
    try:
        conOrigem = fdb.connect(dsn='192.168.1.100:/app/database/DADOS_PCP.FDB',
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
                                 "DATA ENTREGA" < CURRENT_DATE + %i
                             ORDER BY
                                 "DATA ENTREGA",
                                 "CABO"
                          """ % int(limiteHorizonte))
        global dadosOrigem
        dadosOrigem = curOrigem.fetchall()
    except:
        print("Erro na obtenção dos dados de origem!")


def origem2destino():
    try:
        conDestino = sqlite3.connect(database='./database/TESTEPDS.db')
        curDestino = conDestino.cursor()
    except:
        print("Erro na conexão com o banco de dados de destino local!")

    global dadosDestino
    dadosDestino = []

    try:
        for linhaOrigem in dadosOrigem:
            linhaDestino = []
            for c in range(len(linhaOrigem)):
                linhaDestino.append(str(linhaOrigem[c]))
            dadosDestino.append(tuple(linhaDestino))

        for linha in dadosDestino:
            curDestino.execute("REPLACE INTO PDS VALUES %s" % str(linha))

        conDestino.commit()

    except:
        print("Erro ao inserir dados no banco de dados de destino local!")


def atualizaBancoLocal():
    origem(limiteHorizonte)
    origem2destino()

    print("Linhas na Origem: %i" % len(dadosOrigem))
    print("Linhas na Destino: %i" % len(dadosDestino))
    print('FIM')

