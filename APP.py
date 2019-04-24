# --- Imports ---#
from pd import PD
from tkinter import *
from time import sleep, time
from tkinter import ttk
# import login
import configparser as cfgprsr


class Definicoes():
    configFile = cfgprsr.ConfigParser()
    configFile.read('config.ini')
    maquina = configFile['DEFAULT']['Maquina']
    

root = Tk()
root.title('Operação')
root.geometry(Definicoes.configFile['DISPLAY']['RES'])
root.attributes('-fullscreen',
                Definicoes.configFile['DISPLAY']['Tela Cheia'])
root.bind('<Escape>', lambda e: root.destroy())
root.resizable(width=True, height=True)


class Variaveis():
    ID = StringVar()
    REQNUM = StringVar()
    PDNUM = StringVar()
    PAI = StringVar()
    DECAPEA = StringVar()
    DECAPEB = StringVar()
    MEDIDA = StringVar()
    CABO = StringVar()
    QUANTIDADE = StringVar()
    QUANTIDADE_CORTADA = StringVar()
    ACAB1 = StringVar()
    ACAB2 = StringVar()
    ACAB3 = StringVar()
    ACAB4 = StringVar()
    OBSERVACAO = StringVar()
    GRAVACAO = StringVar()
    PROX_CABO = StringVar()
    PROX_DECAPEA = StringVar()
    PROX_MEDIDA = StringVar()
    PROX_DECAPEB = StringVar()


class Fontes():
    fontePadrao = ("Play", 12)
    fonteCabecalho = ("Play", 18, "bold")
    fonteQuantidadePendente = ("Play", 32, "bold")
    fonteQuantidadeCortada = ("Play", 16, "bold")


class Cores():
    # Cores padrão do aplicativo
    bgCorDoCabo = "white"
    bgCinza = "#333333"
    bgVerde = "#00D455"
    letraVerde = "#66FF00"
    bgAcabamentosAux = "#CCC"
    bgRodape = "#454545"
    bgCobre = "#ff9955"

class Imagens():
    # --- IMAGENS ---#
    logo = PhotoImage(
        file="src/images/logos/logo.png")
    startButton = PhotoImage(
        file="src/images/buttons/startButton.png")
    stopButton = PhotoImage(
        file="src/images/buttons/stopButton.png")
    searchButton = PhotoImage(
        file="src/images/buttons/searchButton.png")
    setupStartButton = PhotoImage(
        file="src/images/buttons/setupStartButton.png")
    setupStopButton = PhotoImage(
        file="src/images/buttons/setupStopButton.png")
    pularButton = PhotoImage(
        file="src/images/buttons/pularButton.png")
    paradaButton = PhotoImage(
        file="src/images/buttons/paradaButton.png")
    retomarButton = PhotoImage(
        file="src/images/buttons/retomarButton.png")
    menuButton = PhotoImage(
        file="src/images/buttons/menuButton.png")


