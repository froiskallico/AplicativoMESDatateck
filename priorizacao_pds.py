import pandas as pd
import configparser as cfgprsr
from banco import BANCO
import os
from tkinter import *
from tkinter import ttk
import logger

class AlgoritmoSeparacao:
    def __init__(self, master=None, headless=False):
        self.master = master
        self.headless = headless
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

            self.logoTri_100p = PhotoImage(file=self.diretorio + "/src/images/logos/logoTri_100p.png")

            self.logoTri = Label(self.master,
                                 image=self.logoTri_100p,
                                 font=["Maven Pro", 14, "bold"],
                                 bg="#333333",
                                 fg="#BBBBBB")
            self.logoTri.pack(pady=25)

        if not self.headless:
            montaWidgets()


        self.Definicoes()
        self.OrdenaLista()

    def Definicoes(self):
        try:
            self.diretorio = os.path.dirname(os.path.abspath(__file__))
            self.configFile = cfgprsr.ConfigParser()
            self.configFile.read(self.diretorio + '/config.ini')
            self.maquina = self.configFile['DEFAULT']['maquina']
        except Exception as e:
            logger.logError("Erro ao ler as variáveis de ambiente.    -    Details: {}".format(str(e)))

        try:
            self.connLocal = BANCO().conexao
        except Exception as e:
            logger.logError("Erro ao conectar ao banco de dados Local para priorização dos PDs.    -    Details: {}".format(str(e)))         

    def ImportaLista(self):
        try:
            self.lco = pd.read_sql_query("""
                                         SELECT 
                                             PK_RCQ, 
                                             [QTD_PD_REQ] - [QTD_CORTADA] AS "QTD",
                                             [ACABAMENTO_1],
                                             [ACABAMENTO_2],
                                             PRIORIDADE
                                         FROM 
                                             PDS
                                         WHERE
                                             [QTD_PD_REQ] - [QTD_CORTADA] > 0 AND
                                             MAQUINA = '%s';    
                                         """ % self.maquina,
                                         self.connLocal).fillna('Vazio')
        except Exception as e:
            logger.logError("Erro ao importar a lista de PDs para priorização de PDs.    -    Details: {}".format(str(e)))

    def ImportaAplicaveis(self):
        try:
            self.apl = pd.read_sql_query("""
                                             SELECT
                                                 *
                                             FROM
                                                 APLICAVEL;
                                         """,
                                         self.connLocal)
        except Exception as e:
            logger.logError("Erro ao ler a tabela APLICAVEL do banco de dados local.    -    Details: {}".format(str(e)))

    def ExtraiTerminais(self):
        self.ImportaLista()
        self.ImportaAplicaveis()

        self.terminais = pd.Series(pd.concat([self.lco['ACABAMENTO_1'],
                                              self.lco['ACABAMENTO_2']]).unique())

        self.n = len(self.terminais)
        self.c = sum(range(self.n))

        if not self.headless:
            self.barraProgresso['max'] = self.n

    def DefineRankeamento(self):
        try:
            self.ExtraiTerminais()
        except Exception as e:
            logger.logError("Erro ao extrair os terminais da lista de PDs para priorização dos PDs.    -    Details: {}".format(str(e)))

        self.ranking = pd.DataFrame()
        vol = pd.Series([])

        for t in self.terminais:
            q = 0
            for a in ('ACABAMENTO_1', 'ACABAMENTO_2'):
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
        try:
            self.DefineRankeamento()
        except Exception as e:
            logger.logError("Erro ao definir o ranking de terminais para priorização dos PDs.    -    Details: {}".format(str(e)))

        prioridade = 1
        Acab1 = self.lco['ACABAMENTO_1']
        Acab2 = self.lco['ACABAMENTO_2']

        for t in self.ranking['ACABAMENTO']:
            if t == 'Vazio':
                try:
                    if self.lco.loc[((Acab1 == t) & (Acab2 == t)) |
                                    ((Acab2 == t) & (Acab1 == t))]['QTD'].sum() > 0:
                        self.lco.loc[(((Acab1 == t) & (Acab2 == t)) |
                                     ((Acab2 == t) & (Acab1 == t))), 'PRIORIDADE'] = prioridade
                        prioridade += 1

                    continue

                except:
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
                if not self.headless:
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
        try:
            self.DefinePrioridades()
        except Exception as e:
            logger.logError("Erro ao definir as prioridades no algoritmo de Priorização de PDS.    -    Details: {}".format(str(e)))

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
                                                  TEMP.PK_RCQ = PDS.PK_RCQ);""")

        curLocal.execute("DROP TABLE tempTabelaOrdenada;")

        self.connLocal.commit()

        curLocal.close()
        self.connLocal.close()

    def OrdenaLista(self):
        try:
            self.RegistraOrdenacaoNoBanco()
        except Exception as e:
            logger.logError("Erro ao registrar a lista já priorizada no banco de dados local.    -    Details: {}".format(str(e)))

        # self.ExibeResultados()

        if not self.headless:
            self.master.destroy()

