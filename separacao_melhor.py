import pandas as pd
from banco import BANCO
import configparser as cfgprsr
import os

diretorio = os.path.dirname(os.path.abspath(__file__))
configFile = cfgprsr.ConfigParser()
configFile.read(diretorio + '/config.ini')
maquina = configFile['DEFAULT']['Maq']

bancoLocal = BANCO()
connLocal = bancoLocal.conexao

def terminais(lista):
    return pd.Series(pd.concat([lista['ACABAMENTO 1'],
                                lista['ACABAMENTO 2']]).unique())

lco = pd.read_sql_query("""
                            SELECT 
                                PK_IRP, 
                                BITOLA,
                                [QTD PD REQ] - [QTD_CORTADA] AS "QTD",
                                [ACABAMENTO 1],
                                [ACABAMENTO 2],
                                PRIORIDADE
                            FROM 
                                PDS
                            WHERE
                                "QTD" > 0 AND
                                MÁQUINA = '%s';    
                        """ % maquina,
                        connLocal).replace('None', 'Vazio')

apl = pd.read_sql_query("""
                            SELECT
                                *
                            FROM
                                APLICAVEL;
                        """,
                        connLocal)
                                

n = len(terminais(lco))
c = sum(range(n))

ranking = pd.DataFrame()
vol = pd.Series([])

for t in terminais(lco):
    q = 0
    for a in ('ACABAMENTO 1', 'ACABAMENTO 2'):
        q += lco[lco[a]==t].sum()['QTD']

    vol[len(vol)] = q

ranking['Terminal'] = terminais(lco)
ranking['Volume'] = vol

ranking = ranking.join(apl.set_index('ACABAMENTO'), on='Terminal').fillna('Z').sort_values(['APLICAVEL', 'Volume'], ascending=[False, False   ]).reset_index(drop=True)

prioridade = 0
for t in ranking['Terminal']:
    if t == 'Vazio':
        try:
            if lco.loc[((lco['ACABAMENTO 1'] == t) & (lco['ACABAMENTO 2'] == t)) |
                    ((lco['ACABAMENTO 2'] == t) & (lco['ACABAMENTO 1'] == t))]['QTD'].sum() > 0:
                lco.loc[((lco['ACABAMENTO 1'] == t) & (lco['ACABAMENTO 2'] == t)) |
                    ((lco['ACABAMENTO 2'] == t) & (lco['ACABAMENTO 1'] == t)), 'PRIORIDADE'] = prioridade
                prioridade += 1
                continue

            else:
                continue
        except:
            pass

    try:
        t2 = 'Vazio'

        if lco.loc[((lco['ACABAMENTO 1'] == t) & (lco['ACABAMENTO 2'] == t2)) |
                    ((lco['ACABAMENTO 2'] == t) & (lco['ACABAMENTO 1'] == t2))]['QTD'].sum() > 0:
            lco.loc[((lco['ACABAMENTO 1'] == t) & (lco['ACABAMENTO 2'] == t2)) |
                    ((lco['ACABAMENTO 2'] == t) & (lco['ACABAMENTO 1'] == t2)), 'PRIORIDADE'] = prioridade
            prioridade += 1


        t2 = t

        if lco.loc[((lco['ACABAMENTO 1'] == t) & (lco['ACABAMENTO 2'] == t2)) |
                   ((lco['ACABAMENTO 2'] == t) & (lco['ACABAMENTO 1'] == t2))]['QTD'].sum() > 0:
            lco.loc[((lco['ACABAMENTO 1'] == t) & (lco['ACABAMENTO 2'] == t2)) |
                    ((lco['ACABAMENTO 2'] == t) & (lco['ACABAMENTO 1'] == t2)), 'PRIORIDADE'] = prioridade
            prioridade += 1


    except:
        pass

    x = ranking.index[ranking['Terminal']==t][0]

    for i in range(n-1, x, -1):
        t2 = ranking.loc[i, 'Terminal']

        try:
            if lco.loc[((lco['ACABAMENTO 1'] == t) & (lco['ACABAMENTO 2'] == t2)) |
                   ((lco['ACABAMENTO 2'] == t) & (lco['ACABAMENTO 1'] == t2))]['QTD'].sum() > 0:

                lco.loc[((lco['ACABAMENTO 1'] == t) & (lco['ACABAMENTO 2'] == t2)) |
                        ((lco['ACABAMENTO 2'] == t) & (lco['ACABAMENTO 1'] == t2)), 'PRIORIDADE'] = prioridade
                prioridade += 1
            else:
                continue

        except:
            pass



print('Lista de Corte:')
print(lco.head(10))
print('[...] \n\n')


print('Quantidade de acabamentos possíveis nessa LCO: %s' % n)
print(terminais(lco))
print('Quantidade de combinações possíveis de Acabamentos nesta LCO: %s\n' % c)


print('Ranking de aplicações por volume:')
print(ranking)
print('\n\nSequência de setups de aplicação:')
print(lco.sort_values(['PRIORIDADE', 'BITOLA']).to_string())

lco.sort_values(['PRIORIDADE', 'BITOLA']).to_csv('listaOrdenada.csv', sep=';')