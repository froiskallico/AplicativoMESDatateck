# --- Imports ---#
from pd import PD
import tempos
from tkinter import *
from time import time
import datetime
from tkinter import ttk
# import login
import configparser as cfgprsr
import inspect

class Definicoes():
    configFile = cfgprsr.ConfigParser()
    configFile.read('config.ini')
    maquina = configFile['DEFAULT']['Maquina']


root = Tk()
root.title('Operação')
root.geometry(Definicoes.configFile['DISPLAY']['RES'])
root.attributes('-fullscreen', Definicoes.configFile['DISPLAY']['Tela Cheia'])
root.bind('<Escape>', lambda e: root.destroy())
root.resizable(width=True, height=True)


class Variaveis:
    inicioSecao = datetime.datetime.now().strftime('%d-%m-%Y  %H:%M:%S')
    idUsuarioLogado = 0
    nomeUsuarioLogado = None

    colunas = ('PK_IPC',
               'REQUISICAO',
               'CELULA',
               'DATA GERAÇÃO',
               'DATA ENTREGA',
               'OBSERVAÇÃO REQ',
               'CHICOTE',
               'QTD. CHICOTE PENDENTE',
               'PD',
               'CABO',
               'FK_CRS',
               'VIAS',
               'BITOLA',
               'UNIDADE',
               'QTD PD REQ',
               'MEDIDA',
               'DECAPE A',
               'DECAPE B',
               'ACABAMENTO 1',
               'PONTE 1',
               'ACABAMENTO 2',
               'PONTE 2',
               'ACABAMENTO 3',
               'PONTE 3',
               'ACABAMENTO 4',
               'PONTE 4',
               'OBSERVAÇÃO',
               'GRAVAÇÃO',
               'MÁQUINA',
               'NR. ORDEM CORTE',
               'DESCRICAO',
               'PRIMARIA',
               'SECUNDARIA',
               'COR_TEXTO')

    campos = {
        "PK_IPC":                   "",
        "REQUISICAO":               "",
        "CELULA":                   "",
        "DATA GERAÇÃO":             "",
        "DATA ENTREGA":             "",
        "OBSERVAÇÃO REQ":           "",
        "CHICOTE":                  "",
        "QTD. CHICOTE PENDENTE":    "",
        "PD":                       "",
        "CABO":                     "",
        "FK_CRS":                   "",
        "VIAS":                     "",
        "BITOLA":                   "",
        "UNIDADE":                  "",
        "QTD PD REQ":               "",
        "MEDIDA":                   "",
        "DECAPE A":                 "",
        "DECAPE B":                 "",
        "ACABAMENTO 1":             "",
        "PONTE 1":                  "",
        "ACABAMENTO 2":             "",
        "PONTE 2":                  "",
        "ACABAMENTO 3":             "",
        "PONTE 3":                  "",
        "ACABAMENTO 4":             "",
        "PONTE 4":                  "",
        "OBSERVAÇÃO":               "",
        "GRAVAÇÃO":                 "",
        "MÁQUINA":                  "",
        "NR. ORDEM CORTE":          "",
        "DESCRICAO":                "",
        "PRIMARIA":                 "",
        "SECUNDARIA":               "",
        "COR_TEXTO":                ""}

    estados = ('Ocioso', 
               'Carregado', 
               'Em Setup',
               'Preenchendo RQ',
               'Setup Finalizado',
               'Em Corte',
               'Corte Finalizado',
               'Parado')

    estadoEquipamento = 0
    t0 = 0
    ID = None

    RQPreenchido = False

    virtualNumPadVisible = False


class Fontes:
    fontePadrao = ("Play", 12)
    fontePadraoBold = ("Play", 12, "bold")
    fonteCabecalho = ("Play", 18, "bold")
    fonteQuantidadePendente = ("Play", 32, "bold")
    fonteQuantidadeCortada = ("Play", 16, "bold")


class Cores:
    bgCorDoCabo = "white"
    bgCorDaListra = "white"
    fgCorDoCabo = "#333333"
    bgCinza = "#333333"
    bgVerde = "#00D455"
    letraVerde = "#66FF00"
    bgAcabamentosAux = "#CCC"
    bgRodape = "#454545"
    bgCobre = "#ff9955"


