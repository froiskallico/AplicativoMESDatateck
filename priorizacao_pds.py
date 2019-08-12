import pandas as pd
import configparser as cfgprsr
import sqlite3
import os
from tkinter import *
from tkinter import ttk



class AlgoritmoSeparacao:
    def __init__(self, master=None):
        self.master = master
        self.diretorio = os.path.dirname(os.path.abspath(__file__))

        def montaWidgets():
            self.varBarra = IntVar()
            self.cabecalho = Label(self.master,
                                   text="Aguarde o Sequenciamento de Setup",
                                   font=["Play", 20, "bold"],
                                   bg="#333333",
                                   fg="white",
                                   justify="center")
            self.cabecalho.pack(fil=BOTH,
                                expand=1,
                                pady=20)

            self.barraProgresso = ttk.Progressbar(self.master,
                                                  orient='horizontal',
                                                  mode='determinate',
                                                  len=400,
                                                  var=self.varBarra)
            self.barraProgresso.pack(fill=BOTH,
                                     expand=1,
                                     pady=20,
                                     padx=50)

            self.rodape = Label(self.master,
                                text="Isso pode levar alguns segundos mas estamos \n garantindo o menor número de setups possível",
                                font=["Play", 14, "bold"],
                                bg="#333333",
                                fg="#BBBBBB",
                                justify="center")
            self.rodape.pack(fill=BOTH,
                             expand=1,
                             pady=20)

            print(self.diretorio)

            self.logoTri_100p = PhotoImage(file=self.diretorio + "/src/images/logos/logoTri.png")

            self.logoTri = Label(self.master,
                                 image=self.logoTri_100p,
                                 font=["Maven Pro", 14, "bold"],
                                 bg="#333333",
                                 fg="#BBBBBB")
            self.logoTri.pack()

        montaWidgets()


        self.Definicoes()
        self.OrdenaLista()

    def Definicoes(self):
        self.diretorio = os.path.dirname(os.path.abspath(__file__))
        self.configFile = cfgprsr.ConfigParser()
        self.configFile.read(self.diretorio + '/config.ini')
        self.maquina = self.configFile['DEFAULT']['Maq']

        self.connLocal = sqlite3.connect(self.diretorio + '/database/DADOS.db')

    def ImportaLista(self):
        self.lco = pd.read_sql_query("""
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
                                         [QTD PD REQ] - [QTD_CORTADA] > 0 AND
                                         MÁQUINA = '%s';    
                                     """ % self.maquina,
                                     self.connLocal).replace('None', 'Vazio')

    def ImportaAplicaveis(self):
        self.apl = pd.read_sql_query("""
                                         SELECT
                                             *
                                         FROM
                                             APLICAVEL;
                                     """,
                                     self.connLocal)

    def ExtraiTerminais(self):
        self.ImportaLista()
        self.ImportaAplicaveis()

        self.terminais = pd.Series(pd.concat([self.lco['ACABAMENTO 1'],
                                              self.lco['ACABAMENTO 2']]).unique())

        self.n = len(self.terminais)
        self.c = sum(range(self.n))

        self.barraProgresso['max'] = self.n

    def DefineRankeamento(self):
        self.ExtraiTerminais()

        self.ranking = pd.DataFrame()
        vol = pd.Series([])

        for t in self.terminais:
            q = 0
            for a in ('ACABAMENTO 1', 'ACABAMENTO 2'):
                q += self.lco[self.lco[a]==t].sum()['QTD']

            vol[len(vol)] = q

        self.ranking['ACABAMENTO'] = self.terminais
        self.ranking['Volume'] = vol

        self.ranking = self.ranking.join(self.apl.set_index('ACABAMENTO'),
                                         on='ACABAMENTO')                  \
                                   .fillna('Z')                            \
                                   .sort_values(['APLICAVEL', 'Volume'],
                                                ascending=[False, False])  \
                                   .reset_index(drop=True)

    def DefinePrioridades(self):
        self.DefineRankeamento()

        prioridade = 1
        Acab1 = self.lco['ACABAMENTO 1']
        Acab2 = self.lco['ACABAMENTO 2']

        for t in self.ranking['ACABAMENTO']:
            if t == 'Vazio':
                try:
                    if self.lco.loc[((Acab1 == t) & (Acab2 == t)) |
                                    ((Acab2 == t) & (Acab1 == t))]['QTD'].sum() > 0:
                        self.lco.loc[(((Acab1 == t) & (Acab2 == t)) |
                                     ((Acab2 == t) & (Acab1 == t))), 'PRIORIDADE'] = prioridade
                        prioridade += 1

                    continue

                except :
                    pass

            else:
                try:
                    for t2 in ('Vazio', t):
                        if self.lco.loc[((Acab1 == t) & (Acab2 == t2)) |
                                        ((Acab2 == t) & (Acab1 == t2))]['QTD'].sum() > 0:
                            self.lco.loc[((Acab1 == t) & (Acab2 == t2)) |
                                         ((Acab2 == t) & (Acab1 == t2)), 'PRIORIDADE'] = prioridade
                            prioridade += 1
                except:
                    pass

                x = self.ranking.index[self.ranking['ACABAMENTO'] == t][0]
                self.varBarra.set(x)
                self.master.update()

                if x >= self.n * 0.8:
                    self.rodape['text'] = "Quase lá. Só falta mais um pouco..."

                for i in range(self.n - 1, x, -1):
                    t2 = self.ranking.loc[i, 'ACABAMENTO']

                    try:
                        if self.lco.loc[((Acab1 == t) & (Acab2 == t2)) |
                                        ((Acab2 == t) & (Acab1 == t2))]['QTD'].sum() > 0:
                            self.lco.loc[((Acab1 == t) & (Acab2 == t2)) |
                                         ((Acab2 == t) & (Acab1 == t2)), 'PRIORIDADE'] = prioridade
                            prioridade += 1
                        else:
                            continue
                    except:
                        pass

    def ExibeResultados(self):
        print('Lista de Corte:')
        print(self.lco.head(10))
        print('[...] \n\n')


        print('Quantidade de acabamentos possíveis nessa LCO: %s' % self.n)
        print(self.terminais)
        print('Quantidade de combinações possíveis de Acabamentos nesta LCO: %s\n' % self.c)


        print('Ranking de self.aplicações por volume:')
        print(self.ranking)
        print('\n\nSequência de setups de self.aplicação:')
        print(self.lco.sort_values('PRIORIDADE').to_string())

    def RegistraOrdenacaoNoBanco(self):
        self.DefinePrioridades()

        self.lco.sort_values('PRIORIDADE').to_sql('tempTabelaOrdenada',
                                                  self.connLocal,
                                                  if_exists='replace',
                                                  index=False)

        curLocal =self.connLocal.cursor()

        curLocal.execute("""
                            UPDATE
                                PDS
                            SET
                                PRIORIDADE = (SELECT 
                                                  PRIORIDADE 
                                              FROM 
                                                  tempTabelaOrdenada TEMP
                                              WHERE
                                                  TEMP.PK_IRP = PDS.PK_IRP);""")

        curLocal.execute("DROP TABLE tempTabelaOrdenada;")

        curLocal.close()
        self.connLocal.close()

    def OrdenaLista(self):
        print("Iniciando...")
        curCont = self.connLocal.cursor()

        cont = curCont.execute("""
                        SELECT
                            COUNT(PRIORIDADE)
                        FROM
                            PDS
                        WHERE
                            PRIORIDADE = 0;""").fetchone()

        if cont[0] == 0:
#            pass
#        else:
            self.RegistraOrdenacaoNoBanco()
#            self.ExibeResultados()


        self.master.destroy()

