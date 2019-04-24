#--- Imports ---#
from pd import PD
from tkinter import *
from time import sleep, time
from tkinter import ttk
#import login
import configparser as cfgprsr


class configuracoes():
    configFile = cfgprsr.ConfigParser()
    configFile.read('config.ini')
    maquina = configFile['DEFAULT']['Maquina']


root = Tk()
root.title('Operação')
root.geometry(configuracoes.configFile['DISPLAY']['RES'])
root.attributes('-fullscreen', configuracoes.configFile['DISPLAY']['Tela Cheia'])
root.bind('<Escape>',lambda e: root.destroy())
root.resizable(width=True, height=True)


class variaveis():
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


class cores():
    # Cores padrão do aplicativo
    bgCinza= "#333333"
    bgVerde     = "#00d455"
    letraVerde  = "#66ff00"


class imagens():
    #--- IMAGENS ---#
    logo                = PhotoImage(file="src/images/logos/logo.png")
    startButton         = PhotoImage(file="src/images/buttons/startButton.png")
    stopButton          = PhotoImage(file="src/images/buttons/stopButton.png")
    searchButton        = PhotoImage(file="src/images/buttons/searchButton.png")
    setupStartButton    = PhotoImage(file="src/images/buttons/setupStartButton.png")
    setupStopButton     = PhotoImage(file="src/images/buttons/setupStopButton.png")
    pularButton         = PhotoImage(file="src/images/buttons/pularButton.png")
    paradaButton        = PhotoImage(file="src/images/buttons/paradaButton.png")
    retomarButton       = PhotoImage(file="src/images/buttons/retomarButton.png")
    menuButton          = PhotoImage(file="src/images/buttons/menuButton.png")