class Imagens:
    logo = PhotoImage(
        file="src/images/logos/logo.png")


class activeButtons:
    buscarButton = PhotoImage(
        file="src/images/buttons/activeButtons/buscarButton.png")
    finalizarButton = PhotoImage(
        file="src/images/buttons/activeButtons/finalizarButton.png")
    menuButton = PhotoImage(
        file="src/images/buttons/activeButtons/menuButton.png")
    retomarButton = PhotoImage(
        file="src/images/buttons/activeButtons/retomarButton.png")
    rqButton = PhotoImage(
        file="src/images/buttons/activeButtons/rqButton.png")
    setupButton = PhotoImage(
        file="src/images/buttons/activeButtons/setupButton.png")
    startButton = PhotoImage(
        file="src/images/buttons/activeButtons/startButton.png")
    sairButton = PhotoImage(
        file="src/images/buttons/sairButton.png")
    confirmarButton = PhotoImage(
        file="src/images/buttons/activeButtons/confirmarButton.png")


class inactiveButtons:

    buscarButton = PhotoImage(
        file="src/images/buttons/inactiveButtons/buscarButton.png")
    finalizarButton = PhotoImage(
        file="src/images/buttons/inactiveButtons/finalizarButton.png")
    menuButton = PhotoImage(
        file="src/images/buttons/inactiveButtons/menuButton.png")
    retomarButton = PhotoImage(
        file="src/images/buttons/inactiveButtons/retomarButton.png")
    rqButton = PhotoImage(
        file="src/images/buttons/inactiveButtons/rqButton.png")
    setupButton = PhotoImage(
        file="src/images/buttons/inactiveButtons/setupButton.png")
    startButton = PhotoImage(
        file="src/images/buttons/inactiveButtons/startButton.png")
    confirmarButton = PhotoImage(
        file="src/images/buttons/inactiveButtons/confirmarButton.png")


class redButtons:
    buscarButton = PhotoImage(
        file="src/images/buttons/redButtons/buscarButton.png")
    finalizarButton = PhotoImage(
        file="src/images/buttons/redButtons/finalizarButton.png")
    menuButton = PhotoImage(
        file="src/images/buttons/redButtons/menuButton.png")
    paradaButton = PhotoImage(
        file="src/images/buttons/redButtons/paradaButton.png")
    retomarButton = PhotoImage(
        file="src/images/buttons/redButtons/retomarButton.png")
    rqButton = PhotoImage(
        file="src/images/buttons/redButtons/rqButton.png")
    setupButton = PhotoImage(
        file="src/images/buttons/redButtons/setupButton.png")
    startButton = PhotoImage(
        file="src/images/buttons/redButtons/startButton.png")
    cancelarButton = PhotoImage(
        file="src/images/buttons/redButtons/cancelarButton.png")


