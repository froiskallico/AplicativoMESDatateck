import pandas as pd
import numpy as np

arquivoLista = './13553.csv'

def terminais(lista):
    return pd.Series(pd.concat([lista['ACAB1'],
                                lista['ACAB2']]).unique())


lco = pd.read_csv(arquivoLista,
                  sep=';',
                  encoding='CP1252').fillna('Vazio')

apl = pd.read_csv('apl13553.csv',
                  sep=';',
                  encoding='CP1252')


n = len(terminais(lco))
c = sum(range(n))

ranking = pd.DataFrame()
vol = pd.Series([])

for t in terminais(lco):
    q = 0
    for a in ('ACAB1', 'ACAB2'):
        q += lco[lco[a]==t].sum()['QTD']

    vol[len(vol)] = q

ranking['Terminal'] = terminais(lco)
ranking['Volume'] = vol

ranking = ranking.join(apl.set_index('Terminais'), on='Terminal').fillna('Z').sort_values(['APL', 'Volume'], ascending=[False, False   ]).reset_index(drop=True)

prioridade = 1
for t in ranking['Terminal']:
    if t == 'Vazio':
        try:
            if lco.loc[((lco['ACAB1'] == t) & (lco['ACAB2'] == t)) |
                    ((lco['ACAB2'] == t) & (lco['ACAB1'] == t))]['QTD'].sum() > 0:
                lco.loc[((lco['ACAB1'] == t) & (lco['ACAB2'] == t)) |
                    ((lco['ACAB2'] == t) & (lco['ACAB1'] == t)), 'PRIORIDADE'] = prioridade
                prioridade += 1
                continue

            else:
                continue
        except:
            pass

    try:
        t2 = 'Vazio'

        if lco.loc[((lco['ACAB1'] == t) & (lco['ACAB2'] == t2)) |
                    ((lco['ACAB2'] == t) & (lco['ACAB1'] == t2))]['QTD'].sum() > 0:
            lco.loc[((lco['ACAB1'] == t) & (lco['ACAB2'] == t2)) |
                    ((lco['ACAB2'] == t) & (lco['ACAB1'] == t2)), 'PRIORIDADE'] = prioridade
            prioridade += 1


        t2 = t

        if lco.loc[((lco['ACAB1'] == t) & (lco['ACAB2'] == t2)) |
                   ((lco['ACAB2'] == t) & (lco['ACAB1'] == t2))]['QTD'].sum() > 0:
            lco.loc[((lco['ACAB1'] == t) & (lco['ACAB2'] == t2)) |
                    ((lco['ACAB2'] == t) & (lco['ACAB1'] == t2)), 'PRIORIDADE'] = prioridade
            prioridade += 1


    except:
        pass

    x = ranking.index[ranking['Terminal']==t][0]

    for i in range(n-1, x, -1):
        t2 = ranking.loc[i, 'Terminal']

        try:
            if lco.loc[((lco['ACAB1'] == t) & (lco['ACAB2'] == t2)) |
                   ((lco['ACAB2'] == t) & (lco['ACAB1'] == t2))]['QTD'].sum() > 0:

                lco.loc[((lco['ACAB1'] == t) & (lco['ACAB2'] == t2)) |
                        ((lco['ACAB2'] == t) & (lco['ACAB1'] == t2)), 'PRIORIDADE'] = prioridade
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
print(lco.sort_values('PRIORIDADE').to_string())

lco.sort_values('PRIORIDADE').to_csv('13553SeparacaoExport.csv', sep=';')