#--- Declaração de Classe ---#
class Application:

    def __init__(self, master=None):
        #Log = LOGIN.sts

        #if Log == True:
            self.montaTela()
            self.exibeLista()
    def montaTela(self, master=None):
        #--- Fonte Padrão ---#
        self.fonte = ("Play", 12)

        #--- Containers ---#
        ##--- Cabecalho ----##
        self.containerCabecalho = Frame(master, bd=5, bg=cores.bgCinza)
        self.containerCabecalho["padx"] = 5
        self.containerCabecalho.pack(fill=X, side=TOP)

        ##--- Menu Botoes ---##
        self.containerBotoes = Frame(master, bg=cores.bgCinza)
        self.containerBotoes["padx"] = 0
        self.containerBotoes["pady"] = 10
        self.containerBotoes.pack(side=RIGHT, fill=Y, expand=0)

        ##--- Esquerda ---##
        self.containerEsquerda = Frame(master, bg=cores.bgCinza)
        self.containerEsquerda.pack(side=LEFT, fill=BOTH, expand=1)

        ###--- Dados PD ---###
        self.containerDadosPD = Frame(self.containerEsquerda, bg=cores.bgCinza)
        self.containerDadosPD.pack(fill=BOTH, expand=1, padx=(0,20))

        ####--- Cabecalho PD ---####
        self.containerCabecalhoPD = Frame(self.containerDadosPD, bg=cores.bgCinza)
        self.containerCabecalhoPD.pack(fill=X, pady=(20,35), padx=20)

        ####--- Medidas PD ---####
        self.containerMedidasPD = Frame(self.containerDadosPD, bg=cores.bgCinza)
        self.containerMedidasPD.pack()

        ####--- Cabo ---###
        self.containerCabo = Frame(self.containerDadosPD, bg=cores.bgCinza)
        self.containerCabo.pack()

        ####--- Detalhes PD ---####
        self.containerDetalhesPD = Frame(self.containerDadosPD, bg=cores.bgCinza)
        self.containerDetalhesPD.pack(fill=X, expand=1)

        #####--- Acabamentos Lado A ---#####
        self.containerLadoA = Frame(self.containerDetalhesPD, bg=cores.bgCinza)
        self.containerLadoA.pack(side=LEFT)

        ######--- Acabamento 1 ---######
        self.containerAcabamento1 = Frame(self.containerLadoA, bg="#00d455")
        self.containerAcabamento1.pack(side=TOP, pady=10)

        ######--- Acabamento 3 ---######
        self.containerAcabamento3 = Frame(self.containerLadoA, bg="#cccccc")
        self.containerAcabamento3.pack(side=TOP)

        #####--- Detalhes Meio ---#####
        self.containerDetalhesMeio = Frame(self.containerDetalhesPD, bg=cores.bgCinza)
        self.containerDetalhesMeio.pack(side=LEFT, fill=X, expand=1)

        ######--- Quantidade ---######
        self.containerQuantidade = Frame(self.containerDetalhesMeio, bg=cores.bgCinza)
        self.containerQuantidade.pack(fill=BOTH, expand=1)

        ######--- Observação ---######
        self.containerObservacao = Frame(self.containerDetalhesMeio, bg=cores.bgCinza)
        self.containerObservacao.pack(fill=X, expand=1)

        ######--- Gravação ---######
        self.containerGravacao = Frame(self.containerDetalhesMeio, bg=cores.bgCinza)
        self.containerGravacao.pack(fill=X, expand=1)

        #####--- Acabamentos Lado B ---#####
        self.containerLadoB = Frame(self.containerDetalhesPD, bg=cores.bgCinza)
        self.containerLadoB.pack(side=RIGHT)

        ######--- Acabamento 2 ---######
        self.containerAcabamento2 = Frame(self.containerLadoB, bg="#00d455")
        self.containerAcabamento2.pack(side=TOP, pady=10)

        ######--- Acabamento 4 ---######
        self.containerAcabamento4 = Frame(self.containerLadoB, bg="#ccc")
        self.containerAcabamento4.pack(side=TOP)

        ###--- Rodape ---###
        self.containerRodape = Frame(self.containerEsquerda, bg="#454545")
        self.containerRodape.pack(side=BOTTOM, ipadx=100)

        ####--- Proximo Cabo ---####
        self.containerProxCabo = Frame(self.containerRodape, bg="#454545")
        self.containerProxCabo.pack(side=TOP, fill=X, expand=1)

        ####--- Label Prox Medidas ---####
        self.containerProxMedidas = Frame(self.containerRodape, bg="#454545")
        self.containerProxMedidas.pack()



        #--- Labels ---#
        ##------ Cabeçalho ------##
        self.logo = Label(self.containerCabecalho, text="Datateck", font=("Play", 18, "bold"), image=imagens.logo, bg=cores.bgCinza, fg="white")
        self.logo.pack(side=LEFT)

        self.maquina = Label(self.containerCabecalho, text=configuracoes.maquina, bg=cores.bgCinza, fg="white")
        self.maquina["font"] = ("Play", "18", "bold")
        self.maquina.pack(side=LEFT, fill=X, expand=1)

        self.relogio = Label(self.containerCabecalho, text="00:00:00", padx=10, fg=cores.letraVerde, bg=cores.bgCinza)
        self.relogio["font"] = ("Play", "18", "bold")
        self.relogio.pack(side=LEFT)

        ##--- Dados PD ---##
        ###--- Cabecalho PD ---###
        self.lblReq = Label(self.containerCabecalhoPD, text="Requisição: %s" % (variaveis.REQNUM.get()), bg=cores.bgCinza, fg="white", font=self.fonte, anchor="w")
        self.lblReq.pack(side=LEFT)

        self.lblPD = Label(self.containerCabecalhoPD, text="PD: %s" % variaveis.PDNUM.get(), bg=cores.bgCinza, fg=cores.letraVerde, font=("Play", 16, "bold"), anchor="center")
        self.lblPD.pack(side=LEFT, fill=X, expand=1)

        self.lblReq = Label(self.containerCabecalhoPD, text="Produto Pai: %s" % variaveis.PAI.get(), bg=cores.bgCinza, fg="white", font=self.fonte, anchor="e")
        self.lblReq.pack(side=LEFT)

        ###--- Medidas PD ---###
        self.lblDecapeA = Label(self.containerMedidasPD, text=variaveis.DECAPEA.get(), bg=cores.bgCinza, fg=cores.letraVerde, font=("Play", 16, "bold"))
        self.lblDecapeA.grid(column=0, row=0)

        self.lblMedida = Label(self.containerMedidasPD, text=variaveis.MEDIDA.get(), bg=cores.bgCinza, fg=cores.letraVerde, font=("Play", 16, "bold"), width=30)
        self.lblMedida.grid(column=1, row=0)

        self.lblDecapeB = Label(self.containerMedidasPD, text=variaveis.DECAPEB.get(), bg=cores.bgCinza, fg=cores.letraVerde, font=("Play", 16, "bold"))
        self.lblDecapeB.grid(column=2, row=0)

        ###--- Cabo ---###
        self.lblLadoACabo = Label(self.containerCabo, text="", bg="#ff9955", width=10, height=1)
        self.lblLadoACabo.grid(column=0, row=0)

        self.lblCabo = Label(self.containerCabo, text=variaveis.CABO.get(), bg="white", fg=cores.bgCinza, font=self.fonte, width=40, height=2)
        self.lblCabo.grid(column=1, row=0)

        self.lblLadoBCabo = Label(self.containerCabo, text="", bg="#ff9955", width=10, height=1)
        self.lblLadoBCabo.grid(column=2, row=0)

        ###--- Detalhes ---###

        ####--- Lado A ---####
        #####--- Acabamento 1 ---#####
        self.lblLabelAcabamento1 = Label(self.containerAcabamento1, text="Acabamento 1", bg="#00d455", fg=cores.bgCinza, font=self.fonte, width=20)
        self.lblLabelAcabamento1.pack(fill=BOTH, expand=1, pady=5)

        self.lblAcabamento1 = Label(self.containerAcabamento1, text=variaveis.ACAB1.get(), bg="#00d455", fg=cores.bgCinza, font=self.fonte)
        self.lblAcabamento1.pack(fill=BOTH, expand=1, pady=5)

        #####--- Acabamento 3 ---#####
        self.lblLabelAcabamento3 = Label(self.containerAcabamento3, text="Acabamento 3", bg="#ccc", fg=cores.bgCinza, font=self.fonte, width=20)
        self.lblLabelAcabamento3.pack(fill=BOTH, expand=1, pady=5)

        self.lblAcabamento3 = Label(self.containerAcabamento3, text=variaveis.ACAB3.get(), bg="#ccc", fg=cores.bgCinza, font=self.fonte)
        self.lblAcabamento3.pack(fill=BOTH, expand=1, pady=5)

        ####--- Quantidade ---####
        self.lblLabelQuantidade = Label(self.containerQuantidade, text="Quantidade", font=("Play", 18, "bold"), bg=cores.bgCinza, fg=cores.letraVerde)
        self.lblLabelQuantidade.pack()

        self.lblQuantidade = Label(self.containerQuantidade, text=variaveis.QUANTIDADE.get(), font=("Play", 32, "bold"), bg=cores.bgCinza, fg=cores.letraVerde, anchor="ne")
        self.lblQuantidade.pack()

        self.lblQuantidadeCortada = Label(self.containerQuantidade, text=variaveis.QUANTIDADE_CORTADA.get(), font=("Play", 16, "bold"), bg=cores.bgCinza, fg="red", anchor="sw")
        #self.lblQuantidadeCortada.bind("<Button-1>", self.clicked)
        self.lblQuantidadeCortada.pack()


        ####--- Observacao ---####
        self.lblLabelObservacao = Label(self.containerObservacao, text="Observação", font=self.fonte, bg=cores.bgCinza, fg="#999")
        self.lblLabelObservacao.pack()

        self.lblObservacao = Label(self.containerObservacao, text=variaveis.OBSERVACAO.get(), font=self.fonte, bg=cores.bgCinza, fg="white")
        self.lblObservacao.pack()

        ####--- Gravacao ---####
        self.lblLabelGravacao = Label(self.containerObservacao, text="Gravação", font=self.fonte, bg=cores.bgCinza, fg="#999")
        self.lblLabelGravacao.pack()

        self.lblGravacao = Label(self.containerObservacao, text=variaveis.GRAVACAO.get(), font=self.fonte, bg=cores.bgCinza, fg="white")
        self.lblGravacao.pack()

        ####--- Labo B ---####
        #####--- Acabamento 2 ---#####
        self.lblLabelAcabamento2 = Label(self.containerAcabamento2, text="Acabamento 2", bg="#00d455", fg=cores.bgCinza, font=self.fonte, width=20)
        self.lblLabelAcabamento2.pack(fill=BOTH, expand=1, pady=5)

        self.lblAcabamento2 = Label(self.containerAcabamento2, text=variaveis.ACAB2.get(), bg="#00d455", fg=cores.bgCinza, font=self.fonte)
        self.lblAcabamento2.pack(fill=BOTH, expand=1, pady=5)

        #####--- Acabamento 4 ---#####
        self.lblLabelAcabamento4 = Label(self.containerAcabamento4, text="Acabamento 4", bg="#ccc", fg=cores.bgCinza, font=self.fonte, width=20)
        self.lblLabelAcabamento4.pack(fill=BOTH, expand=1, pady=5)

        self.lblAcabamento4 = Label(self.containerAcabamento4, text=variaveis.ACAB4.get(), bg="#ccc", fg=cores.bgCinza, font=self.fonte)
        self.lblAcabamento4.pack(fill=BOTH, expand=1, pady=5)

        #--- Botões ---#
        self.btnStart = Button(self.containerBotoes, image=imagens.startButton, bg=cores.bgCinza, relief=FLAT, anchor="w", command=self.opera, bd=0,    highlightthickness=0)
        self.btnStart["width"] = 130
        self.btnStart["height"] = 50
        self.btnStart.pack(pady=5)

        self.btnStop = Button(self.containerBotoes, image=imagens.stopButton, bg=cores.bgCinza, relief=FLAT, anchor="w", command=self.stop, bd=0,    highlightthickness=0)
        self.btnStop["width"] = 130
        self.btnStop["height"] = 50
        self.btnStop.pack(pady=5)

        self.btnBusca = Button(self.containerBotoes, image=imagens.searchButton, bg=cores.bgCinza, anchor="w", command=self.exibeLista, bd=0, highlightthickness=0)
        self.btnBusca["width"] = 130
        self.btnBusca["height"] = 50
        self.btnBusca.pack(pady=5)

        self.btnPula = Button(self.containerBotoes, image=imagens.pularButton, bg=cores.bgCinza, relief=FLAT, anchor="w", bd=0,  highlightthickness=0)
        self.btnPula["width"] = 130
        self.btnPula["height"] = 50
        self.btnPula.pack(pady=5)

        self.btnParada = Button(self.containerBotoes, image=imagens.paradaButton, bg=cores.bgCinza, relief=FLAT, anchor="w", bd=0,  highlightthickness=0)
        self.btnParada["width"] = 130
        self.btnParada["height"] = 50
        self.btnParada.pack(pady=5)

        self.btnMenu = Button(self.containerBotoes, image=imagens.menuButton, bg=cores.bgCinza, relief=FLAT, anchor="w", bd=0,  highlightthickness=0)
        self.btnMenu["width"] = 130
        self.btnMenu["height"] = 50
        self.btnMenu.pack(pady=5)

        #--- Rodape ---#
        self.lblProxCabo = Label(self.containerProxCabo, text=variaveis.PROX_CABO.get(), bg="#454545", fg="#888")
        self.lblProxCabo.pack(side=TOP, fill=X, expand=1)

        self.lblLabelProxDecapeA = Label(self.containerProxMedidas, text="Decape A", bg="#454545", fg="#888")
        self.lblLabelProxDecapeA.grid(column=0, row=0)

        self.lblLabelProxMedida = Label(self.containerProxMedidas, text="Medida", bg="#454545", fg="#888", width=30)
        self.lblLabelProxMedida.grid(column=1, row=0)

        self.lblLabelProxDecapeB = Label(self.containerProxMedidas, text="Decape B", bg="#454545", fg="#888")
        self.lblLabelProxDecapeB.grid(column=2, row=0)

        self.lblProxDecapeA = Label(self.containerProxMedidas, text=variaveis.PROX_DECAPEA.get(), bg="#454545", fg="#888")
        self.lblProxDecapeA.grid(column=0, row=1)

        self.lblProxMedida = Label(self.containerProxMedidas, text=variaveis.PROX_MEDIDA.get(), bg="#454545", fg="#888")
        self.lblProxMedida.grid(column=1, row=1)

        self.lblProxDecapeB = Label(self.containerProxMedidas, text=variaveis.PROX_DECAPEB.get(), bg="#454545", fg="#888")
        self.lblProxDecapeB.grid(column=2, row=1)

    def limpaTela(self):
        for ele in root.winfo_children():
            ele.destroy()

        Application()

    def exibeLista(self):
        for ele in self.containerEsquerda.winfo_children():
            ele.destroy()

        self.listaCount = Label(self.containerEsquerda, bg=cores.bgCinza, fg="white", font=("Play", 12), anchor=NE)
        self.listaCount.grid(column=0, row=2, sticky='ne')

        self.containerEsquerda.grid_rowconfigure(0, weight=1)
        self.containerEsquerda.grid_columnconfigure(0, weight=1)
        self.containerEsquerda.configure(padx=15, pady=15)

        self.vsb = ttk.Scrollbar(self.containerEsquerda, orient="vertical")
        self.hsb = ttk.Scrollbar(self.containerEsquerda, orient="horizontal")

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 16), rowheight=35)
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 16, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        # self.dataCols = ('ID',
        #                'Requisição',
        #                'PD',
        #                'CABO',
        #                'DECAPE A',
        #                'DECAPE B',
        #                'MEDIDA',
        #                'ACABAMENTO 1',
        #                'ACABAMENTO 2',
        #                'OBSERVAÇÃO',
        #                'PRODUTO FINAL',
        #                'QUANTIDADE',
        #                'QTD. CORTADA',
        #                'ENTREGA',
        #                'PRIORIDADE',
        #                'MÁQUINA',
        #                'PRI. MEDIDA',
        #                'ULT. MEDIDA')

        self.dataCols = ('Medida',
                         'Quantidade',
                         'Requisição',
                         'PD')

        self.tvw = ttk.Treeview(
            self.containerEsquerda,
            style="mystyle.Treeview",
            columns=self.dataCols,
            show='tree headings')

        self.vsb['command'] = self.tvw.yview
        self.hsb['command'] = self.tvw.xview

        self.tvw.heading("#0", text="Cabo/PD")

        for field in self.dataCols:
            self.tvw.heading(field, text=str(field.title()))
            self.tvw.column(field, stretch=False, width=100)

        self.tvw.grid(column=0, row=0, sticky='nswe')
        self.vsb.grid(column=1, row=0, sticky='ns')
        self.hsb.grid(column=0, row=1, sticky='we')

        self.btnConfirma = Button(self.containerEsquerda, text="Carregar", font=("Play", 16), bg=cores.bgCinza, fg="white")
        self.btnConfirma.bind("<Button-1>", self.listaSelectBtn)
        self.btnConfirma.grid(column=0, row=3, ipadx=5)

        self.populaLista()

    def listaSelectBtn(self, master):
        self.itemSel = self.tvw.focus()
        self.itemData = self.tvw.item(self.itemSel)

        print(self.itemData)

        variaveis.ID.set(self.itemData.get('values')[4])
        variaveis.REQNUM.set(self.itemData.get('values')[2])
        variaveis.PDNUM.set(self.itemData.get('values')[3])
        variaveis.PAI.set("-")
        variaveis.DECAPEA.set("-")
        variaveis.DECAPEB.set("-")
        variaveis.MEDIDA.set(self.itemData.get('values')[0])
        variaveis.CABO.set(self.itemData.get('text'))
        variaveis.QUANTIDADE.set(self.itemData.get('values')[1])
        variaveis.QUANTIDADE_CORTADA.set("-")
        variaveis.ACAB1.set("-")
        variaveis.ACAB2.set("-")
        variaveis.ACAB3.set("-")
        variaveis.ACAB4.set("-")
        variaveis.OBSERVACAO.set("-")
        variaveis.GRAVACAO.set("-")
        PROX_CABO.set("-")
        PROX_DECAPEA.set("-")
        PROX_MEDIDA.set("-")
        PROX_DECAPEB.set("-")

        for ele in root.winfo_children():
            ele.destroy()

        self.montaTela()

    def populaLista(self):
        pd = PD()
        pd.buscarPD(configuracoes.maquina)

        self.data = pd.info

        cabos = []
        for item in self.data:
            if item[3] not in cabos:
                cabos.append(str(item[3]))

        for cabo in cabos:
                self.tvw.insert('', 'end', cabo, text=cabo)

        print (cabos)

        for item in self.data:
            self.tvw.insert(item[3], 'end', text=item[3], values=(item[6], item[11], item[1], item[2], item[0]))

        self.listaCount.configure(text='Total de PDs: ' + str(len(self.data)))

    def opera(self):
        global tempoInicio
        tempoInicio = int(time())
        global operando
        operando = True

        self.atualizaCronografo()

    def atualizaCronografo(self):
        if operando:
            tempoAtual = int(time() - tempoInicio)

            if tempoAtual % 1 == 0:
                QUANTIDADE_CORTADA.set(int(QUANTIDADE_CORTADA.get()) + 1)
                self.lblQuantidadeCortada.configure(text=QUANTIDADE_CORTADA.get())

            if QUANTIDADE_CORTADA.get() == QUANTIDADE.get():
                self.stop()

            self.relogio.configure(text=tempoAtual)
            root.after(1000, self.atualizaCronografo)

    def stop(self):
        pd = PD()

        global operando

        if (operando):
            operando = False

##        QUANTIDADE_CORTADA.set(QUANTIDADE.get())
        self.limpaTela()
        pd.atualizaQuantidadeCortada(ID.get(), QUANTIDADE_CORTADA.get())

    def teste(self):
        con = fdb.connect(
            dsn='192.168.1.100:/app/database/DADOS.FDB',
            user='sysdba',
            password='el0perdid0'
        )
        cur = con.cursor()
        cur.execute("Select * from Bitolas where PK_BIT = 50")


        print(cur.fetchone())
        pd = PD()
        pd.buscarPD("Samec")

        print(pd.CABO)

Application(root)
root.mainloop()
