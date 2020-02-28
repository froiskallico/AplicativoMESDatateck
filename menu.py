#--- Imports ---#
import atualiza_bdlocal
import pandas as pd
from tkinter import *
from tkinter import ttk
import configparser as cfgprsr
import os
import logger
import banco
#import priorizacao_pds as priori

class Menu:
    def __init__(self, parent, master=None):
        self.parent = parent
        self.master = master
        self.diretorio = os.path.dirname(os.path.abspath(__file__))
        self.virtualNumPadVisible = False

        self.configFile = cfgprsr.ConfigParser()

        self.configFile.read(self.diretorio + '/config.ini')
        self.maquina = self.configFile['DEFAULT']['maquina']
        self.limiteHorizonte = self.configFile['DEFAULT']['limite horizonte']
        self.limiteCircuitos = self.configFile['DEFAULT']['limitediariocircuitos']
        self.maquinaAutomatica = self.configFile['DEFAULT']['MaqAutomatica']
        self.loadMode = self.configFile['DEFAULT']['filtraLista']

        def montaTela():
            def montaFrames():
                ##--- Cabecalho ----##
                self.containerCabecalho = Frame(self.master,
                                                bd=5,
                                                bg=Cores.bgCinza)
                self.containerCabecalho["padx"] = 5
                self.containerCabecalho.pack(fill=X,
                                             side=TOP)

                ##--- Menu Botoes ---##
                self.containerBotoes = Frame(self.master,
                                             bg=Cores.bgCinza)
                self.containerBotoes["padx"] = 0
                self.containerBotoes["pady"] = 10
                self.containerBotoes.pack(side=RIGHT,
                                          fill=Y,
                                          expand=0)

                ##--- Esquerda ---##
                self.containerEsquerda = Frame(self.master,
                                               bg=Cores.bgCinza)
                self.containerEsquerda.pack(side=TOP,
                                            fill=BOTH,
                                            expand=1,
                                            pady=5,
                                            padx=70)

                # --- Rodape ---###
                self.contRodapemenu = Frame(self.master,
                                             bg=Cores.bgCinza)
                self.contRodapemenu.pack(side=BOTTOM,
                                          anchor=SW,
                                          fill=X,
                                          expand=1)

            def carregaImagens():
                self.logoDtkImg = PhotoImage(
                    file=self.diretorio + "/src/images/logos/logo.png")
                self.logoTriImg = PhotoImage(
                    file=self.diretorio + "/src/images/logos/logoTri.png")
                self.redParadaButton = PhotoImage(
                    file=self.diretorio + "/src/images/buttons/redButtons/paradaButton.png")
                self.inactiveMenuButton = PhotoImage(
                    file=self.diretorio + "/src/images/buttons/inactiveButtons/menuButton.png")
                self.redSairButton = PhotoImage(
                    file=self.diretorio + "/src/images/buttons/sairButton.png")
                self.activeConfirmarButton = PhotoImage(
                    file=self.diretorio + "/src/images/buttons/activeButtons/confirmarButton.png")
                self.logoutButton = PhotoImage(
                    file=self.diretorio + "/src/images/buttons/logoutButton.png")

            def montaBotoes():
                def destroyScreens():
                    self.master.destroy()
                    if self.virtualNumPadVisible:
                        self.popUpVNumPad.destroy()
                        self.virtualNumPadVisible = False

                # --- Botões ---#
                self.btnMenu = Button(self.containerBotoes,
                                      image=self.inactiveMenuButton,
                                      width=130,
                                      height=50,
                                      bg=Cores.bgCinza,
                                      relief=FLAT,
                                      anchor="w",
                                      bd=0,
                                      highlightthickness=0)
                self.btnMenu.image = self.inactiveMenuButton
                # self.btnMenu["command"] =
                self.btnMenu.pack(pady=5)

                self.btnSair = Button(self.containerBotoes,
                                      image=self.redSairButton,
                                      width=130,
                                      height=50,
                                      bg=Cores.bgCinza,
                                      relief=FLAT,
                                      anchor="w",
                                      bd=0,
                                      highlightthickness=0)
                self.btnSair["command"] = (lambda: destroyScreens())
                self.btnSair.image = self.redSairButton
                self.btnSair.pack(pady=5)

                self.btnLogout = Button(self.containerBotoes,
                                      image=self.logoutButton,
                                      width=130,
                                      height=50,
                                      bg=Cores.bgCinza,
                                      relief=FLAT,
                                      anchor="w",
                                      bd=0,
                                      highlightthickness=0)
                self.btnLogout["command"] = (lambda: os.system('sudo pkill -9 python && sudo systemctl restart app'))
                self.btnLogout.image = self.logoutButton
                self.btnLogout.pack(pady=5)

                self.btnConfirmar = Button(self.contRodapemenu,
                                           image=self.activeConfirmarButton,
                                           bg=Cores.bgCinza,
                                           relief=FLAT,
                                           bd=0,
                                           highlightthickness=0)
                self.btnConfirmar.image = self.activeConfirmarButton
                self.btnConfirmar['command'] = self.registraAlteracoes
                self.btnConfirmar.pack(side=BOTTOM,
                                       fill=Y,
                                       expand=1,
                                       pady=10)

            def montaWidgets():
                def montaLimites():
                    try:
                        desmontaOrdensEntry()
                    except:
                        pass

                    self.lblLimiteCircuitos = Label(self.containerEsquerda,
                                                    text='Limite Diário de Circuitos:',
                                                    font=Fontes.fontePadraoBold,
                                                    bg=Cores.bgCinza,
                                                    fg='white')
                    self.lblLimiteCircuitos.grid(row=2,
                                                 column=0,
                                                 pady=10,
                                                 padx=10)

                    self.scrLimiteCircuitos = Scale(self.containerEsquerda,
                                                    orient=HORIZONTAL,
                                                    width=50,
                                                    from_=500,
                                                    to=20000,
                                                    resolution=500,
                                                    font=Fontes.fontePadraoBold,
                                                    bg=Cores.bgCinza,
                                                    fg=Cores.bgVerde,
                                                    bd=0,
                                                    highlightthickness=0)
                    self.scrLimiteCircuitos.grid(row=2,
                                                 column=1,
                                                 columnspan=2,
                                                 pady=10,
                                                 sticky='we')
                    self.scrLimiteCircuitos.set(self.limiteCircuitos)

                    self.lblLimiteHorizonte = Label(self.containerEsquerda,
                                                    text='Limite Horizonte de Dias:',
                                                    font=Fontes.fontePadraoBold,
                                                    bg=Cores.bgCinza,
                                                    fg='white')
                    self.lblLimiteHorizonte.grid(row=3,
                                                 column=0,
                                                 pady=10,
                                                 padx=10)

                    self.scrLimiteHorizonte = Scale(self.containerEsquerda,
                                                    orient=HORIZONTAL,
                                                    width=50,
                                                    from_=1,
                                                    to=30,
                                                    resolution=1,
                                                    font=Fontes.fontePadraoBold,
                                                    bg=Cores.bgCinza,
                                                    fg=Cores.bgVerde,
                                                    bd=0,
                                                    highlightthickness=0)
                    self.scrLimiteHorizonte.grid(row=3,
                                                 column=1,
                                                 columnspan=2,
                                                 pady=10,
                                                 sticky='we')
                    self.scrLimiteHorizonte.set(self.limiteHorizonte)

                    self.lblMaqAuto = Label(self.containerEsquerda,
                                            text='Sequenciamento  de Setups:',
                                            font=Fontes.fontePadraoBold,
                                            bg=Cores.bgCinza,
                                            fg='white')
                    self.lblMaqAuto.grid(row=4,
                                         column=0,
                                         pady=10,
                                         padx=10)

                    self.varMaqAuto = StringVar()
                    self.varMaqAuto.set(self.maquinaAutomatica)

                    self.selSeqCabo = Radiobutton(self.containerEsquerda,
                                                  text="Por Cabo",
                                                  indicatoron=0,
                                                  bg=Cores.bgCinza,
                                                  fg='white',
                                                  activeforeground=Cores.letraVerde,
                                                  selectcolor=Cores.bgVerde,
                                                  width=15,
                                                  height=2,
                                                  font=Fontes.fontePadrao,
                                                  variable=self.varMaqAuto,
                                                  value='False')
                    self.selSeqCabo.grid(row=4,
                                         column=1,
                                         pady=10,
                                         sticky='we')

                    self.selSeqAcab = Radiobutton(self.containerEsquerda,
                                                  text="Por Acabamento",
                                                  indicatoron=0,
                                                  bg=Cores.bgCinza,
                                                  fg='white',
                                                  activeforeground=Cores.letraVerde,
                                                  selectcolor=Cores.bgVerde,
                                                  width=15,
                                                  height=2,
                                                  font=Fontes.fontePadrao,
                                                  variable=self.varMaqAuto,
                                                  value='True')
                    self.selSeqAcab.grid(row=4,
                                         column=2,
                                         pady=10,
                                         sticky='we')

                def desmontaLimites():
                    self.lblLimiteCircuitos.grid_forget()
                    self.scrLimiteCircuitos.grid_forget()
                    self.lblLimiteHorizonte.grid_forget()
                    self.scrLimiteHorizonte.grid_forget()
                    self.lblMaqAuto.grid_forget()
                    self.selSeqCabo.grid_forget()
                    self.selSeqAcab.grid_forget()

                def montaOrdensEntry():
                    try:
                        desmontaLimites()
                    except:
                        pass

                    self.lblNrListas = Label(self.containerEsquerda,
                                             text='Ordens de Corte:',
                                             font=Fontes.fontePadraoBold,
                                             bg=Cores.bgCinza,
                                             fg='white')
                    self.lblNrListas.grid(row=2,
                                          column=0,
                                          pady=10,
                                          padx=10)

                    self.entryNrListas = Entry(self.containerEsquerda,
                                               width=10,
                                               bg='lightcyan2',
                                               disabledbackground='dark slate gray',
                                               font=Fontes.fonteCabecalho,
                                               justify=LEFT)
                    self.entryNrListas.grid(row=2,
                                            column=1,
                                            columnspan=2,
                                            sticky='we',
                                            pady=10,
                                            padx=10)
                    self.entryNrListas.bind("<Button-1>",
                                             lambda x:
                                             self.virtualNumPad(
                                                 self.entryNrListas))

                    self.lblMaqAuto = Label(self.containerEsquerda,
                                            text='Sequenciamento  de Setups:',
                                            font=Fontes.fontePadraoBold,
                                            bg=Cores.bgCinza,
                                            fg='white')
                    self.lblMaqAuto.grid(row=4,
                                         column=0,
                                         pady=10,
                                         padx=10)

                    self.varMaqAuto = StringVar()
                    self.varMaqAuto.set(self.maquinaAutomatica)

                    self.selSeqCabo = Radiobutton(self.containerEsquerda,
                                                  text="Por Cabo",
                                                  indicatoron=0,
                                                  bg=Cores.bgCinza,
                                                  fg='white',
                                                  activeforeground=Cores.letraVerde,
                                                  selectcolor=Cores.bgVerde,
                                                  width=15,
                                                  height=2,
                                                  font=Fontes.fontePadrao,
                                                  variable=self.varMaqAuto,
                                                  value='False')
                    self.selSeqCabo.grid(row=4,
                                         column=1,
                                         pady=10,
                                         sticky='we')

                    self.selSeqAcab = Radiobutton(self.containerEsquerda,
                                                  text="Por Acabamento",
                                                  indicatoron=0,
                                                  bg=Cores.bgCinza,
                                                  fg='white',
                                                  activeforeground=Cores.letraVerde,
                                                  selectcolor=Cores.bgVerde,
                                                  width=15,
                                                  height=2,
                                                  font=Fontes.fontePadrao,
                                                  variable=self.varMaqAuto,
                                                  value='True')
                    self.selSeqAcab.grid(row=4,
                                         column=2,
                                         pady=10,
                                         sticky='we')

                def desmontaOrdensEntry():
                    try:
                        self.popUpVNumPad.destroy()
                    except:
                        pass


                ##------ Cabeçalho ------##
                self.logoDtk = Label(self.containerCabecalho,
                                  text="Datateck",
                                  font=["Play", 20, "bold"],
                                  image=self.logoDtkImg,
                                  bg=Cores.bgCinza,
                                  fg="white")
                self.logoDtk.image = self.logoDtkImg
                self.logoDtk.pack(side=LEFT)

                self.lblMenu = Label(self.containerCabecalho,
                                     text='Menu de Configurações',
                                     font=["Play", 20, "bold"],
                                     bg=Cores.bgCinza,
                                     fg="white")
                self.lblMenu.pack(side=LEFT,
                                  fill=BOTH,
                                  expand=1)


                ##------ Widgets Menu ------##
                self.lblMaquina = Label(self.containerEsquerda,
                                        text='Máquina: ',
                                        font=Fontes.fontePadraoBold,
                                        bg=Cores.bgCinza,
                                        fg='white')
                self.lblMaquina.grid(row=0,
                                     column=0,
                                     pady=10,
                                     padx=10)

                self.cboMaquina = ttk.Combobox(self.containerEsquerda,
                                               # style="mystyle.Combobox",
                                               font=('Play', 24),
                                               values=Variaveis.maquinas)
                self.cboMaquina.grid(row=0,
                                     column=1,
                                     columnspan=2,
                                     pady=10,
                                     sticky='we')

                self.cboMaquina.set(self.maquina)

                self.lblLoadMode = Label(self.containerEsquerda,
                                         text='Modo de Carregamento de Lista:',
                                         font=Fontes.fontePadraoBold,
                                         bg=Cores.bgCinza,
                                         fg='white')
                self.lblLoadMode.grid(row=1,
                                      column=0,
                                      pady=10,
                                      padx=10)

                self.varLoadMode = StringVar()
                self.varLoadMode.set(self.loadMode)

                self.selModoAuto = Radiobutton(self.containerEsquerda,
                                               text="Automático",
                                               indicatoron=0,
                                               bg=Cores.bgCinza,
                                               fg='white',
                                               activeforeground=Cores.letraVerde,
                                               selectcolor=Cores.bgVerde,
                                               width=15,
                                               height=2,
                                               font=Fontes.fontePadrao,
                                               variable=self.varLoadMode,
                                               value='False',
                                               command=montaLimites)
                self.selModoAuto.grid(row=1,
                                      column=1,
                                      pady=10,
                                      sticky='we')

                self.selModoLista = Radiobutton(self.containerEsquerda,
                                                text="Por Ordens de Corte",
                                                indicatoron=0,
                                                bg=Cores.bgCinza,
                                                fg='white',
                                                activeforeground=Cores.letraVerde,
                                                selectcolor=Cores.bgVerde,
                                                width=15,
                                                height=2,
                                                font=Fontes.fontePadrao,
                                                variable=self.varLoadMode,
                                                value='True',
                                                command=montaOrdensEntry)
                self.selModoLista.grid(row=1,
                                       column=2,
                                       pady=10,
                                       sticky='we')


                if self.varLoadMode.get() == 'True':
                    montaOrdensEntry()
                else:
                    montaLimites()

                self.mensagemMenu = StringVar()

                self.lblMsgMenu = Label(self.contRodapemenu,
                                        textvariable=self.mensagemMenu,
                                        font=Fontes.fontePadraoBold,
                                        bg=Cores.bgCinza,
                                        fg='limegreen')
                self.lblMsgMenu.pack(side=TOP,
                                     fill=X,
                                     expand=1)

                self.logoTri = Label(self.containerBotoes,
                                     text="Powered by TRI",
                                     image=self.logoTriImg,
                                     bg=Cores.bgCinza,
                                     fg="white",
                                     anchor='se')
                self.logoTri.image = self.logoTriImg
                self.logoTri.pack(side=BOTTOM,
                                  pady=5,
                                  anchor='w')

            montaFrames()
            carregaImagens()
            montaBotoes()
            montaWidgets()
        montaTela()

    def registraAlteracoes(self):
        if self.virtualNumPadVisible:
            self.popUpVNumPad.destroy()
            self.virtualNumPadVisible = False

        self.mensagemMenu.set("Por favor aguarde enquanto as configurações são salvas")
        self.master.update()

        self.configFile.set('DEFAULT',
                            'maquina',
                            str(self.cboMaquina.get()))
        self.configFile.set('DEFAULT',
                            'filtralista',
                            str(self.varLoadMode.get()))
        self.configFile.set('DEFAULT',
                            'maqautomatica',
                            str(self.varMaqAuto.get()))

        if self.varLoadMode.get() == 'True':
            self.configFile.set('DEFAULT',
                                'ordens',
                                '({})'.format(str(self.entryNrListas.get())))

        else:
            self.configFile.set('DEFAULT',
                                'limite horizonte',
                                str(self.scrLimiteHorizonte.get()))
            self.configFile.set('DEFAULT',
                                'limitediariocircuitos',
                                str(self.scrLimiteCircuitos.get()))


        with open(self.diretorio + '/config.ini', 'w') as configfile:
            self.configFile.write(configfile)


        try:
            atualiza_bdlocal.AtualizaBancoLocal()
            #priori.AlgoritmoSeparacao(headless=True)

            self.parent.limpaTela()
            self.parent.montaTelaPrincipal()
            self.master.destroy()
        except Exception as e:
            self.configFile.set('DEFAULT', 'filtralista', 'False')

            with open(self.diretorio + '/config.ini', 'w') as configfile:
                self.configFile.write(configfile)

            self.mensagemMenu.set('Erro. Verifique as configurações')
            self.lblMsgMenu['fg'] = 'red'

            logger.logError("Erro ao salver as configurações do Menu.    -    Details: {}".format(str(e)))

    def virtualNumPad(self, parent):
        parent.configure(bg='lightgreen')
        parent.delete(0, END)
        self.mensagemMenu.set('')

        if self.virtualNumPadVisible:
            self.popUpVNumPad.destroy()
            self.virtualNumPadVisible = False
            self.virtualNumPad(parent)

        elif not self.virtualNumPadVisible:
            self.virtualNumPadVisible = True

            self.popUpVNumPad = Toplevel(bg=Cores.bgCinza,
                                         bd=7,
                                         relief=RAISED)
            self.popUpVNumPad.overrideredirect(1)
            self.popUpVNumPad.attributes('-topmost', 'true')
            self.popUpVNumPad.bind('<Escape>',
                                   lambda e: self.popUpVNumPad.destroy())
            self.popUpVNumPad.geometry('+5+260')
            self.popUpVNumPad.focus()

            containerNumPad = Frame(self.popUpVNumPad,
                                    bg=Cores.bgCinza)
            containerNumPad.pack(side=TOP)

            listaDeTeclas = [
                ['1', '2', '3'],
                ['4', '5', '6'],
                ['7', '8', '9'],
                [',', '0', '<']
            ]

            containerNumPadLinha = list(range(len(listaDeTeclas)))

            for linha in containerNumPadLinha:
                containerNumPadLinha[linha] = Frame(containerNumPad,
                                                    bg=Cores.bgCinza)
                containerNumPadLinha[linha].pack(side=TOP)

                teclas = list(range(len(listaDeTeclas[linha])))

                for tecla in teclas:
                    cmd = lambda x = listaDeTeclas[linha][tecla]: kp(self,
                                                                     x,
                                                                     parent)

                    teclas[tecla] = Button(containerNumPadLinha[linha],
                                           text=listaDeTeclas[linha][tecla],
                                           width=5,
                                           height=3,
                                           relief=RIDGE,
                                           bd=2,
                                           bg='black',
                                           fg='white',
                                           font=Fontes.fontePadraoBold,
                                           command=cmd)
                    teclas[tecla].pack(side=LEFT,
                                       padx=1,
                                       pady=1)

        def kp(self, keyValue, parent):
            if keyValue == "<":
                parent.delete(len(parent.get()) - 1, END)
            else:
                parent.insert(END, keyValue)


class Variaveis:
    def BuscaMaquinas():
        bdGlobal = banco.GLOBAL_DATABASE().conexao

        lista = pd.read_sql_query("SELECT DESCRICAO FROM MAQUINAS",
                                  bdGlobal)
        return lista['DESCRICAO'].tolist()

    maquinas = BuscaMaquinas()


class Fontes:
    fontePadrao = ("Play", 12)
    fontePadraoBold = ("Play", 12, "bold")
    fonteCabecalho = ("Play", 24, "bold")
    fonteQuantidadePendente = ("Play", 32, "bold")
    fonteQuantidadeCortada = ("Play", 16, "bold")


class Cores:
    bgCinza = "#333333"
    bgVerde = "#00D455"
    letraVerde = "#66FF00"
    bgAcabamentosAux = "#CCC"
    bgRodape = "#454545"