class Application:

    # --- Inicialização do Aplicativo --- #
    def __init__(self, master=None):
        # Log = LOGIN.sts
        # if Log == True:
        self.montaTelaPrincipal()
        self.montaLista()

    # --- Geração do Layout Principal --- #
    def montaTelaPrincipal(self, master=None):
        self.montaContainers()
        self.montaLabels()
        self.montaBotoes()

    def montaContainers(self, master=None):
        ##--- Cabecalho ----##
        self.containerCabecalho = Frame(master,
                                        bd=5,
                                        bg=Cores.bgCinza)
        self.containerCabecalho["padx"] = 5
        self.containerCabecalho.pack(fill=X,
                                     side=TOP)

        ##--- Menu Botoes ---##
        self.containerBotoes = Frame(master,
                                     bg=Cores.bgCinza)
        self.containerBotoes["padx"] = 0
        self.containerBotoes["pady"] = 10
        self.containerBotoes.pack(side=RIGHT,
                                  fill=Y,
                                  expand=0)

        ##--- Esquerda ---##
        self.containerEsquerda = Frame(master,
                                       bg=Cores.bgCinza)
        self.containerEsquerda.pack(side=LEFT,
                                    fill=BOTH,
                                    expand=1)

        ###--- Dados PD ---###
        self.containerDadosPD = Frame(self.containerEsquerda,
                                      bg=Cores.bgCinza)
        self.containerDadosPD.pack(fill=BOTH,
                                   expand=1,
                                   padx=(0, 20))

        ####--- Cabecalho PD ---####
        self.containerCabecalhoPD = Frame(self.containerDadosPD,
                                          bg=Cores.bgCinza)
        self.containerCabecalhoPD.pack(fill=X,
                                       pady=(20, 35),
                                       padx=20)

        ####--- Medidas PD ---####
        self.containerMedidasPD = Frame(self.containerDadosPD,
                                        bg=Cores.bgCinza)
        self.containerMedidasPD.pack()

        ####--- Cabo ---###
        self.containerCabo = Frame(self.containerDadosPD,
                                   bg=Cores.bgCinza)
        self.containerCabo.pack()

        ####--- Detalhes PD ---####
        self.containerDetalhesPD = Frame(self.containerDadosPD,
                                         bg=Cores.bgCinza)
        self.containerDetalhesPD.pack(fill=X,
                                      expand=1)

        #####--- Acabamentos Lado A ---#####
        self.containerLadoA = Frame(self.containerDetalhesPD,
                                    bg=Cores.bgCinza)
        self.containerLadoA.pack(side=LEFT)

        ######--- Acabamento 1 ---######
        self.containerAcabamento1 = Frame(self.containerLadoA,
                                          bg=Cores.bgVerde)
        self.containerAcabamento1.pack(side=TOP,
                                       pady=10)

        ######--- Acabamento 3 ---######
        self.containerAcabamento3 = Frame(self.containerLadoA,
                                          bg=Cores.bgAcabamentosAux)
        self.containerAcabamento3.pack(side=TOP)

        #####--- Detalhes Meio ---#####
        self.containerDetalhesMeio = Frame(self.containerDetalhesPD,
                                           bg=Cores.bgCinza)
        self.containerDetalhesMeio.pack(side=LEFT,
                                        fill=X,
                                        expand=1)

        ######--- Quantidade ---######
        self.containerQuantidade = Frame(self.containerDetalhesMeio,
                                         bg=Cores.bgCinza)
        self.containerQuantidade.pack(fill=BOTH,
                                      expand=1)

        ######--- Observação ---######
        self.containerObservacao = Frame(self.containerDetalhesMeio,
                                         bg=Cores.bgCinza)
        self.containerObservacao.pack(fill=X,
                                      expand=1)

        ######--- Gravação ---######
        self.containerGravacao = Frame(self.containerDetalhesMeio,
                                       bg=Cores.bgCinza)
        self.containerGravacao.pack(fill=X,
                                    expand=1)

        #####--- Acabamentos Lado B ---#####
        self.containerLadoB = Frame(self.containerDetalhesPD,
                                    bg=Cores.bgCinza)
        self.containerLadoB.pack(side=RIGHT)

        ######--- Acabamento 2 ---######
        self.containerAcabamento2 = Frame(self.containerLadoB,
                                          bg=Cores.bgVerde)
        self.containerAcabamento2.pack(side=TOP,
                                       pady=10)

        ######--- Acabamento 4 ---######
        self.containerAcabamento4 = Frame(self.containerLadoB,
                                          bg=Cores.bgAcabamentosAux)
        self.containerAcabamento4.pack(side=TOP)

        ###--- Rodape ---###
        self.containerRodape = Frame(self.containerEsquerda,
                                     bg=Cores.bgRodape)
        self.containerRodape.pack(side=BOTTOM,
                                  ipadx=100)

        ####--- Proximo Cabo ---####
        self.containerProxCabo = Frame(self.containerRodape,
                                       bg=Cores.bgRodape)
        self.containerProxCabo.pack(side=TOP,
                                    fill=X,
                                    expand=1)

        ####--- Label Prox Medidas ---####
        self.containerProxMedidas = Frame(self.containerRodape,
                                          bg=Cores.bgRodape)
        self.containerProxMedidas.pack()

    def montaLabels(self, master=None):
        ##------ Cabeçalho ------##
        self.logo = Label(self.containerCabecalho,
                          text="Datateck",
                          font=Fontes.fonteCabecalho,
                          image=Imagens.logo,
                          bg=Cores.bgCinza,
                          fg="white")
        self.logo.pack(side=LEFT)

        self.maquina = Label(self.containerCabecalho,
                             text=Definicoes.maquina,
                             font=Fontes.fonteCabecalho,
                             bg=Cores.bgCinza,
                             fg="white")
        self.maquina.pack(side=LEFT, 
                          fill=X, 
                          expand=1)

        self.relogio = Label(self.containerCabecalho, 
                             text="00:00:00",
                             font=Fontes.fonteCabecalho,
                             padx=10,
                             fg=Cores.letraVerde, 
                             bg=Cores.bgCinza)
        self.relogio.pack(side=LEFT)

        ##--- Dados PD ---##
        ###--- Cabecalho PD ---###
        self.lblRequisicao = Label(self.containerCabecalhoPD,
                            text="Requisição: %s" % (Variaveis.REQNUM.get()),
                            font=Fontes.fontePadrao,
                            bg=Cores.bgCinza,
                            fg="white",
                            anchor="w")
        self.lblRequisicao.pack(side=LEFT)

        self.lblPD = Label(self.containerCabecalhoPD,
                           text="PD: %s" % Variaveis.PDNUM.get(),
                           font=Fontes.fonteCabecalho,
                           bg=Cores.bgCinza,
                           fg=Cores.letraVerde,
                           anchor="center")
        self.lblPD.pack(side=LEFT,
                        fill=X,
                        expand=1)

        self.lblProdutoFinal = Label(self.containerCabecalhoPD,
                            text="Produto Final: %s" % Variaveis.PAI.get(),
                            font=Fontes.fontePadrao,
                            bg=Cores.bgCinza,
                            fg="white",
                            anchor="e")
        self.lblProdutoFinal.pack(side=LEFT)

        ###--- Medidas PD ---###
        self.lblDecapeA = Label(self.containerMedidasPD,
                                text=Variaveis.DECAPEA.get(),
                                font=Fontes.fonteCabecalho,
                                bg=Cores.bgCinza,
                                fg=Cores.letraVerde)
        self.lblDecapeA.grid(column=0,
                             row=0)

        self.lblMedida = Label(self.containerMedidasPD,
                               text=Variaveis.MEDIDA.get(),
                               font=Fontes.fonteCabecalho,
                               bg=Cores.bgCinza,
                               fg=Cores.letraVerde,
                               width=30)
        self.lblMedida.grid(column=1,
                            row=0)

        self.lblDecapeB = Label(self.containerMedidasPD,
                                text=Variaveis.DECAPEB.get(),
                                font=Fontes.fonteCabecalho,
                                bg=Cores.bgCinza,
                                fg=Cores.letraVerde)
        self.lblDecapeB.grid(column=2,
                             row=0)

        ###--- Cabo ---###
        self.lblLadoACabo = Label(self.containerCabo,
                                  text="",
                                  bg=Cores.bgCobre,
                                  width=10,
                                  height=1)
        self.lblLadoACabo.grid(column=0,
                               row=0)

        self.lblCabo = Label(self.containerCabo,
                             text=Variaveis.CABO.get(),
                             font=Fontes.fontePadrao,
                             bg=Cores.bgCorDoCabo,
                             fg=Cores.bgCinza,
                             width=40,
                             height=2)
        self.lblCabo.grid(column=1,
                          row=0)

        self.lblLadoBCabo = Label(self.containerCabo,
                                  text="",
                                  bg=Cores.bgCobre,
                                  width=10,
                                  height=1)
        self.lblLadoBCabo.grid(column=2,
                               row=0)

        ###--- Detalhes ---###
        ####--- Lado A ---####
        #####--- Acabamento 1 ---#####
        self.lblLabelAcabamento1 = Label(self.containerAcabamento1,
                                         text="Acabamento 1",
                                         font=Fontes.fontePadrao,
                                         bg=Cores.bgVerde,
                                         fg=Cores.bgCinza,
                                         width=20)
        self.lblLabelAcabamento1.pack(fill=BOTH,
                                      expand=1,
                                      pady=5)

        self.lblAcabamento1 = Label(self.containerAcabamento1,
                                    text=Variaveis.ACAB1.get(),
                                    font=Fontes.fontePadrao,
                                    bg=Cores.bgVerde,
                                    fg=Cores.bgCinza)
        self.lblAcabamento1.pack(fill=BOTH,
                                 expand=1,
                                 pady=5)

        #####--- Acabamento 3 ---#####
        self.lblLabelAcabamento3 = Label(self.containerAcabamento3,
                                         text="Acabamento 3",
                                         font=Fontes.fontePadrao,
                                         bg=Cores.bgAcabamentosAux,
                                         fg=Cores.bgCinza,
                                         width=20)
        self.lblLabelAcabamento3.pack(fill=BOTH,
                                      expand=1,
                                      pady=5)

        self.lblAcabamento3 = Label(self.containerAcabamento3,
                                    text=Variaveis.ACAB3.get(),
                                    font=Fontes.fontePadrao,
                                    bg=Cores.bgAcabamentosAux,
                                    fg=Cores.bgCinza)
        self.lblAcabamento3.pack(fill=BOTH,
                                 expand=1,
                                 pady=5)

        ####--- Quantidade ---####
        self.lblLabelQuantidade = Label(self.containerQuantidade,
                                        text="Quantidade",
                                        font=Fontes.fonteCabecalho,
                                        bg=Cores.bgCinza,
                                        fg=Cores.letraVerde)
        self.lblLabelQuantidade.pack()

        self.lblQuantidadePendente = Label(self.containerQuantidade,
                                           text=Variaveis.QUANTIDADE.get(),
                                           font=Fontes.fonteQuantidadePendente,
                                           bg=Cores.bgCinza,
                                           fg=Cores.letraVerde,
                                           anchor="ne")
        self.lblQuantidadePendente.pack()

        self.lblQuantidadeCortada = Label(self.containerQuantidade,
                                          text=Variaveis.QUANTIDADE_CORTADA.get(),
                                          font=Fontes.fonteQuantidadeCortada,
                                          bg=Cores.bgCinza,
                                          fg="red",
                                          anchor="sw")
        # self.lblQuantidadeCortada.bind("<Button-1>",
        #                                self.informarQuantidadeCortada)
        self.lblQuantidadeCortada.pack()

        ####--- Observacao ---####
        self.lblLabelObservacao = Label(self.containerObservacao,
                                        text="Observação",
                                        font=Fontes.fontePadrao,
                                        bg=Cores.bgCinza,
                                        fg=Cores.bgAcabamentosAux)
        self.lblLabelObservacao.pack()

        self.lblObservacao = Label(self.containerObservacao,
                                   text=Variaveis.OBSERVACAO.get(),
                                   font=Fontes.fontePadrao,
                                   bg=Cores.bgCinza,
                                   fg="white")
        self.lblObservacao.pack()

        ####--- Gravacao ---####
        self.lblLabelGravacao = Label(self.containerObservacao,
                                      text="Gravação",
                                      font=Fontes.fontePadrao,
                                      bg=Cores.bgCinza,
                                      fg=Cores.bgAcabamentosAux)
        self.lblLabelGravacao.pack()

        self.lblGravacao = Label(self.containerObservacao,
                                 text=Variaveis.GRAVACAO.get(),
                                 font=Fontes.fontePadrao,
                                 bg=Cores.bgCinza,
                                 fg="white")
        self.lblGravacao.pack()

        ####--- Labo B ---####
        #####--- Acabamento 2 ---#####
        self.lblLabelAcabamento2 = Label(self.containerAcabamento2,
                                         text="Acabamento 2",
                                         font=Fontes.fontePadrao,
                                         bg=Cores.bgVerde,
                                         fg=Cores.bgCinza,
                                         width=20)
        self.lblLabelAcabamento2.pack(fill=BOTH,
                                      expand=1,
                                      pady=5)

        self.lblAcabamento2 = Label(self.containerAcabamento2,
                                    text=Variaveis.ACAB2.get(),
                                    font=Fontes.fontePadrao,
                                    bg=Cores.bgVerde,
                                    fg=Cores.bgCinza)
        self.lblAcabamento2.pack(fill=BOTH,
                                 expand=1,
                                 pady=5)

        #####--- Acabamento 4 ---#####
        self.lblLabelAcabamento4 = Label(self.containerAcabamento4,
                                         text="Acabamento 4",
                                         font=Fontes.fontePadrao,
                                         bg=Cores.bgAcabamentosAux,
                                         fg=Cores.bgCinza,
                                         width=20)
        self.lblLabelAcabamento4.pack(fill=BOTH,
                                      expand=1,
                                      pady=5)

        self.lblAcabamento4 = Label(self.containerAcabamento4,
                                    text=Variaveis.ACAB4.get(),
                                    font=Fontes.fontePadrao,
                                    bg=Cores.bgAcabamentosAux,
                                    fg=Cores.bgCinza)
        self.lblAcabamento4.pack(fill=BOTH,
                                 expand=1,
                                 pady=5)

        # --- Rodape ---#
        self.lblProxCabo = Label(self.containerProxCabo,
                                 text=Variaveis.PROX_CABO.get(),
                                 bg=Cores.bgRodape,
                                 fg=Cores.bgAcabamentosAux)
        self.lblProxCabo.pack(side=TOP,
                              fill=X,
                              expand=1)

        self.lblLabelProxDecapeA = Label(self.containerProxMedidas,
                                         text="Decape A",
                                         bg=Cores.bgRodape,
                                         fg=Cores.bgAcabamentosAux)
        self.lblLabelProxDecapeA.grid(column=0,
                                      row=0)

        self.lblLabelProxMedida = Label(self.containerProxMedidas,
                                        text="Medida",
                                        bg=Cores.bgRodape,
                                        fg=Cores.bgAcabamentosAux,
                                        width=30)
        self.lblLabelProxMedida.grid(column=1,
                                     row=0)

        self.lblLabelProxDecapeB = Label(self.containerProxMedidas,
                                         text="Decape B",
                                         bg=Cores.bgRodape,
                                         fg=Cores.bgAcabamentosAux)
        self.lblLabelProxDecapeB.grid(column=2,
                                      row=0)

        self.lblProxDecapeA = Label(self.containerProxMedidas,
                                    text=Variaveis.PROX_DECAPEA.get(),
                                    bg=Cores.bgRodape,
                                    fg=Cores.bgAcabamentosAux)
        self.lblProxDecapeA.grid(column=0,
                                 row=1)

        self.lblProxMedida = Label(self.containerProxMedidas,
                                   text=Variaveis.PROX_MEDIDA.get(),
                                   bg=Cores.bgRodape,
                                   fg="#888")
        self.lblProxMedida.grid(column=1, row=1)

        self.lblProxDecapeB = Label(self.containerProxMedidas,
                                    text=Variaveis.PROX_DECAPEB.get(),
                                    bg=Cores.bgRodape,
                                    fg=Cores.bgAcabamentosAux)
        self.lblProxDecapeB.grid(column=2,
                                 row=1)

    def montaBotoes(self, master=None):
        # --- Botões ---#
        self.btnStart = Button(self.containerBotoes,
                               image=Imagens.startButton,
                               width=130,
                               height=50,
                               bg=Cores.bgCinza,
                               relief=FLAT,
                               anchor="w",
                               bd=0,
                               highlightthickness=0)
        # self.btnStart["command"] =
        self.btnStart.pack(pady=5)

        self.btnStop = Button(self.containerBotoes,
                              image=Imagens.stopButton,
                              width=130,
                              height=50,
                              bg=Cores.bgCinza,
                              relief=FLAT,
                              anchor="w",
                              bd=0,
                              highlightthickness=0)
        self.btnStop["command"] = self.stop
        self.btnStop.pack(pady=5)

        self.btnBusca = Button(self.containerBotoes,
                               image=Imagens.searchButton,
                               width=130,
                               height=50,
                               bg=Cores.bgCinza,
                               relief=FLAT,
                               anchor="w",
                               bd=0,
                               highlightthickness=0)
        self.btnBusca["command"] = self.montaLista
        self.btnBusca.pack(pady=5)

        self.btnPula = Button(self.containerBotoes,
                              image=Imagens.pularButton,
                              width=130,
                              height=50,
                              bg=Cores.bgCinza,
                              relief=FLAT,
                              anchor="w",
                              bd=0,
                              highlightthickness=0)
        # self.btnPula["command"] =
        self.btnPula.pack(pady=5)

        self.btnParada = Button(self.containerBotoes,
                                image=Imagens.paradaButton,
                                width=130,
                                height=50,
                                bg=Cores.bgCinza,
                                relief=FLAT,
                                anchor="w",
                                bd=0,
                                highlightthickness=0)
        # self.btnParada["command"] =
        self.btnParada.pack(pady=5)

        self.btnMenu = Button(self.containerBotoes,
                              image=Imagens.menuButton,
                              width=130,
                              height=50,
                              bg=Cores.bgCinza,
                              relief=FLAT,
                              anchor="w",
                              bd=0,
                              highlightthickness=0)
        # self.btnMenu["command"] =
        self.btnMenu.pack(pady=5)

    # --- Limpeza de Layouts --- #
    def limpaTela(self):
        for ele in root.winfo_children():
            ele.destroy()

    def limpaContainerEsquerda(self):
        for ele in self.containerEsquerda.winfo_children():
            ele.destroy()

    # --- Busca Lista de Corte --- #
    def montaLista(self):
        self.limpaContainerEsquerda()


        self.dataCols = ('Medida',
                         'Quantidade',
                         'Requisição',
                         'PD')


        self.containerEsquerda.grid_rowconfigure(0, weight=1)
        self.containerEsquerda.grid_columnconfigure(0, weight=1)
        self.containerEsquerda.configure(padx=15, pady=15)


        style = ttk.Style()
        style.configure("mystyle.Treeview",
                        highlightthickness=0,
                        bd=0,
                        font=("Calibri", 18),
                        rowheight=50)
        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 16, 'bold'))
        style.layout("mystyle.Treeview",
                     [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])


        self.vsb = ttk.Scrollbar(self.containerEsquerda,
                                 orient="vertical")
        self.hsb = ttk.Scrollbar(self.containerEsquerda,
                                 orient="horizontal")

        self.tvw = ttk.Treeview(self.containerEsquerda,
                                style="mystyle.Treeview",
                                columns=self.dataCols)

        self.tvw.heading("#0", text="Cabo/PD")

        self.vsb['command'] = self.tvw.yview
        self.hsb['command'] = self.tvw.xview

        self.listaCount = Label(self.containerEsquerda,
                                bg=Cores.bgCinza,
                                fg="white", 
                                font=Fontes.fontePadrao,
                                anchor=NE)
        self.listaCount.grid(column=0,
                             row=2,
                             sticky='ne')


        for field in self.dataCols:
            self.tvw.heading(field, text=str(field.title()))
            self.tvw.column(field, stretch=False, width=120)

        self.tvw.grid(column=0, row=0, sticky='nswe')
        self.vsb.grid(column=1, row=0, sticky='ns')
        self.hsb.grid(column=0, row=1, sticky='we')

        self.btnConfirma = Button(self.containerEsquerda,
                                  text="Carregar",
                                  font=Fontes.fonteCabecalho,
                                  bg=Cores.bgCinza,
                                  fg="white")
        self.btnConfirma.bind("<Button-1>", self.listaSelectBtn)
        self.btnConfirma.grid(column=0,
                              row=3,
                              ipadx=5)

        self.populaLista()

    def populaLista(self):
        pd = PD()
        pd.buscarPD(Definicoes.maquina)

        self.data = pd.info

        cabos = []
        for item in self.data:
            if item[3] not in cabos:
                cabos.append(str(item[3]))

        for cabo in cabos:
            self.tvw.insert('', 'end', cabo, text=cabo)

        print(cabos)

        for item in self.data:
            self.tvw.insert(item[3], 'end', text=item[3], values=(
                item[6], item[11], item[1], item[2], item[0]))

        self.listaCount.configure(text='Total de PDs: ' + str(len(self.data)))

    def listaSelectBtn(self, master=None):
        self.itemSel = self.tvw.focus()
        self.itemData = self.tvw.item(self.itemSel)

        print(self.itemData)

        Variaveis.ID.set(self.itemData.get('values')[4])
        Variaveis.REQNUM.set(self.itemData.get('values')[2])
        Variaveis.PDNUM.set(self.itemData.get('values')[3])
        Variaveis.PAI.set("-")
        Variaveis.DECAPEA.set("-")
        Variaveis.DECAPEB.set("-")
        Variaveis.MEDIDA.set(self.itemData.get('values')[0])
        Variaveis.CABO.set(self.itemData.get('text'))
        Variaveis.QUANTIDADE.set(self.itemData.get('values')[1])
        Variaveis.QUANTIDADE_CORTADA.set("-")
        Variaveis.ACAB1.set("-")
        Variaveis.ACAB2.set("-")
        Variaveis.ACAB3.set("-")
        Variaveis.ACAB4.set("-")
        Variaveis.OBSERVACAO.set("-")
        Variaveis.GRAVACAO.set("-")
        Variaveis.PROX_CABO.set("-")
        Variaveis.PROX_DECAPEA.set("-")
        Variaveis.PROX_MEDIDA.set("-")
        Variaveis.PROX_DECAPEB.set("-")

        for ele in root.winfo_children():
            ele.destroy()

        self.montaTelaPrincipal()

    def atualizaCronografo(self):
        if operando:
            tempoAtual = int(time() - tempoInicio)

            if tempoAtual % 1 == 0:
                QUANTIDADE_CORTADA.set(int(QUANTIDADE_CORTADA.get()) + 1)
                self.lblQuantidadeCortada.configure(
                    text=QUANTIDADE_CORTADA.get())

            if QUANTIDADE_CORTADA.get() == QUANTIDADE.get():
                self.stop()

            self.relogio.configure(text=tempoAtual)
            root.after(1000, self.atualizaCronografo)

    def stop(self):
        pd = PD()

        global operando

        if (operando):
            operando = False

        ##		  QUANTIDADE_CORTADA.set(QUANTIDADE.get())
        self.limpaTela()
        pd.atualizaQuantidadeCortada(ID.get(), QUANTIDADE_CORTADA.get())


Application(root)
root.mainloop()