class Application:

    # --- Inicialização do Aplicativo --- #
    def __init__(self, master=None):
        # Variaveis.idUsuarioLogado = login.idUsuario
        # Variaveis.nomeUsuarioLogado = login.nomeUsuario
        #
        # if Variaveis.idUsuarioLogado > 0:
            self.montaTelaPrincipal()

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

        ##--- Rodape ---###
        self.containerRodape = Frame(self.containerEsquerda,
                                     bg=Cores.bgCinza)
        self.containerRodape.pack(side=BOTTOM,
                                  anchor=SW)

        # ####--- Proximo Cabo ---####
        # self.containerProxCabo = Frame(self.containerRodape,
        #                                bg=Cores.bgRodape)
        # self.containerProxCabo.pack(side=TOP,
        #                             fill=X,
        #                             expand=1)
        #
        # ####--- Label Prox Medidas ---####
        # self.containerProxMedidas = Frame(self.containerRodape,
        #                                   bg=Cores.bgRodape)
        # self.containerProxMedidas.pack()

    def montaLabels(self, master=None):
        ##------ Cabeçalho ------##
        self.logo = Label(self.containerCabecalho,
                          text="Datateck",
                          font=Fontes.fonteCabecalho,
                          image=Imagens.logo,
                          bg=Cores.bgCinza,
                          fg="white")
        self.logo.pack(side=LEFT)

        self.lblMaquina = Label(self.containerCabecalho,
                                text=Definicoes.maquina,
                                font=Fontes.fonteCabecalho,
                                bg=Cores.bgCinza,
                                fg="white")
        self.lblMaquina.pack(side=LEFT,
                             fill=BOTH,
                             expand=1)

        self.lblEstado = Label(self.containerCabecalho,
                               text=Variaveis.estados[Variaveis.estadoEquipamento],
                               font=Fontes.fontePadrao,
                               bg=Cores.bgCinza,
                               fg="white",
                               anchor=CENTER,
                               justify=CENTER)
        self.lblEstado.pack(side=TOP,
                            fill=BOTH)

        self.lblRelogio = Label(self.containerCabecalho,
                                text="00:00:00",
                                font=Fontes.fonteCabecalho,
                                padx=10,
                                fg=Cores.letraVerde,
                                bg=Cores.bgCinza)
        self.lblRelogio.pack(side=LEFT,
                             fill=Y)

        ##--- Dados PD ---##
        ###--- Cabecalho PD ---###
        self.lblRequisicao = Label(self.containerCabecalhoPD,
                            text="Requisição: %s" % (Variaveis.campos.get("REQUISICAO")),
                            font=Fontes.fontePadrao,
                            bg=Cores.bgCinza,
                            fg="white",
                            anchor="w")
        self.lblRequisicao.pack(side=LEFT)

        self.lblPD = Label(self.containerCabecalhoPD,
                           text="PD: %s" % Variaveis.campos.get("PD"),
                           font=Fontes.fonteCabecalho,
                           bg=Cores.bgCinza,
                           fg=Cores.letraVerde,
                           anchor="center")
        self.lblPD.pack(side=LEFT,
                        fill=X,
                        expand=1)

        self.lblProdutoFinal = Label(self.containerCabecalhoPD,
                            text="Produto Final: %s" % Variaveis.campos.get("CHICOTE"),
                            font=Fontes.fontePadrao,
                            bg=Cores.bgCinza,
                            fg="white",
                            anchor="e")
        self.lblProdutoFinal.pack(side=LEFT)

        ###--- Medidas PD ---###
        self.lblDecapeA = Label(self.containerMedidasPD,
                                text=Variaveis.campos.get("DECAPE A"),
                                font=Fontes.fonteCabecalho,
                                bg=Cores.bgCinza,
                                fg=Cores.letraVerde)
        self.lblDecapeA.grid(column=0,
                             row=0)

        self.lblMedida = Label(self.containerMedidasPD,
                               text=Variaveis.campos.get("MEDIDA"),
                               font=Fontes.fonteCabecalho,
                               bg=Cores.bgCinza,
                               fg=Cores.letraVerde,
                               width=30)
        self.lblMedida.grid(column=1,
                            row=0)

        self.lblDecapeB = Label(self.containerMedidasPD,
                                text=Variaveis.campos.get("DECAPE B"),
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
                                  bd=0,
                                  height=2)
        self.lblLadoACabo.grid(column=0,
                               row=0,
                               rowspan=3)

        self.lblCaboSec1 = Label(self.containerCabo,
                             text="",
                             font=Fontes.fontePadrao,
                             bg=Cores.bgCorDoCabo,
                             fg=Cores.fgCorDoCabo,
                             width=40,
                             bd=0,
                             height=1)
        self.lblCaboSec1.grid(column=1,
                          row=0)

        self.lblCabo = Label(self.containerCabo,
                             text=Variaveis.campos.get("CABO"),
                             font=Fontes.fontePadrao,
                             bg=Cores.bgCorDaListra,
                             fg=Cores.fgCorDoCabo,
                             width=40,
                             bd=0,
                             height=1)
        self.lblCabo.grid(column=1,
                          row=1)

        self.lblCaboSec2 = Label(self.containerCabo,
                                 text="",
                                 font=Fontes.fontePadrao,
                                 bg=Cores.bgCorDoCabo,
                                 fg=Cores.fgCorDoCabo,
                                 width=40,
                                 bd=0,
                                 height=1)
        self.lblCaboSec2.grid(column=1,
                              row=2)

        self.lblLadoBCabo = Label(self.containerCabo,
                                  text="",
                                  bg=Cores.bgCobre,
                                  width=10,
                                  bd=0,
                                  height=2)
        self.lblLadoBCabo.grid(column=2,
                               row=0,
                               rowspan=3)

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
                                    text=Variaveis.campos.get("ACABAMENTO 1"),
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
                                    text=Variaveis.campos.get("ACABAMENTO 3"),
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
                                           text=Variaveis.campos.get("QTD PD REQ"),
                                           font=Fontes.fonteQuantidadePendente,
                                           bg=Cores.bgCinza,
                                           fg=Cores.letraVerde,
                                           anchor="ne")
        self.lblQuantidadePendente.pack()

        self.lblQuantidadeCortada = Label(self.containerQuantidade,
                                          text=Variaveis.campos.get("QUANTIDADE_CORTADA"),
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
                                   text=Variaveis.campos.get("OBSERVAÇÃO"),
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
                                 text=Variaveis.campos.get("GRAVAÇÃO"),
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
                                    text=Variaveis.campos.get("ACABAMENTO 2"),
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
                                    text=Variaveis.campos.get("ACABAMENTO 4"),
                                    font=Fontes.fontePadrao,
                                    bg=Cores.bgAcabamentosAux,
                                    fg=Cores.bgCinza)
        self.lblAcabamento4.pack(fill=BOTH,
                                 expand=1,
                                 pady=5)

        # --- Rodape ---#
        self.lblRodape = Label(self.containerRodape,
                               text="%s - Logado desde:  %s" %
                                    (Variaveis.nomeUsuarioLogado,
                                     Variaveis.inicioSecao),
                               bg=Cores.bgCinza,
                               fg='white',
                               anchor='sw')
        self.lblRodape.pack()


        # self.lblProxCabo = Label(self.containerProxCabo,
        #                          text=Variaveis.campos.get("PROX_CABO"),
        #                          bg=Cores.bgRodape,
        #                          fg=Cores.bgAcabamentosAux)
        # self.lblProxCabo.pack(side=TOP,
        #                       fill=X,
        #                       expand=1)
        #
        # self.lblLabelProxDecapeA = Label(self.containerProxMedidas,
        #                                  text="Decape A",
        #                                  bg=Cores.bgRodape,
        #                                  fg=Cores.bgAcabamentosAux)
        # self.lblLabelProxDecapeA.grid(column=0,
        #                               row=0)
        #
        # self.lblLabelProxMedida = Label(self.containerProxMedidas,
        #                                 text="Medida",
        #                                 bg=Cores.bgRodape,
        #                                 fg=Cores.bgAcabamentosAux,
        #                                 width=30)
        # self.lblLabelProxMedida.grid(column=1,
        #                              row=0)
        #
        # self.lblLabelProxDecapeB = Label(self.containerProxMedidas,
        #                                  text="Decape B",
        #                                  bg=Cores.bgRodape,
        #                                  fg=Cores.bgAcabamentosAux)
        # self.lblLabelProxDecapeB.grid(column=2,
        #                               row=0)
        #
        # self.lblProxDecapeA = Label(self.containerProxMedidas,
        #                             text=Variaveis.campos.get("PROX_DECAPEA"),
        #                             bg=Cores.bgRodape,
        #                             fg=Cores.bgAcabamentosAux)
        # self.lblProxDecapeA.grid(column=0,
        #                          row=1)
        #
        # self.lblProxMedida = Label(self.containerProxMedidas,
        #                            text=Variaveis.campos.get("PROX_MEDIDA"),
        #                            bg=Cores.bgRodape,
        #                            fg="#888")
        # self.lblProxMedida.grid(column=1, row=1)
        #
        # self.lblProxDecapeB = Label(self.containerProxMedidas,
        #                             text=Variaveis.campos.get("PROX_DECAPEB"),
        #                             bg=Cores.bgRodape,
        #                             fg=Cores.bgAcabamentosAux)
        # self.lblProxDecapeB.grid(column=2,
        #                          row=1)

    def montaBotoes(self, master=None):

        # --- Botões ---#
        self.btnBuscar = Button(self.containerBotoes,
                                image=activeButtons.buscarButton,
                                width=130,
                                height=50,
                                bg=Cores.bgCinza,
                                relief=FLAT,
                                anchor="w",
                                bd=0,
                                highlightthickness=0)
        self.btnBuscar["command"] = self.montaLista
        self.btnBuscar.pack(pady=5)

        self.btnSetup = Button(self.containerBotoes,
                               image=inactiveButtons.setupButton,
                               width=130,
                                   height=50,
                               bg=Cores.bgCinza,
                               relief=FLAT,
                               anchor="w",
                               bd=0,
                               highlightthickness=0)
        self.btnSetup["command"] = self.setupStartStop
        self.btnSetup.pack(pady=5)

        self.btnStart = Button(self.containerBotoes,
                               image=inactiveButtons.startButton,
                               width=130,
                               height=50,
                               bg=Cores.bgCinza,
                               relief=FLAT,
                               anchor="w",
                               bd=0,
                               highlightthickness=0)
        # self.btnStart["command"] =
        self.btnStart.pack(pady=5)

        self.btnRQ = Button(self.containerBotoes,
                              image=inactiveButtons.rqButton,
                              width=130,
                              height=50,
                              bg=Cores.bgCinza,
                              relief=FLAT,
                              anchor="w",
                              bd=0,
                              highlightthickness=0)
        self.btnRQ["command"] = self.abrirPopUpRQSetup
        self.btnRQ.pack(pady=5)

        self.btnParada = Button(self.containerBotoes,
                                image=redButtons.paradaButton,
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
                              image=activeButtons.menuButton,
                              width=130,
                              height=50,
                              bg=Cores.bgCinza,
                              relief=FLAT,
                              anchor="w",
                              bd=0,
                              highlightthickness=0)
        # self.btnMenu["command"] =
        self.btnMenu.pack(pady=5)
        
        self.btnSair = Button(self.containerBotoes,
                              image=activeButtons.sairButton,
                              width=130,
                              height=50,
                              bg=Cores.bgCinza,
                              relief=FLAT,
                              anchor="w",
                              bd=0,
                              highlightthickness=0)
        self.btnSair["command"] = root.destroy
        self.btnSair.pack(pady=5)

    # --- Limpeza de Layouts --- #
    def limpaTela(self):
        for ele in root.winfo_children():
            ele.destroy()

    def limpaContainerEsquerda(self):
        for ele in self.containerEsquerda.winfo_children():
            ele.destroy()

    # --- Busca Lista de Corte --- #
    def montaLista(self):
        self.btnBuscar.configure(image=inactiveButtons.buscarButton)

        if Variaveis.estadoEquipamento <= 1:
            self.limpaContainerEsquerda()


            self.dataCols = ('Medida',
                             'Quantidade',
                             'Requisição',
                             'ID')


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
            self.tvw.bind("<ButtonRelease-1>", self.abrirOuFecharNode)

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
                                      fg="white",
                                      bd=0,
                                      relief=FLAT,
                                      image=activeButtons.confirmarButton)
            self.btnConfirma.bind("<Button-1>", self.listaSelectBtn)
            self.btnConfirma.grid(column=0,
                                  row=3,
                                  ipadx=5)

            self.populaLista()

    def populaLista(self):
        pd = PD()
        pd.buscaLista(Definicoes.maquina)

        self.data = pd.lista

        cabos = []

        for item in self.data:
            if item[9] not in cabos:
                cabos.append(str(item[9]))


        for cabo in cabos:
            self.tvw.insert('', 'end', cabo, text=cabo)

        for item in self.data:
            self.tvw.insert(
                            item[9],
                            'end',
                            text=item[8], values=(
                                                item[15],
                                                round(item[14]),
                                                item[1],
                                                item[0]))

        self.listaCount.configure(text='Total de PDs: ' + str(len(self.data)))

    def abrirOuFecharNode(self, master=None):
        self.nodeSel = self.tvw.focus()
        self.nodeIsOpen = self.tvw.item(self.nodeSel, option='open')

        self.tvw.item(self.nodeSel, open= not self.nodeIsOpen)

    def listaSelectBtn(self, master=None):
        self.itemSel = self.tvw.focus()
        self.itemData = self.tvw.item(self.itemSel)
        Variaveis.ID = self.itemData.get('values')[3]

        self.carregaDadosDoPDNaTela(Variaveis.ID)

    def carregaDadosDoPDNaTela(self, ID):
        pd = PD()
        pd.buscaPD(ID)
        dadosDoPD = pd.dadosPD

        for i in range(len(dadosDoPD)):
            try:
                Variaveis.campos[Variaveis.colunas[i]] = round(dadosDoPD[i])
            except:
                Variaveis.campos[Variaveis.colunas[i]] = dadosDoPD[i]

        for ele in root.winfo_children():
            ele.destroy()

        Cores.bgCorDoCabo = Variaveis.campos.get("PRIMARIA")
        Cores.bgCorDaListra = Variaveis.campos.get("SECUNDARIA")
        Cores.fgCorDoCabo = Variaveis.campos.get("COR_TEXTO")

        Variaveis.estadoEquipamento = 1

        t = tempos.TEMPOS()
        t.tomaTempoEvento(Variaveis.ID,
                          1,
                          Variaveis.idUsuarioLogado,
                          Definicoes.maquina)

        self.montaTelaPrincipal()

        self.btnSetup.configure(image=activeButtons.setupButton)

    def setupStartStop(self):
        if Variaveis.estadoEquipamento in (1, 4):
            Variaveis.estadoEquipamento = 2

            t = tempos.TEMPOS()

            t.tomaTempoEvento(Variaveis.ID,
                              3,
                              Variaveis.idUsuarioLogado,
                              Definicoes.maquina)

            Variaveis.t0 = time()

            self.atualizaCronografo()

            self.btnBuscar.configure(image=inactiveButtons.buscarButton)
            self.btnSetup.configure(image=redButtons.setupButton)
            self.btnRQ.configure(image=activeButtons.rqButton)

            self.atualizaEstado()

        elif Variaveis.estadoEquipamento == 2:
            Variaveis.estadoEquipamento = 4
            t = tempos.TEMPOS()

            t.tomaTempoEvento(Variaveis.ID,
                              4,
                              Variaveis.idUsuarioLogado,
                              Definicoes.maquina)

            self.zeraCronografo()

            self.btnSetup.configure(image=activeButtons.setupButton)
            self.btnRQ.configure(image=inactiveButtons.rqButton)

            self.atualizaEstado()

    def zeraCronografo(self):
        self.lblRelogio.configure(text='00:00:00')

    def atualizaCronografo(self):
        if Variaveis.estadoEquipamento in (2, 3, 5):

            tempoAtual = (time() - Variaveis.t0)

            horas = int(tempoAtual/3600)
            minutos = int((tempoAtual - horas*3600)/60)
            segundos = int(tempoAtual - (horas * 3600) - (minutos * 60))

            tempoAtual = '%02d:%02d:%02d' % (horas, minutos, segundos)

            self.lblRelogio.configure(text=tempoAtual)
            root.after(1000, self.atualizaCronografo)

    def atualizaEstado(self):
        self.lblEstado.configure(
            text=Variaveis.estados[Variaveis.estadoEquipamento])

    def abrirPopUpRQSetup(self):
        # if Variaveis.estadoEquipamento == 2:
            print(Variaveis.campos["ACABAMENTO 1"])
            Variaveis.estadoEquipamento = 3

            self.btnRQ.configure(image=inactiveButtons.rqButton)

            self.popUpRQSetup = Toplevel(bg=Cores.bgCinza,
                                         bd=7,
                                         relief=RAISED)
            self.popUpRQSetup.overrideredirect(1)
            self.popUpRQSetup.attributes('-topmost', 'true')
            self.popUpRQSetup.bind('<Escape>', self.cancelarPopUpRQSetup)
            self.popUpRQSetup.geometry('+300+200')
            self.popUpRQSetup.focus()

            self.frameCamposRQ = Frame(self.popUpRQSetup,
                                       bg=Cores.bgCinza)
            self.frameCamposRQ.pack(side=TOP,
                                    fill=BOTH,
                                    expand=1,
                                    padx=15,
                                    pady=(5,10))

            self.botoesRQ = Frame(self.popUpRQSetup,
                                  bg=Cores.bgCinza)
            self.botoesRQ.pack(side=BOTTOM,
                               fill=X,
                               expand=1,
                               padx=10,
                               pady=10)

            self.btnConfirmaRQ = Button(self.botoesRQ,
                                        text="Fechar",
                                        font=Fontes.fontePadrao,
                                        bg=Cores.bgCinza,
                                        fg='white',
                                        relief=FLAT,
                                        image=inactiveButtons.confirmarButton)

            # self.btnConfirmaRQ["command"] =

            self.btnCancelaRQ = Button(self.botoesRQ,
                                       text="Fechar",
                                       font=Fontes.fontePadrao,
                                       bg=Cores.bgCinza,
                                       fg='white',
                                       relief=FLAT,
                                       image=redButtons.cancelarButton)
            self.btnCancelaRQ["command"] = self.cancelarPopUpRQSetup

            self.lblRegQualidade = Label(self.frameCamposRQ,
                                         text="REGISTROS DE QUALIDADE",
                                         font=Fontes.fonteCabecalho,
                                         bg=Cores.bgCinza,
                                         fg='azure2',
                                         justify=CENTER)

            self.lblPriMedida = Label(self.frameCamposRQ,
                                      text="PRIMEIRA MEDIDA (mm)",
                                      font=Fontes.fontePadrao,
                                      bg=Cores.bgCinza,
                                      fg=Cores.letraVerde,
                                      justify=CENTER)

            self.entryPriMedida = Entry(self.frameCamposRQ,
                                        width=10,
                                        bg='lightcyan2',
                                        disabledbackground='dark slate gray',
                                        font=Fontes.fonteCabecalho,
                                        justify=CENTER)
            self.entryPriMedida.bind("<Button-1>",
                                     lambda x:
                                     self.virtualNumPad(
                                         self.entryPriMedida))

            self.lblLadoA = Label(self.frameCamposRQ,
                                  text="LADO A",
                                  font=Fontes.fontePadrao,
                                  bg=Cores.bgCinza,
                                  fg=Cores.letraVerde,
                                  justify=CENTER)

            self.lblLadoB = Label(self.frameCamposRQ,
                                  text="LADO B",
                                  font=Fontes.fontePadrao,
                                  bg=Cores.bgCinza,
                                  fg=Cores.letraVerde,
                                  justify=CENTER)

            self.entryAlturaIsolanteA = Entry(self.frameCamposRQ,
                                              width=10,
                                              bg='lightcyan2',
                                              disabledbackground='dark slate gray',
                                              font=Fontes.fonteCabecalho,
                                              justify=CENTER)
            self.entryAlturaIsolanteA.bind("<Button-1>",
                                     lambda x:
                                     self.virtualNumPad(
                                         self.entryAlturaIsolanteA))

            self.lblAlturaIsolante = Label(self.frameCamposRQ,
                                           text="Altura Isolante (mm)",
                                           font=Fontes.fontePadrao,
                                           bg=Cores.bgCinza,
                                           fg='white',
                                           justify=CENTER)

            self.entryAlturaIsolanteB = Entry(self.frameCamposRQ,
                                              width=10,
                                              bg='lightcyan2',
                                              disabledbackground='dark slate gray',
                                              font=Fontes.fonteCabecalho,
                                              justify=CENTER)
            self.entryAlturaIsolanteB.bind("<Button-1>",
                                           lambda x:
                                           self.virtualNumPad(
                                               self.entryAlturaIsolanteB))

            self.entryAlturaCondutorA = Entry(self.frameCamposRQ,
                                              width=10,
                                              bg='lightcyan2',
                                              disabledbackground='dark slate gray',
                                              font=Fontes.fonteCabecalho,
                                              justify=CENTER)
            self.entryAlturaCondutorA.bind("<Button-1>",
                                           lambda x:
                                           self.virtualNumPad(
                                               self.entryAlturaCondutorA))

            self.lblAlturaCondutor = Label(self.frameCamposRQ,
                                           text="Altura Condutor (mm)",
                                           font=Fontes.fontePadrao,
                                           bg=Cores.bgCinza,
                                           fg='white',
                                           justify=CENTER)

            self.entryAlturaCondutorB = Entry(self.frameCamposRQ,
                                              width=10,
                                              bg='lightcyan2',
                                              disabledbackground='dark slate gray',
                                              font=Fontes.fonteCabecalho,
                                              justify=CENTER)
            self.entryAlturaCondutorB.bind("<Button-1>",
                                           lambda x:
                                           self.virtualNumPad(
                                               self.entryAlturaCondutorB))

            self.entryTracaoA = Entry(self.frameCamposRQ,
                                      width=10,
                                      bg='lightcyan2',
                                      disabledbackground='dark slate gray',
                                      font=Fontes.fonteCabecalho,
                                      justify=CENTER)
            self.entryTracaoA.bind("<Button-1>",
                                           lambda x:
                                           self.virtualNumPad(
                                               self.entryTracaoA))

            self.lblTracao = Label(self.frameCamposRQ,
                                   text="Tração (kgf)",
                                   font=Fontes.fontePadrao,
                                   bg=Cores.bgCinza,
                                   fg='white',
                                   justify=CENTER)

            self.entryTracaoB = Entry(self.frameCamposRQ,
                                      width=10,
                                      bg='lightcyan2',
                                      disabledbackground='dark slate gray',
                                      font=Fontes.fonteCabecalho,
                                      justify=CENTER)
            self.entryTracaoB.bind("<Button-1>",
                                           lambda x:
                                           self.virtualNumPad(
                                               self.entryTracaoB))

            self.lblRegQualidade.grid(column=0,
                                      row=0,
                                      columnspan=5,
                                      pady=10)

            self.lblPriMedida.grid(column=0,
                                   row=1,
                                   columnspan=3,
                                   pady=10)
            self.entryPriMedida.grid(column=0,
                                     row=2,
                                     columnspan=3)

            self.lblLadoA.grid(column=0,
                               row=3)
            self.lblLadoB.grid(column=2,
                               row=3)

            self.entryAlturaIsolanteA.grid(column=0,
                                           row=4)
            self.lblAlturaIsolante.grid(column=1,
                                        row=4)
            self.entryAlturaIsolanteB.grid(column=2,
                                           row=4)

            self.entryAlturaCondutorA.grid(column=0,
                                           row=5)
            self.lblAlturaCondutor.grid(column=1,
                                        row=5,
                                        pady=10)
            self.entryAlturaCondutorB.grid(column=2,
                                           row=5)

            self.entryTracaoA.grid(column=0,
                                   row=6)
            self.lblTracao.grid(column=1,
                                row=6)
            self.entryTracaoB.grid(column=2,
                                   row=6)

            self.btnConfirmaRQ.pack(side=LEFT,
                                    anchor='center',
                                    fill=X,
                                    expand=1)
            self.btnCancelaRQ.pack(side=LEFT,
                                   anchor='center',
                                   fill=X,
                                   expand=1)

            self.entryAlturaIsolanteA.configure(state='disabled')
            self.entryAlturaCondutorA.configure(state='disabled')
            self.entryTracaoA.configure(state='disabled')

            for ele in self.frameCamposRQ.winfo_children():
                if ele.winfo_class() == 'Entry':
                    print(ele.winfo_name())
                    ele.config(bg='black')

    def cancelarPopUpRQSetup(self):
        if Variaveis.estadoEquipamento == 3:
            Variaveis.estadoEquipamento = 2

            if Variaveis.virtualNumPadVisible:
                self.popUpVNumPad.destroy()
                Variaveis.virtualNumPadVisible = False

            self.popUpRQSetup.destroy()

            self.btnRQ.configure(image=activeButtons.rqButton)

    def virtualNumPad(self, papai):
        papai.configure(bg='lightgreen')
        papai.delete(0, END)

        if Variaveis.virtualNumPadVisible:

            self.popUpVNumPad.destroy()
            Variaveis.virtualNumPadVisible = False
            self.virtualNumPad(papai)

        elif not Variaveis.virtualNumPadVisible:
            Variaveis.virtualNumPadVisible = True

            self.popUpVNumPad = Toplevel(bg=Cores.bgCinza,
                                         bd=7,
                                         relief=RAISED)
            self.popUpVNumPad.overrideredirect(1)
            self.popUpVNumPad.attributes('-topmost', 'true')
            self.popUpVNumPad.bind('<Escape>',
                                   lambda e: self.popUpVNumPad.destroy())
            self.popUpVNumPad.geometry('+800+200')
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
                                                                     papai)

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
            print(parent)
            print(keyValue)

            if keyValue == "<":
                parent.delete(len(parent.get()) - 1, END)
            else:
                parent.insert(END, keyValue)




Application(root)
root.mainloop()
