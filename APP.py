#--- Imports ---#
from pd import PD
import tempos
import etiqueta
import priorizacao_pds as priori
from motivos import MOTIVOS
from tkinter import *
from time import time
import datetime
from tkinter import ttk
import menu as configMenu
import login
import configparser as cfgprsr
import inspect
import os, re

diretorio = os.path.dirname(os.path.abspath(__file__))

class Definicoes:
    configFile = cfgprsr.ConfigParser()
    configFile.read(diretorio + '/config.ini')


def montaRoot():
    global root
    root = Tk()
    root.title('Operação')
    root.geometry(Definicoes.configFile['DISPLAY']['RES'])
    root.attributes('-fullscreen', Definicoes.configFile['DISPLAY']['Tela Cheia'])
    root.attributes('-topmost', 'false')
    root.bind('<Escape>', lambda e: root.destroy())
    root.resizable(width=True, height=True)
montaRoot()

class Variaveis:
    inicioSecao = datetime.datetime.now().strftime('%d-%m-%Y  %H:%M:%S')
    idUsuarioLogado = 0
    nomeUsuarioLogado = None

    colunas = ('PK_IRP',
               'REQUISICAO',
               'CELULA',
               'DATA_GERACAO',
               'DATA_ENTREGA',
               'OBSERVACAO_REQ',
               'CHICOTE',
               'PD',
               'CPD',
               'CABO',
               'FK_CRS',
               'VIAS',
               'BITOLA',
               'UNIDADE',
               'NORMA',
               'QTD_PD_REQ',
               'QTD_CORTADA',
               'MEDIDA',
               'DECAPE_A',
               'DECAPE_B',
               'ACABAMENTO_1',
               'PONTE_1',
               'ACABAMENTO_2',
               'PONTE_2',
               'ACABAMENTO_3',
               'PONTE_3',
               'ACABAMENTO_4',
               'PONTE_4',
               'OBSERVACAO',
               'GRAVACAO',
               'MAQUINA',
               'NR_ORDEM_CORTE',
               'PRIORIDADE',
               'DESCRICAO',
               'PRIMARIA',
               'SECUNDARIA',
               'COR_TEXTO')

    campos = {
        "PK_IRP":            "",
        "REQUISICAO":        "",
        "CELULA":            "",
        "DATA_GERACAO":      "",
        "DATA_ENTREGA":      "",
        "OBSERVACAO_REQ":    "",
        "CHICOTE":           "",
        "PD":                "",
        "CPD":               "",
        "CABO":              "",
        "FK_CRS":            "",
        "VIAS":              "",
        "BITOLA":            "",
        "UNIDADE":           "",
        "NORMA":             "",
        "QTD_PD_REQ":        "",
        "QTD_CORTADA":       "",
        "MEDIDA":            "",
        "DECAPE_A":          "",
        "DECAPE_B":          "",
        "ACABAMENTO_1":      "",
        "PONTE_1":           "",
        "ACABAMENTO_2":      "",
        "PONTE_2":           "",
        "ACABAMENTO_3":      "",
        "PONTE_3":           "",
        "ACABAMENTO_4":      "",
        "PONTE_4":           "",
        "OBSERVACAO":        "",
        "GRAVACAO":          "",
        "MAQUINA":           "",
        "NR_ORDEM_CORTE":    "",
        "PRIORIDADE":        "",
        "DESCRICAO":         "",
        "PRIMARIA":          "",
        "SECUNDARIA":        "",
        "COR_TEXTO":         ""}

    estados = ('Ocioso',
               'Carregado',
               'Em Setup',
               'Preenchendo RQ',
               'Setup Finalizado',
               'Em Corte',
               'Corte Finalizado',
               'Parado')

    estadoEquipamento = 0
    estadoAntesDaParada = 0
    t0 = 0
    tempoAtual = 0
    t0Parada = 0
    tAcumulado = 0
    ID = 0

    RQPreenchido = False

    exigeRegQual = True

    virtualNumPadVisible = False

    quantidadePendente = 0
    quantidadeCortada = 0

    quantidadeDivergente = False

    maquinaParada = False
    paradaEmSetup = False
    paradaEmCorte = False

    ultimaNorma = None
    ultimoAcabamento1 = None
    ultimoAcabamento2 = None

    ultimoRegistro = []


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
        file=diretorio + "/src/images/logos/logo.png")
    logoTri = PhotoImage(
        file=diretorio + "/src/images/logos/logoTri.png")


class activeButtons:
    buscarButton = PhotoImage(
        file=diretorio + "/src/images/buttons/activeButtons/buscarButton.png")
    finalizarButton = PhotoImage(
        file=diretorio + "/src/images/buttons/activeButtons/finalizarButton.png")
    menuButton = PhotoImage(
        file=diretorio + "/src/images/buttons/activeButtons/menuButton.png")
    retomarButton = PhotoImage(
        file=diretorio + "/src/images/buttons/activeButtons/retomarButton.png")
    rqButton = PhotoImage(
        file=diretorio + "/src/images/buttons/activeButtons/rqButton.png")
    setupButton = PhotoImage(
        file=diretorio + "/src/images/buttons/activeButtons/setupButton.png")
    startButton = PhotoImage(
        file=diretorio + "/src/images/buttons/activeButtons/startButton.png")
    sairButton = PhotoImage(
        file=diretorio + "/src/images/buttons/sairButton.png")
    confirmarButton = PhotoImage(
        file=diretorio + "/src/images/buttons/activeButtons/confirmarButton.png")


class inactiveButtons:
    buscarButton = PhotoImage(
        file=diretorio + "/src/images/buttons/inactiveButtons/buscarButton.png")
    finalizarButton = PhotoImage(
        file=diretorio + "/src/images/buttons/inactiveButtons/finalizarButton.png")
    menuButton = PhotoImage(
        file=diretorio + "/src/images/buttons/inactiveButtons/menuButton.png")
    retomarButton = PhotoImage(
        file=diretorio + "/src/images/buttons/inactiveButtons/retomarButton.png")
    rqButton = PhotoImage(
        file=diretorio + "/src/images/buttons/inactiveButtons/rqButton.png")
    setupButton = PhotoImage(
        file=diretorio + "/src/images/buttons/inactiveButtons/setupButton.png")
    startButton = PhotoImage(
        file=diretorio + "/src/images/buttons/inactiveButtons/startButton.png")
    confirmarButton = PhotoImage(
        file=diretorio + "/src/images/buttons/inactiveButtons/confirmarButton.png")


class redButtons:
    buscarButton = PhotoImage(
        file=diretorio + "/src/images/buttons/redButtons/buscarButton.png")
    finalizarButton = PhotoImage(
        file=diretorio + "/src/images/buttons/redButtons/finalizarButton.png")
    menuButton = PhotoImage(
        file=diretorio + "/src/images/buttons/redButtons/menuButton.png")
    paradaButton = PhotoImage(
        file=diretorio + "/src/images/buttons/redButtons/paradaButton.png")
    retomarButton = PhotoImage(
        file=diretorio + "/src/images/buttons/redButtons/retomarButton.png")
    rqButton = PhotoImage(
        file=diretorio + "/src/images/buttons/redButtons/rqButton.png")
    setupButton = PhotoImage(
        file=diretorio + "/src/images/buttons/redButtons/setupButton.png")
    startButton = PhotoImage(
        file=diretorio + "/src/images/buttons/redButtons/startButton.png")
    cancelarButton = PhotoImage(
        file=diretorio + "/src/images/buttons/redButtons/cancelarButton.png")


