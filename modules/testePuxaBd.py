import fdb

con = fdb.connect(dsn='192.168.1.100:/app/database/DADOS_PCP.FDB',
                  user='SYSDBA',
                  password='el0perdid0')

cur = con.cursor()

cur.execute("SELECT * FROM BITOLAS")

dadosOrigem = cur.fetchall()

print (dadosOrigem)
