import fdb
import sqlite3

conOrigem = fdb.connect(dsn='192.168.1.100:/app/database/DADOS_PCP.FDB',
                        user='SYSDBA',
                        password='el0perdid0',
                        charset='WIN1252')
curOrigem = conOrigem.cursor()
curOrigem.execute("""SELECT 
                        FIRST 10 * 
                    FROM 
                        PDS_PENDENTES_CORTE 
                    WHERE 
                        "MÁQUINA" = 'Samec' 
                    ORDER BY 
                        PK_IQC""")


conDestino = sqlite3.connect(database='../database/TESTEPDS.db')
curDestino = conDestino.cursor()
dadosDestino = []


dadosOrigem = curOrigem.fetchall()


for linhaOrigem in dadosOrigem:
    linhaDestino = []
    # print(linhaOrigem)
    for c in range(len(linhaOrigem)):
        # print(linhaOrigem[c])
        linhaDestino.append(str(linhaOrigem[c]))
        # print(linhaDestino[c])
    dadosDestino.append(tuple(linhaDestino))

print(dadosDestino)

for linha in dadosDestino:
    print("INSERT INTO PDS VALUES %s" % str(linha))
    try:
        curDestino.execute("INSERT INTO PDS VALUES %s" % str(linha))
        conDestino.commit()
    except:
        pass


print("Linhas na Origem: %i" % len(dadosOrigem))
print("Linhas na Destino: %i" % len(dadosDestino))
print('FIM')