class Application:

    # --- Inicialização do Aplicativo --- #
    def __init__(self, master=None):
        Variaveis.idUsuarioLogado = login.idUsuario
        Variaveis.nomeUsuarioLogado = login.nomeUsuario

        if Variaveis.idUsuarioLogado > 0:
            self.montaTelaPrincipal()

            #------- debug -------#


            try:
                etq = etiqueta.etiqueta()
                etq.testeImpressora()
            except:
                pass

    # --- Geração do Layout Principal --- #
    def montaTelaPrincipal(self, master=None):
        self.configFile = cfgprsr.ConfigParser()
        self.configFile.read(diretorio + '/config.ini')
        self.maquina = self.configFile['DEFAULT']['maquina']
        self.maquinaAutomatica = self.configFile['DEFAULT']['MaqAutomatica']

        def montaContainers(master=None):
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
                                      anchor=SW,
                                      fill=X,
                                      expand=1)

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

        def montaLabels(master=None):
            ##------ Cabeçalho ------##
            self.logo = Label(self.containerCabecalho,
                              text="Datateck",
                              font=Fontes.fonteCabecalho,
                              image=Imagens.logo,
                              bg=Cores.bgCinza,
                              fg="white")
            self.logo.pack(side=LEFT)

            self.lblMaquina = Label(self.containerCabecalho,
                                    text=self.maquina,
                                    font=Fontes.fonteCabecalho,
                                    bg=Cores.bgCinza,
                                    fg="white")
            self.lblMaquina.pack(side=LEFT,
                                 fill=BOTH,
                                 expand=1)

            self.lblEstado = Label(self.containerCabecalho,
                                   text=Variaveis.estados[
                                       Variaveis.estadoEquipamento],
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
                                       text="Requisição: %s" % (
                                           Variaveis.campos.get("REQUISICAO")),
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
                                         text="Produto Final: %s" % Variaveis.campos.get(
                                             "CHICOTE"),
                                         font=Fontes.fontePadrao,
                                         bg=Cores.bgCinza,
                                         fg="white",
                                         anchor="e")
            self.lblProdutoFinal.pack(side=LEFT)

            ###--- Medidas PD ---###
            self.lblDecapeA = Label(self.containerMedidasPD,
                                    text=Variaveis.campos.get("DECAPE_A"),
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
                                    text=Variaveis.campos.get("DECAPE_B"),
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
            self.lblCaboSec1.bind("<Button-1>", lambda x: self.PopUpCabo())

            self.lblCabo = Label(self.containerCabo,
                                 text="CPD: %s | Cabo: %s" % (Variaveis.campos.get("CPD"),
                                                     Variaveis.campos.get("CABO")),
                                 font=Fontes.fontePadrao,
                                 bg=Cores.bgCorDaListra,
                                 fg=Cores.fgCorDoCabo,
                                 width=40,
                                 bd=0,
                                 height=1)
            self.lblCabo.grid(column=1,
                              row=1)
            self.lblCabo.bind("<Button-1>", lambda x: self.PopUpCabo())

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
            self.lblCaboSec2.bind("<Button-1>", lambda x: self.PopUpCabo())

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
                                        text=Variaveis.campos.get(
                                             "ACABAMENTO_1"),
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
                                        text=Variaveis.campos.get(
                                            "ACABAMENTO_3"),
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
                                               text=Variaveis.quantidadePendente,
                                               font=Fontes.fonteQuantidadePendente,
                                               bg=Cores.bgCinza,
                                               fg=Cores.letraVerde,
                                               anchor="ne")
            self.lblQuantidadePendente.pack()

            self.lblQuantidadeCortada = Label(self.containerQuantidade,
                                              text=Variaveis.campos.get(
                                                  "QUANTIDADE_CORTADA"),
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
                                       text=Variaveis.campos.get("OBSERVACAO"),
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
                                     text=Variaveis.campos.get("GRAVACAO"),
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
                                        text=Variaveis.campos.get(
                                            "ACABAMENTO_2"),
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
                                        text=Variaveis.campos.get(
                                            "ACABAMENTO_4"),
                                        font=Fontes.fontePadrao,
                                        bg=Cores.bgAcabamentosAux,
                                        fg=Cores.bgCinza)
            self.lblAcabamento4.pack(fill=BOTH,
                                     expand=1,
                                     pady=5)


            for i in [1, 2]:
                acabs = [self.lblAcabamento1, self.lblAcabamento2]
                if Variaveis.campos.get("PONTE_%d" % i) == "S":
                    acabs[i-1].config(bg='yellow',
                                      text='%s \n CRIMPAGEM COM PONTE' %
                                      Variaveis.campos.get('ACABAMENTO_%d' % i))

            # --- Rodape ---#
            self.lblRodape = Label(self.containerRodape,
                                   text="%s - Logado desde:  %s" %
                                        (Variaveis.nomeUsuarioLogado,
                                         Variaveis.inicioSecao),
                                   bg=Cores.bgCinza,
                                   fg='white',
                                   anchor='sw')
            self.lblRodape.pack(side=LEFT,
                                fill=X,
                                expand=1)

            self.logoTri = Label(self.containerBotoes,
                                 text="Powered by TRI",
                                 image=Imagens.logoTri,
                                 bg=Cores.bgCinza,
                                 fg="white",
                                 anchor='se')
            self.logoTri.pack(side=BOTTOM,
                              pady=5,
                              anchor='w')

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

        def montaBotoes(master=None):
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
            self.btnStart["command"] = self.corteStartStop
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
            self.btnRQ["command"] = (lambda: self.popUpRQSetup())
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
            self.btnParada["command"] = self.paradaDeMaquina
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
            self.btnMenu["command"] = self.AbreMenu
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
            # self.btnSair.pack(pady=5)

        montaContainers()
        montaLabels()
        montaBotoes()

    # --- Limpeza de Layouts --- #
    def limpaTela(self):
        for ele in root.winfo_children():
            ele.destroy()

    def labelsUpdate(self):
        ##--- Dados PD ---##
        ###--- Cabecalho PD ---###
        self.lblRequisicao = Label(text="Requisição: %s" % (
                                       Variaveis.campos.get("REQUISICAO")))
        self.lblPD = Label(text="PD: %s" % Variaveis.campos.get("PD"))

        self.lblProdutoFinal = Label(text="Produto Final: %s" % Variaveis.campos.get(
                                         "CHICOTE"))

        ###--- Medidas PD ---###
        self.lblDecapeA = Label(text=Variaveis.campos.get("DECAPE_A"))
        self.lblMedida = Label(text=Variaveis.campos.get("MEDIDA"))
        self.lblDecapeB = Label(text=Variaveis.campos.get("DECAPE_B"))

        ###--- Cabo ---###
        self.lblCaboSec1 = Label(bg=Cores.bgCorDoCabo)
        self.lblCabo = Label(bg=Cores.bgCorDaListra)
        self.lblCaboSec2 = Label(bg=Cores.bgCorDoCabo)

        ###--- Detalhes ---###
        ####--- Lado A ---####
        #####--- Acabamento 1 ---#####
        self.lblAcabamento1 = Label(text=Variaveis.campos.get("ACABAMENTO_1"))
        self.lblAcabamento3 = Label(text=Variaveis.campos.get("ACABAMENTO_3"))

        ####--- Quantidade ---####
        self.lblQuantidadePendente = Label(text=Variaveis.campos.get(
                                               "QTD_PD_REQ"))
        self.lblQuantidadeCortada = Label(text=Variaveis.campos.get(
                                              "QUANTIDADE_CORTADA"))

        ####--- Observacao ---####
        self.lblObservacao = Label(text=Variaveis.campos.get("OBSERVACAO"))

        ####--- Gravacao ---####
        self.lblGravacao = Label(text=Variaveis.campos.get("GRAVACAO"))

        ####--- Labo B ---####
        #####--- Acabamento 2 ---#####
        self.lblAcabamento2 = Label(text=Variaveis.campos.get("ACABAMENTO_2"))
        self.lblAcabamento4 = Label(text=Variaveis.campos.get("ACABAMENTO_4"))

    def limpaContainerEsquerda(self):
        for ele in self.containerEsquerda.winfo_children():
            ele.destroy()

    # --- Busca Lista de Corte --- #
    def montaLista(self):
        def listaSelectBtn(master=None):
            def carregaDadosDoPDNaTela():
                pd = PD()
                pd.buscaPD(Variaveis.ID)
                dadosDoPD = pd.dadosPD

                for i in range(len(dadosDoPD)):
                    try:
                        Variaveis.campos[Variaveis.colunas[i]] = round(
                            dadosDoPD[i], 2)
                    except:
                        Variaveis.campos[Variaveis.colunas[i]] = dadosDoPD[i]

                Cores.bgCorDoCabo = Variaveis.campos.get("PRIMARIA")
                Cores.bgCorDaListra = Variaveis.campos.get("SECUNDARIA")
                Cores.fgCorDoCabo = Variaveis.campos.get("COR_TEXTO")

                Variaveis.quantidadePendente = Variaveis.campos.get(
                    "QTD_PD_REQ") - Variaveis.campos.get("QTD_CORTADA")


                self.limpaTela()
                self.montaTelaPrincipal()

                Variaveis.estadoEquipamento = 1
                self.atualizaEstado()

                t = tempos.TEMPOS()
                t.tomaTempoEvento(Variaveis.ID,
                                  1,
                                  Variaveis.idUsuarioLogado,
                                  self.maquina)

                self.btnSetup.configure(image=activeButtons.setupButton)
                self.btnMenu.configure(image=inactiveButtons.menuButton)

            self.itemSel = self.tvw.focus()
            self.itemData = self.tvw.item(self.itemSel)
            Variaveis.ID = self.itemData.get('values')[3]

            carregaDadosDoPDNaTela()

        def abrirOuFecharNode(master=None):
            self.nodeSel = self.tvw.focus()
            self.nodeIsOpen = self.tvw.item(self.nodeSel, option='open')

            self.tvw.item(self.nodeSel, open=not self.nodeIsOpen)

        def populaLista():
            pd = PD()

            if self.maquinaAutomatica == 'True':
                def montaTelaCarregamento():
                    self.popUpBarraProgresso = Toplevel(bg=Cores.bgCinza)
                    self.popUpBarraProgresso.overrideredirect(1)
                    self.popUpBarraProgresso.attributes('-topmost', 'true')
                    self.popUpBarraProgresso.bind("<Button-1>",
                                                  lambda
                                                      e: self.popUpBarraProgresso.destroy)
                    self.popUpBarraProgresso.geometry(Definicoes.configFile['DISPLAY']['RES'])
                    self.popUpBarraProgresso.focus()

                montaTelaCarregamento()

                priori.AlgoritmoSeparacao(self.popUpBarraProgresso)

                pd.buscaLista()
                self.data = pd.lista

                casais = []

                for item in self.data:
                    casal = '%s | %s' % (str(item[20]), str(item[22]))
                    casal_invertido = '%s | %s' % (str(item[22]), str(item[20]))
                    if casal not in casais and casal_invertido not in casais:
                        casais.append(casal)

                for casal in casais:
                    self.tvw.insert('', 'end', casal, text=casal)

                qtd_Total = 0
                for item in self.data:
                    casal = '%s | %s' % (str(item[20]), str(item[22]))
                    casal_invertido = '%s | %s' % (str(item[22]), str(item[20]))
                    cabo = item[9]
                    medida = item[17]
                    qtd_req = round(item[15])
                    qtd_cortada = item[16]
                    qtd_pendente = qtd_req - qtd_cortada
                    qtd_Total += qtd_pendente
                    requisicao = item[1]
                    pk_irp = item[0]
                    # print("PK: %i - QTD REQ: %i - QTD_CORT: %i" % (item[0], item[14], item[15]))

                    try:
                        self.tvw.insert(casal,
                                        'end',
                                        text=cabo,
                                        values=(medida,
                                                qtd_pendente,
                                                requisicao,
                                                pk_irp))
                    except:
                        self.tvw.insert(casal_invertido,
                                        'end',
                                        text=cabo,
                                        values=(medida,
                                                qtd_pendente,
                                                requisicao,
                                                pk_irp))

            else:
                pd.buscaLista()
                self.data = pd.lista
                cabos = []

                for item in self.data:
                    cabo = item[9]

                    if cabo not in cabos:
                        cabos.append(str(cabo))

                for cabo in cabos:
                    self.tvw.insert('', 'end', cabo, text=cabo)

                qtd_Total = 0
                for item in self.data:
                    cabo = item[9]
                    pd = item[8]
                    medida = item[17]
                    qtd_req = round(item[15])
                    qtd_cortada = item[16]
                    qtd_pendente = qtd_req - qtd_cortada
                    qtd_Total += qtd_pendente
                    requisicao = item[1]
                    pk_irp = item[0]

                    self.tvw.insert(
                        cabo,
                        'end',
                        text=pd, values=(
                            medida,
                            qtd_pendente,
                            requisicao,
                            pk_irp))

            self.listaCount.configure(
                text='Total de PDs: %s   -   Total de Circuitos: %s' % (
                str(len(self.data)), str(int(qtd_Total))))

            root.update()

        if Variaveis.estadoEquipamento in (0,1,4,6) and not Variaveis.RQPreenchido:
            Variaveis.estadoEquipamento = 0

            self.btnSetup.config(image=inactiveButtons.setupButton)
            self.btnBuscar.configure(image=inactiveButtons.buscarButton)

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


            self.vsb = Scrollbar(self.containerEsquerda,
                                 orient="vertical",
                                 width=80)
            self.hsb = Scrollbar(self.containerEsquerda,
                                 orient="horizontal",
                                 width=30)

            self.tvw = ttk.Treeview(self.containerEsquerda,
                                    style="mystyle.Treeview",
                                    columns=self.dataCols,
                                    yscrollcommand=self.vsb.set,
                                    xscrollcommand=self.hsb.set)
            self.tvw.bind("<ButtonRelease-1>", abrirOuFecharNode)

            def strCabecalho():
                if self.maquinaAutomatica:
                    return "Par de Terminais"
                else:
                    return "Cabo/PD"

            self.tvw.heading("#0", text=strCabecalho())

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
                self.tvw.column('ID', stretch=False, width=0)

            self.tvw.grid(column=0, row=0, sticky='nswe')
            self.vsb.grid(column=1, row=0, sticky='ns')
            self.hsb.grid(column=0, row=1, sticky='we')

            self.btnConfirma = Button(self.containerEsquerda,
                                      text="Carregar",
                                      font=Fontes.fonteCabecalho,
                                      bg=Cores.bgCinza,
                                      fg="white",
                                      bd=0,
                                      highlightthickness=0,
                                      relief=FLAT,
                                      image=activeButtons.confirmarButton)
            self.btnConfirma.bind("<Button-1>", listaSelectBtn)
            self.btnConfirma.grid(column=0,
                                  row=3,
                                  ipadx=5)

            populaLista()

    def setupStartStop(self):
        if Variaveis.estadoEquipamento in (1, 4) and not Variaveis.RQPreenchido:
            Variaveis.estadoEquipamento = 2

            t = tempos.TEMPOS()

            t.tomaTempoEvento(Variaveis.ID,
                              3,
                              Variaveis.idUsuarioLogado,
                              self.maquina)

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
                              self.maquina)

            self.zeraCronografo()


            self.btnSetup.config(image=activeButtons.setupButton)
            self.btnRQ.config(image=inactiveButtons.rqButton)

            if Variaveis.RQPreenchido:
                self.btnSetup.config(image=inactiveButtons.setupButton)
                self.btnStart.config(image=activeButtons.startButton)
                self.btnBuscar.config(image=inactiveButtons.buscarButton)
            else:
                self.btnBuscar.config(image=activeButtons.buscarButton)

            self.atualizaEstado()

    def zeraCronografo(self):
        self.lblRelogio.configure(text='00:00:00')

    def atualizaCronografo(self):
        if Variaveis.estadoEquipamento in (2, 3, 5):

            Variaveis.tempoAtual = (time() - Variaveis.t0) + Variaveis.tAcumulado

            horas = int(Variaveis.tempoAtual/3600)
            minutos = int((Variaveis.tempoAtual - horas*3600)/60)
            segundos = int(Variaveis.tempoAtual - (horas * 3600) - (minutos * 60))

            stringTempoAtual = '%02d:%02d:%02d' % (horas, minutos, segundos)

            self.lblRelogio.configure(text=stringTempoAtual)
            root.after(1000, self.atualizaCronografo)

    def atualizaEstado(self):
        self.lblEstado.configure(
            text=Variaveis.estados[Variaveis.estadoEquipamento])

    def popUpRQSetup(self):
        def cancelarpopUpRQSetup():
            if Variaveis.estadoEquipamento == 3:
                Variaveis.estadoEquipamento = 2

                if Variaveis.virtualNumPadVisible:
                    self.popUpVNumPad.destroy()
                    Variaveis.virtualNumPadVisible = False

                self.popUpRQSetupScreen.destroy()

                self.btnRQ.configure(image=activeButtons.rqButton)

        def abrirPopUpRQSetup():
            if Variaveis.estadoEquipamento == 2 and not Variaveis.RQPreenchido:
                Variaveis.estadoEquipamento = 3

                UN = Variaveis.ultimaNorma
                NA = Variaveis.campos['NORMA']
                UA1 = Variaveis.ultimoAcabamento1
                A1A = Variaveis.campos['ACABAMENTO_1']
                UA2 = Variaveis.ultimoAcabamento2
                A2A = Variaveis.campos['ACABAMENTO_2']

                print('---Carregando PD ---')
                print('Ultima Norma: {}'.format(UN))
                print('Norma Atual: {} \n'.format(NA))
                print('Ultimo Acab1: {}'.format(UA1))
                print('Acab1 Atual: {} \n'.format(A1A))
                print('Ultimo Acab2: {}'.format(UA2))
                print('Acab2 Atual: {} \n'.format(A2A))

                Variaveis.exigeRegQual = not (UN == NA and (
                                         ((A1A == UA1) and (A2A == UA2)) or
                                         ((A1A == UA2) and (A2A == UA1))))

                print('exigeRegQual: {} \n'.format(Variaveis.exigeRegQual))

                self.btnRQ.configure(image=inactiveButtons.rqButton)

                def montaScreen():
                    self.popUpRQSetupScreen = Toplevel(bg=Cores.bgCinza,
                                                 bd=7,
                                                 relief=RAISED)
                    self.popUpRQSetupScreen.overrideredirect(1)
                    self.popUpRQSetupScreen.attributes('-topmost', 'true')
                    self.popUpRQSetupScreen.bind('<Escape>', cancelarpopUpRQSetup)
                    self.popUpRQSetupScreen.geometry('+50+50')
                    self.popUpRQSetupScreen.focus()

                    self.frameCamposRQ = Frame(self.popUpRQSetupScreen,
                                               bg=Cores.bgCinza)
                    self.frameCamposRQ.pack(side=TOP,
                                            fill=BOTH,
                                            expand=1,
                                            padx=15,
                                            pady=(5,10))

                    self.frameBotoesRQ = Frame(self.popUpRQSetupScreen,
                                               bg=Cores.bgCinza)
                    self.frameBotoesRQ.pack(side=BOTTOM,
                                            fill=X,
                                            expand=1,
                                            padx=10,
                                            pady=10)

                def montaWidgets():
                    def registraRQSetup():
                        if Variaveis.virtualNumPadVisible:
                            self.popUpVNumPad.destroy()
                            Variaveis.virtualNumPadVisible = False

                        pd = PD
                        self.dadosRQ = []

                        def registraPriMedida():

                            if (self.entryPriMedida.get() not in ('0', '')):
                                registro = []
                                registro.append(Variaveis.campos.get("PK_IRP"))
                                registro.append(1)
                                try: registro.append(
                                    float(
                                        self.entryPriMedida.get().replace(',',
                                                                          '.')))
                                except:
                                    self.lblMensagem.config(
                                        text='Digite corretamente um valor de medida'
                                    )
                                registro.append(0)
                                registro.append(Variaveis.idUsuarioLogado)
                                registro.append(self.maquina)
                                self.dadosRQ.append(list(registro))

                            else:
                                self.entryPriMedida.config(bg='indian red')
                                self.lblMensagem.config(
                                    text='Informe a Primeira Medida!')

                        def registraMedidas():
                            #Todo: Salvar valores nas variaveis.ult...
                            if Variaveis.exigeRegQual:
                                for L in (1, 2):
                                    if Variaveis.campos.get(
                                            "ACABAMENTO_%s" % L) is not None:
                                        for ele in self.frameCamposRQ.winfo_children():
                                            if ele.winfo_class() == 'Entry' \
                                                    and int(
                                                ele.winfo_name()[-1:]) == L:
                                                if ele.get() in ('0',''):
                                                    ele.config(bg='indian red')
                                                    self.lblMensagem.config(
                                                        text='Informe as medidas para registro')
                                                else:
                                                    registro = []
                                                    registro.append(
                                                        Variaveis.campos.get(
                                                            "PK_IRP"))
                                                    registro.append(int(
                                                        ele.winfo_name()[-2:-1]))
                                                    try:
                                                        registro.append(float(
                                                            ele.get().replace(',',
                                                                              '.')))
                                                    except:
                                                        self.lblMensagem.config(
                                                            text='Digite corretamente um valor de medida')
                                                    registro.append(
                                                        int(ele.winfo_name()[-1:]))
                                                    registro.append(
                                                        Variaveis.idUsuarioLogado)
                                                    registro.append(
                                                        self.maquina)
                                                    self.dadosRQ.append(registro)
                                                    print(self.dadosRQ)
                                                    Variaveis.ultimoRegistro = self.dadosRQ
                            else:
                                self.dadosRQ = Variaveis.ultimoRegistro

                        registraPriMedida()

                        if self.maquinaAutomatica == 'True':
                            registraMedidas()

                        if self.lblMensagem['text'] == '':
                            if Variaveis.virtualNumPadVisible:
                                self.popUpVNumPad.destroy()
                                Variaveis.virtualNumPadVisible = False

                            try:
                                self.dadosRQ = list(self.dadosRQ)
                                pd.registraRQSetup(0, Variaveis.ID, self.dadosRQ)
                                Variaveis.RQPreenchido = True
                                Variaveis.ultimaNorma = Variaveis.campos['NORMA']
                                Variaveis.ultimoAcabamento1 = Variaveis.campos['ACABAMENTO_1']
                                Variaveis.ultimoAcabamento2 = Variaveis.campos['ACABAMENTO_2']

                                print('\n --- Registrando no banco ---')
                                print('NewUltima Norma: {}'.format(
                                    Variaveis.ultimaNorma))
                                print('NewUltimo Acab1: {}'.format(
                                    Variaveis.ultimoAcabamento1))
                                print('NewUltimo Acab2: {}'.format(
                                    Variaveis.ultimoAcabamento2))
                            except:
                                self.lblMensagem['text'] = 'Erro ao salvar os registros!'


                            if Variaveis.RQPreenchido:
                                self.popUpRQSetupScreen.destroy()
                                Variaveis.estadoEquipamento = 2

                    def configWidgets():
                        self.btnConfirmaRQ = Button(self.frameBotoesRQ,
                                                text="Confirmar",
                                                font=Fontes.fontePadrao,
                                                bg=Cores.bgCinza,
                                                fg='white',
                                                relief=FLAT,
                                                bd=0,
                                                highlightthickness=0,
                                                image=activeButtons.confirmarButton)
                        self.btnConfirmaRQ["command"] = registraRQSetup

                        self.btnCancelaRQ = Button(self.frameBotoesRQ,
                                                   text="Cancelar",
                                                   font=Fontes.fontePadrao,
                                                   bg=Cores.bgCinza,
                                                   fg='white',
                                                   relief=FLAT,
                                                   bd=0,
                                                   highlightthickness=0,
                                                   image=redButtons.cancelarButton)
                        self.btnCancelaRQ["command"] = cancelarpopUpRQSetup

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
                                                    name='entry10',
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
                                                          name='entry31',
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
                                                          name='entry32',
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
                                                          name='entry41',
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
                                                          name='entry42',
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
                                                  name='entry51',
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
                                                  name='entry52',
                                                  width=10,
                                                  bg='lightcyan2',
                                                  disabledbackground='dark slate gray',
                                                  font=Fontes.fonteCabecalho,
                                                  justify=CENTER)
                        self.entryTracaoB.bind("<Button-1>",
                                                       lambda x:
                                                       self.virtualNumPad(
                                                           self.entryTracaoB))

                        self.lblMensagem = Label(self.frameBotoesRQ,
                                                 text= '',
                                                 font=Fontes.fontePadrao,
                                                 bg=Cores.bgCinza,
                                                 fg='red',
                                                 justify=CENTER)
                    configWidgets()

                    def displayWidgets():
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

                        if self.maquinaAutomatica == 'True' and Variaveis.exigeRegQual:
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

                        self.lblMensagem.pack(side=TOP,
                                              anchor='center',
                                              fill=X,
                                              expand=1)
                        self.btnConfirmaRQ.pack(side=LEFT,
                                                anchor='center',
                                                fill=X,
                                                expand=1)
                        self.btnCancelaRQ.pack(side=LEFT,
                                               anchor='center',
                                               fill=X,
                                               expand=1)
                    displayWidgets()

                def desabilitaLadosNaoUtilizados():
                    if Variaveis.campos["ACABAMENTO_1"] is None:
                        self.entryAlturaCondutorA.config(state='disabled')
                        self.entryAlturaIsolanteA.config(state='disabled')
                        self.entryTracaoA.config(state='disabled')
                    if Variaveis.campos["ACABAMENTO_2"] is None:
                        self.entryAlturaCondutorB.config(state='disabled')
                        self.entryAlturaIsolanteB.config(state='disabled')
                        self.entryTracaoB.config(state='disabled')

                montaScreen()
                montaWidgets()
                desabilitaLadosNaoUtilizados()

        abrirPopUpRQSetup()

    def virtualNumPad(self, parent):
        parent.configure(bg='lightgreen')
        parent.delete(0, END)

        self.lblMensagem.config(text='')

        if Variaveis.virtualNumPadVisible:
            self.popUpVNumPad.destroy()
            Variaveis.virtualNumPadVisible = False
            self.virtualNumPad(parent)

        elif not Variaveis.virtualNumPadVisible:
            Variaveis.virtualNumPadVisible = True

            self.popUpVNumPad = Toplevel(bg=Cores.bgCinza,
                                         bd=7,
                                         relief=RAISED)
            self.popUpVNumPad.overrideredirect(1)
            self.popUpVNumPad.attributes('-topmost', 'true')
            self.popUpVNumPad.bind('<Escape>',
                                   lambda e: self.popUpVNumPad.destroy())
            self.popUpVNumPad.geometry('+700+50')
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

    def corteStartStop(self):
        if Variaveis.estadoEquipamento == 4 and Variaveis.RQPreenchido:
            Variaveis.estadoEquipamento = 5

            self.btnStart.config(image=redButtons.finalizarButton)

            t = tempos.TEMPOS()

            t.tomaTempoEvento(Variaveis.ID,
                              5,
                              Variaveis.idUsuarioLogado,
                              self.maquina)

            Variaveis.tAcumulado = 0
            Variaveis.t0 = time()

            self.atualizaCronografo()

            self.atualizaEstado()

        elif Variaveis.estadoEquipamento == 5:
            def abrirPopUpQtdCortada():
                def registraRQCorte():
                    if Variaveis.virtualNumPadVisible:
                        self.popUpVNumPad.destroy()
                        Variaveis.virtualNumPadVisible = False

                    dados = []

                    def limpaTela():
                        for i in range(len(Variaveis.colunas)):
                            Variaveis.campos[Variaveis.colunas[i]] = ''

                        for ele in root.winfo_children():
                            ele.destroy()

                        Cores.bgCorDoCabo = "white"
                        Cores.bgCorDaListra = "white"
                        Cores.fgCorDoCabo = "#333333"
                        Variaveis.quantidadePendente = None

                    def registraNoBanco():
                        if self.lblMensagem['text'] == '' and not \
                        Variaveis.quantidadeDivergente:
                            self.lblMensagem.config(
                                text="Registrando no Banco de Dados",
                                fg=Cores.letraVerde)
                            self.popUpQtdCortada.update()

                            if Variaveis.virtualNumPadVisible:
                                self.popUpVNumPad.destroy()
                                Variaveis.virtualNumPadVisible = False

                            try:
                                pd = PD

                                pd.registraRQSetup(0, Variaveis.ID, dados)

                                t = tempos.TEMPOS()

                                t.tomaTempoEvento(Variaveis.ID,
                                                  6,
                                                  Variaveis.idUsuarioLogado,
                                                  self.maquina)
                                t.tomaTempoEvento(Variaveis.ID,
                                                  2,
                                                  Variaveis.idUsuarioLogado,
                                                  self.maquina)

                                novaQtdCortada = int(Variaveis.quantidadeCortada) + int(Variaveis.campos.get(
                                    "QTD_CORTADA"))

                                pd.registraCorteNoBanco(0, Variaveis.ID,
                                                        novaQtdCortada)

                                try:
                                    self.Etiqueta()
                                except:
                                    self.lblMensagem.config(
                                    text='Erro ao imprimir a etiqueta'
                                )

                                Variaveis.RQPreenchido = True

                                self.popUpQtdCortada.destroy()
                                Variaveis.estadoEquipamento = 0

                                Variaveis.RQPreenchido = False
                                limpaTela()
                                self.montaTelaPrincipal()

                            except:
                                self.lblMensagem.config(
                                    text='Erro ao salvar os registros'
                                )

                    def justificativaDivergencia():
                        def confirmaJustificativa():
                            item = self.listaDivergencias.curselection()


                            self.divergenciaScreen.destroy()
                            self.lblMensagem.config(text='')
                            Variaveis.quantidadeDivergente = False
                            registraNoBanco()

                        def cancelaJustificativa():
                            self.divergenciaScreen.destroy()

                        def montaScreen():
                            self.divergenciaScreen = Toplevel(bg=Cores.bgCinza,
                                                              bd=7,
                                                              relief=RAISED)
                            self.divergenciaScreen.overrideredirect(1)
                            self.divergenciaScreen.attributes('-topmost',
                                                              'true')
                            self.divergenciaScreen.bind('<Escape>', lambda
                                x: cancelaJustificativa())
                            self.divergenciaScreen.geometry('+50+50')
                            self.divergenciaScreen.focus()

                            self.containerSuperior = Frame(self.divergenciaScreen,
                                                           bg=Cores.bgCinza)
                            self.containerSuperior.pack(side=TOP,
                                                        fill=BOTH,
                                                        expand=1)

                            self.containerInferior = Frame(self.divergenciaScreen,
                                                           bg=Cores.bgCinza)
                            self.containerInferior.pack(side=BOTTOM,
                                                        fill=BOTH,
                                                        expand=0)

                        def montaWidgets():
                            def carregaLista():
                                mot = MOTIVOS()
                                listaMotivos = mot.buscaListaMotivosDivergencia()

                                for motivo in listaMotivos:
                                    self.listaDivergencias.insert(END, motivo)

                            self.vsb = Scrollbar(self.containerSuperior,
                                                 orient="vertical",
                                                 width=80)

                            self.listaDivergencias = Listbox(
                                self.containerSuperior,
                                bg=Cores.bgAcabamentosAux,
                                fg='black',
                                font=('Play', 18),
                                yscrollcommand=self.vsb.set)
                            self.listaDivergencias.pack(side=LEFT,
                                                        fill=BOTH,
                                                        expand=1,
                                                        padx=10,
                                                        pady=(15, 0))

                            self.vsb['command'] = self.listaDivergencias.yview

                            self.vsb.pack(side=LEFT,
                                          padx=(0, 15),
                                          fill=Y)

                            self.btnConfirmaDiv = Button(
                                self.containerInferior,
                                text="Confirmar",
                                font=Fontes.fontePadrao,
                                bg=Cores.bgCinza,
                                fg='white',
                                relief=FLAT,
                                image=activeButtons.confirmarButton)
                            self.btnConfirmaDiv[
                                "command"] = lambda: confirmaJustificativa()
                            self.btnConfirmaDiv.pack(side=TOP,
                                                     pady=20)

                            carregaLista()

                        montaScreen()
                        montaWidgets()

                    def registraQtdCortada():
                        if (self.entryQtdCortada.get() not in ('')):
                            try:
                                Variaveis.quantidadeCortada = int(
                                    self.entryQtdCortada.get()
                                )
                            except:
                                self.lblMensagem.config(
                                    text='Digite corretamente a quantidade cortada')

                            if int((Variaveis.quantidadeCortada)) < int(
                                    Variaveis.quantidadePendente):
                                # print("QTD DIVERGENTE")
                                self.lblMensagem.config(
                                    text='Quantidade divergente. Justifique!')
                                Variaveis.quantidadeDivergente = True
                                justificativaDivergencia()

                            elif int((Variaveis.quantidadeCortada)) > int(
                                    Variaveis.quantidadePendente):
                                self.lblMensagem.config(text='A quantidade cortada não pode ser maior que a quantidade a cortar'
                                )
                                self.entryQtdCortada.config(bg='indian red')

                            else:
                                Variaveis.quantidadeDivergente = False
                                try:
                                    registraNoBanco()
                                except:
                                    self.lblMensagem.config(text='Erro ao registrar no Banco')


                        else:
                            self.entryQtdCortada.config(bg='indian red')
                            self.lblMensagem.config(
                                text='Informe a Quantidade Cortada!')

                    def registraUltMedida():
                        if (self.entryUltMedida.get() not in ('0', '')):
                            registro = []
                            registro.append(Variaveis.campos.get("PK_IRP"))
                            registro.append(2)
                            try:
                                registro.append(
                                    float(
                                        self.entryUltMedida.get().replace(
                                            ',',
                                            '.')))
                            except:
                                self.lblMensagem.config(
                                    text='Digite corretamente um valor de medida'
                                )
                            registro.append(0)
                            registro.append(Variaveis.idUsuarioLogado)
                            registro.append(self.maquina)
                            dados.append(list(registro))
                            registraQtdCortada()
                        else:
                            self.entryUltMedida.config(bg='indian red')
                            self.lblMensagem.config(
                                text='Informe a Ultima Medida!')


                    registraUltMedida()

                def montaScreen():
                    def fechaPopUpQtdCortada():
                        if Variaveis.virtualNumPadVisible:
                            self.popUpVNumPad.destroy()
                            Variaveis.virtualNumPadVisible = False
                        self.popUpQtdCortada.destroy()

                    self.popUpQtdCortada = Toplevel(bg=Cores.bgCinza,
                                                 bd=7,
                                                 relief=RAISED)
                    self.popUpQtdCortada.overrideredirect(1)
                    self.popUpQtdCortada.attributes('-topmost', 'true')
                    self.popUpQtdCortada.bind('<Escape>',
                                              lambda e:fechaPopUpQtdCortada())
                    self.popUpQtdCortada.geometry('+100+100')
                    self.popUpQtdCortada.focus()

                def montaWidgets():
                    self.btnConfirma = Button(self.popUpQtdCortada,
                                                text="Confirmar",
                                                font=Fontes.fontePadrao,
                                                bg=Cores.bgCinza,
                                                fg='white',
                                                relief=FLAT,
                                                image=activeButtons.confirmarButton)
                    self.btnConfirma["command"] = registraRQCorte

                    self.lblRegQualidade = Label(self.popUpQtdCortada,
                                                 text="REGISTROS DE QUALIDADE",
                                                 font=Fontes.fonteCabecalho,
                                                 bg=Cores.bgCinza,
                                                 fg='azure2',
                                                 justify=CENTER)

                    self.lblUltMedida = Label(self.popUpQtdCortada,
                                              text="ÚLTIMA MEDIDA (mm)",
                                              font=Fontes.fontePadrao,
                                              bg=Cores.bgCinza,
                                              fg=Cores.letraVerde,
                                              justify=CENTER)

                    self.entryUltMedida = Entry(self.popUpQtdCortada,
                                                width=10,
                                                bg='lightcyan2',
                                                disabledbackground='dark slate gray',
                                                font=Fontes.fonteCabecalho,
                                                justify=CENTER)
                    self.entryUltMedida.bind("<Button-1>",
                                             lambda x:self.virtualNumPad(
                                                 self.entryUltMedida))

                    self.lblQtdCortada = Label(self.popUpQtdCortada,
                                               text="QUANTIDADE CORTADA:",
                                               font=Fontes.fontePadrao,
                                               bg=Cores.bgCinza,
                                               fg=Cores.letraVerde,
                                               justify=CENTER)

                    self.entryQtdCortada = Entry(self.popUpQtdCortada,
                                                width=10,
                                                bg='lightcyan2',
                                                disabledbackground='dark slate gray',
                                                font=Fontes.fonteCabecalho,
                                                justify=CENTER)
                    self.entryQtdCortada.bind("<Button-1>",
                                             lambda x:
                                             self.virtualNumPad(
                                                 self.entryQtdCortada))

                    self.lblQtdACortar = Label(self.popUpQtdCortada,
                                               text="Pendente: %s" % Variaveis.quantidadePendente,
                                               font=['Play', 11],
                                               bg=Cores.bgCinza,
                                               fg='white',
                                               anchor="center")

                    self.lblMensagem = Label(self.popUpQtdCortada,
                                             text='',
                                             font=Fontes.fontePadrao,
                                             bg=Cores.bgCinza,
                                             fg='red',
                                             justify=CENTER)

                    self.lblRegQualidade.pack(side=TOP,
                                              fill=X,
                                              expand=1,
                                              padx=20,
                                              pady=20)

                    self.lblUltMedida.pack(side=TOP,
                                           fill=X,
                                           padx=20,
                                           pady=10,
                                           expand=1)

                    self.entryUltMedida.pack(side=TOP,
                                             padx=20,
                                             pady=(0,20))

                    self.lblQtdCortada.pack(side=TOP,
                                            fill=X,
                                            padx=20,
                                            pady=10,
                                            expand=1)

                    self.entryQtdCortada.pack(side=TOP,
                                              padx=20,
                                              pady=(0,5))

                    self.lblQtdACortar.pack(side=TOP,
                                            padx=5,
                                            pady=(0,5))

                    self.btnConfirma.pack(side=BOTTOM,
                                          pady=(5,25))

                    self.lblMensagem.pack(side=BOTTOM)

                montaScreen()
                montaWidgets()

            abrirPopUpQtdCortada()

    def paradaDeMaquina(self):
        self.idMotivo = None
        if not Variaveis.maquinaParada and Variaveis.estadoEquipamento > 0:
            def retomar():
                t = tempos.TEMPOS()

                t.tomaTempoParada(Variaveis.ID,
                                  8,
                                  Variaveis.idUsuarioLogado,
                                  self.maquina,
                                  self.idMotivo)

                Variaveis.estadoEquipamento = Variaveis.estadoAntesDaParada
                Variaveis.t0 = time()
                self.atualizaCronografo()

                if Variaveis.paradaEmCorte:
                    Variaveis.paradaEmCorte = False
                    t.tomaTempoEvento(Variaveis.ID,
                                      Variaveis.estadoEquipamento,
                                      Variaveis.idUsuarioLogado,
                                      self.maquina)

                if Variaveis.paradaEmSetup:
                    Variaveis.paradaEmSetup = False
                    t.tomaTempoEvento(Variaveis.ID,
                                          3,
                                          Variaveis.idUsuarioLogado,
                                          self.maquina)


                Variaveis.maquinaParada = False
                self.popUpParada.destroy()

            def atualizaCronografoParada():
                if Variaveis.maquinaParada:

                    tempoAtualParada = (time() - Variaveis.t0Parada)
                    horas = int(tempoAtualParada / 3600)
                    minutos = int((tempoAtualParada - horas * 3600) / 60)
                    segundos = int(
                        tempoAtualParada - (horas * 3600) - (minutos * 60))

                    tempoAtualParada = '%02d:%02d:%02d' % (horas, minutos, segundos)

                    self.cronometroParada.config(text=tempoAtualParada)
                    root.after(1000, atualizaCronografoParada)

            def cronometroParada():
                Variaveis.t0Parada = time()

                for frame in (self.frameButtons.winfo_children(),
                              self.frameLista.winfo_children()):
                    for ele in frame:
                        ele.destroy()

                self.lblDescMotivo = Label(self.frameLista,
                                           bg=Cores.bgCinza,
                                           text=self.descMotivo,
                                           fg='red',
                                           font=("Play", 36, 'bold'))

                self.lblDescMotivo.pack(side=TOP,
                                        fill=X,
                                        expand=1)

                self.cronometroParada = Label(self.frameLista,
                                              bg=Cores.bgCinza,
                                              text='00:00:00',
                                              fg='red',
                                              font=("Play", 72, 'bold'))

                self.cronometroParada.pack(side=TOP,
                                           fill=BOTH,
                                           expand=1)

                self.btnRetomar = Button(self.frameButtons,
                                          text="Retomar",
                                          font=Fontes.fontePadrao,
                                          bg=Cores.bgCinza,
                                          fg='white',
                                          relief=FLAT,
                                          image=activeButtons.retomarButton)
                self.btnRetomar["command"] = retomar
                self.btnRetomar.pack(side=TOP)

                atualizaCronografoParada()

            def registraParadaNoBanco():
                t = tempos.TEMPOS()

                t.tomaTempoParada(Variaveis.ID,
                                  Variaveis.estadoEquipamento,
                                  Variaveis.idUsuarioLogado,
                                  self.maquina,
                                  self.idMotivo)

                if Variaveis.estadoAntesDaParada == 5:
                    Variaveis.paradaEmCorte = True
                    t.tomaTempoEvento(Variaveis.ID,
                                      Variaveis.estadoAntesDaParada+1,
                                      Variaveis.idUsuarioLogado,
                                      self.maquina)

                if Variaveis.estadoAntesDaParada in (2,3):
                    Variaveis.paradaEmSetup = True
                    t.tomaTempoEvento(Variaveis.ID,
                                      4,
                                      Variaveis.idUsuarioLogado,
                                      self.maquina)

                cronometroParada()

            def confirmaParada():
                try:
                    Variaveis.maquinaParada = True

                    iP = self.listaParadas.curselection()
                    self.idMotivo = iP[0]
                    self.descMotivo = self.listaParadas.get(iP[0])

                    Variaveis.estadoAntesDaParada = Variaveis.estadoEquipamento
                    Variaveis.estadoEquipamento = 7

                    registraParadaNoBanco()

                    Variaveis.tAcumulado = Variaveis.tempoAtual
                except:
                    self.lblMensagem.config(text='Justifique sua parada!',
                                            bg='yellow')

            def cancelaParada():
                Variaveis.maquinaParada = False
                self.popUpParada.destroy()

            def montaScreen():
                self.popUpParada = Toplevel(bg=Cores.bgCinza)
                self.popUpParada.overrideredirect(1)
                self.popUpParada.attributes('-topmost', 'true')
                # self.popUpParada.bind('<Escape>',
                #                           lambda e: cancelaParada())
                self.popUpParada.geometry(Definicoes.configFile['DISPLAY']['RES'])
                self.popUpParada.focus()

                self.frameTitulo = Frame(self.popUpParada,
                                 bg=Cores.bgCinza)
                self.frameTitulo.pack(side=TOP,
                                      pady=(20,5))

                self.frameLista = Frame(self.popUpParada,
                                        bg=Cores.bgCinza)
                self.frameLista.pack(side=TOP,
                                     fill=BOTH,
                                     expand=1,
                                     pady=(5,20),
                                     padx=20)

                self.frameButtons = Frame(self.popUpParada,
                                          bg=Cores.bgCinza)
                self.frameButtons.pack(side=BOTTOM,
                                       pady=(30,25))

            def montaWidgets():
                def carregaLista():
                    mot = MOTIVOS()
                    listaMotivos = mot.buscaListaMotivosParada()

                    for motivo in listaMotivos:
                        self.listaParadas.insert(END, motivo)

                self.lblTitulo = Label(self.frameTitulo,
                                       text="PARADA DE MÁQUINA",
                                       font=Fontes.fonteCabecalho,
                                       bg=Cores.bgCinza,
                                       fg='red',
                                       justify=CENTER)

                self.vsb = Scrollbar(self.frameLista,
                                     orient="vertical",
                                     width=80)

                self.listaParadas = Listbox(self.frameLista,
                                            bg=Cores.bgAcabamentosAux,
                                            fg='black',
                                            yscrollcommand=self.vsb.set,
                                            font=('Play', 18))

                self.vsb['command'] = self.listaParadas.yview

                self.lblMensagem = Label(self.frameButtons,
                                         text='',
                                         font=Fontes.fontePadrao,
                                         fg='red',
                                         bg=Cores.bgCinza)

                self.btnConfirma = Button(self.frameButtons,
                                          text="Confirmar",
                                          font=Fontes.fontePadrao,
                                          bg=Cores.bgCinza,
                                          fg='white',
                                          relief=FLAT,
                                          bd=0,
                                          highlightthickness=0,
                                          image=activeButtons.confirmarButton)
                self.btnConfirma["command"] = confirmaParada

                self.btnCancela = Button(self.frameButtons,
                                         text="Cancelar",
                                         font=Fontes.fontePadrao,
                                         bg=Cores.bgCinza,
                                         fg='white',
                                         relief=FLAT,
                                         image=redButtons.cancelarButton)
                self.btnCancela["command"] = cancelaParada

                self.lblTitulo.pack(side=LEFT,
                                    pady=(20,10),
                                    fill=BOTH,
                                    expand=1)

                self.listaParadas.pack(side=LEFT,
                                       fill=BOTH,
                                       expand=1,
                                       padx=(15,0))

                self.vsb.pack(side=LEFT,
                              padx=(0,15),
                              fill=Y)

                self.lblMensagem.pack(side=TOP,
                                      fill=X,
                                      expand=1)

                self.btnConfirma.pack(side=LEFT)

                self.btnCancela.pack(side=LEFT)

                carregaLista()

            montaScreen()
            montaWidgets()

    def Etiqueta(self):
        etq = etiqueta.etiqueta()
        etq.imprimeEtiqueta(Variaveis.quantidadeCortada, Variaveis.nomeUsuarioLogado, **Variaveis.campos)

    def PopUpCabo(self):
        def montaScreen():
            self.PopUpCaboScreen = Toplevel(bg=Cores.bgCinza,
                                            bd=7,
                                            relief=RAISED)
            self.PopUpCaboScreen.overrideredirect(1)
            self.PopUpCaboScreen.attributes('-topmost', 'true')
            self.PopUpCaboScreen.bind("<Button-1>", lambda e: self.PopUpCaboScreen.destroy())
            self.PopUpCaboScreen.geometry('+50+150')
            self.PopUpCaboScreen.focus()

            self.lblCaboExt = Label(self.PopUpCaboScreen,
                                    text="CPD: %s \nCabo: %s" % (
                                    Variaveis.campos.get("CPD"),
                                    Variaveis.campos.get("CABO")),
                                    font=Fontes.fonteCabecalho,
                                    bg=Cores.bgCinza,
                                    fg="white",
                                    bd=0,
                                    height=4,
                                    justify=LEFT)
            self.lblCaboExt.pack(side=TOP,
                                 padx=20,
                                 pady=15,
                                 expand=1,
                                 fill=X)

        montaScreen()

    def AbreMenu(self):
        if Variaveis.estadoEquipamento in (0, 6):
            def montaTelaMenu():
                self.popUpMenu = Toplevel(bg=Cores.bgCinza)
                self.popUpMenu.overrideredirect(1)
                self.popUpMenu.attributes('-topmost', 'true')
                # self.popUpMenu.bind("<Escape>",
                #                               lambda
                #                                   e: self.popUpMenu.destroy())
                self.popUpMenu.geometry(Definicoes.configFile['DISPLAY']['RES'])
                self.popUpMenu.option_add('*TCombobox*Listbox.font',
                                ('Play', 24))

            montaTelaMenu()
            configMenu.Menu(self, self.popUpMenu)


Application(root)
root.mainloop()
