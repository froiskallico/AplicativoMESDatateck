#--- Imports ---#
from PD import PD
from tkinter import *
from time import sleep, time
from PIL import Image, ImageTk
from tkinter import ttk
#import LOGIN
import threading
global operando
import configparser as cfgprsr

#--- Configurações ---#
config = cfgprsr.ConfigParser()
config.read('config.ini')

maquina = config['DEFAULT']['Maquina']


#--- Declarações ---#
operando = False


#--- Tela Principal ---#
root = Tk()
root.title('Operação')
root.geometry(config['DISPLAY']['RES'])
root.attributes('-fullscreen', config['DISPLAY']['Tela Cheia'])
root.bind('<Escape>',lambda e: root.destroy())
root.resizable(width=True, height=True)

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


#--- CORES ---#
bgCinza		= "#333333"
bgVerde		= "#00d455"
letraVerde	= "#66ff00"

#--- IMAGENS ---#
logo			= PhotoImage(file="src/images/logos/logo.png")
startButton		= PhotoImage(file="src/images/buttons/startButton.png")
stopButton		= PhotoImage(file="src/images/buttons/stopButton.png")
searchButton	= PhotoImage(file="src/images/buttons/searchButton.png")
pularButton		= PhotoImage(file="src/images/buttons/pularButton.png")
paradaButton	= PhotoImage(file="src/images/buttons/paradaButton.png")
menuButton		= PhotoImage(file="src/images/buttons/menuButton.png")


#--- Declaração de Classe ---#
class Application:
	
	def __init__(self, master=None):
		#Log = LOGIN.sts

		#if Log == True:
			self.montaTela()

	def montaTela(self, master=None):
		#--- Fonte Padrão ---#
		self.fonte = ("Play", 12)

		#--- Containers ---#
		##--- Cabecalho ----##
		self.containerCabecalho = Frame(master, bd=5, bg=bgCinza)
		self.containerCabecalho["padx"] = 5
		self.containerCabecalho.pack(fill=X, side=TOP)

		##--- Esquerda ---##
		self.containerEsquerda = Frame(master, bg=bgCinza)
		self.containerEsquerda.pack(side=LEFT, fill=BOTH, expand=1)
		
		###--- Dados PD ---###
		self.containerDadosPD = Frame(self.containerEsquerda, bg=bgCinza)
		self.containerDadosPD.pack(fill=BOTH, expand=1, padx=(0,20))

		####--- Cabecalho PD ---####
		self.containerCabecalhoPD = Frame(self.containerDadosPD, bg=bgCinza)
		self.containerCabecalhoPD.pack(fill=X, pady=(20,35), padx=20)	 

		####--- Medidas PD ---####
		self.containerMedidasPD = Frame(self.containerDadosPD, bg=bgCinza)
		self.containerMedidasPD.pack()

		####--- Cabo ---###
		self.containerCabo = Frame(self.containerDadosPD, bg=bgCinza)
		self.containerCabo.pack()

		####--- Detalhes PD ---####
		self.containerDetalhesPD = Frame(self.containerDadosPD, bg=bgCinza)
		self.containerDetalhesPD.pack(fill=X, expand=1)

		#####--- Acabamentos Lado A ---#####
		self.containerLadoA = Frame(self.containerDetalhesPD, bg=bgCinza)
		self.containerLadoA.pack(side=LEFT)
		
		######--- Acabamento 1 ---######
		self.containerAcabamento1 = Frame(self.containerLadoA, bg="#00d455")
		self.containerAcabamento1.pack(side=TOP, pady=10)

		######--- Acabamento 3 ---######
		self.containerAcabamento3 = Frame(self.containerLadoA, bg="#cccccc")
		self.containerAcabamento3.pack(side=TOP)

		#####--- Detalhes Meio ---#####
		self.containerDetalhesMeio = Frame(self.containerDetalhesPD, bg=bgCinza)
		self.containerDetalhesMeio.pack(side=LEFT, fill=X, expand=1)

		######--- Quantidade ---######
		self.containerQuantidade = Frame(self.containerDetalhesMeio, bg=bgCinza)
		self.containerQuantidade.pack(fill=BOTH, expand=1)	 

		######--- Observação ---######
		self.containerObservacao = Frame(self.containerDetalhesMeio, bg=bgCinza)
		self.containerObservacao.pack(fill=X, expand=1)

		######--- Gravação ---######
		self.containerGravacao = Frame(self.containerDetalhesMeio, bg=bgCinza)
		self.containerGravacao.pack(fill=X, expand=1)
		
		#####--- Acabamentos Lado B ---#####
		self.containerLadoB = Frame(self.containerDetalhesPD, bg=bgCinza)
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

		##--- Menu Botoes ---##
		self.containerBotoes = Frame(master, bg = bgCinza)
		self.containerBotoes["padx"] = 0
		self.containerBotoes["pady"] = 10
		self.containerBotoes.pack(side=RIGHT, fill=Y)
	
		#--- Labels ---#
		##------ Cabeçalho ------##
		self.logo = Label(self.containerCabecalho, text="Datateck", font=("Play", 18, "bold"), image=logo, bg=bgCinza, fg="white")
		self.logo.pack(side=LEFT)
		
		self.maquina = Label(self.containerCabecalho, text=maquina, bg=bgCinza, fg="white")
		self.maquina["font"] = ("Play", "18", "bold")
		self.maquina.pack(side=LEFT, fill=X, expand=1)

		self.relogio = Label(self.containerCabecalho, text="00:00:00", padx=10, fg=letraVerde, bg=bgCinza)
		self.relogio["font"] = ("Play", "18", "bold")
		self.relogio.pack(side=LEFT)

		##--- Dados PD ---##
		###--- Cabecalho PD ---###
		self.lblReq = Label(self.containerCabecalhoPD, text="Requisição: %s" % (REQNUM.get()), bg=bgCinza, fg="white", font=self.fonte, anchor="w")
		self.lblReq.pack(side=LEFT)

		self.lblPD = Label(self.containerCabecalhoPD, text="PD: %s" % PDNUM.get(), bg=bgCinza, fg=letraVerde, font=("Play", 16, "bold"), anchor="center")
		self.lblPD.pack(side=LEFT, fill=X, expand=1)

		self.lblReq = Label(self.containerCabecalhoPD, text="Produto Pai: %s" % PAI.get(), bg=bgCinza, fg="white", font=self.fonte, anchor="e")
		self.lblReq.pack(side=LEFT)

		###--- Medidas PD ---###
		self.lblDecapeA = Label(self.containerMedidasPD, text=DECAPEA.get(), bg=bgCinza, fg=letraVerde, font=("Play", 16, "bold"))
		self.lblDecapeA.grid(column=0, row=0)

		self.lblMedida = Label(self.containerMedidasPD, text=MEDIDA.get(), bg=bgCinza, fg=letraVerde, font=("Play", 16, "bold"), width=30)
		self.lblMedida.grid(column=1, row=0)

		self.lblDecapeB = Label(self.containerMedidasPD, text=DECAPEB.get(), bg=bgCinza, fg=letraVerde, font=("Play", 16, "bold"))
		self.lblDecapeB.grid(column=2, row=0)

		###--- Cabo ---###
		self.lblLadoACabo = Label(self.containerCabo, text="", bg="#ff9955", width=10, height=1)
		self.lblLadoACabo.grid(column=0, row=0)

		self.lblCabo = Label(self.containerCabo, text=CABO.get(), bg="white", fg=bgCinza, font=self.fonte, width=40, height=2)
		self.lblCabo.grid(column=1, row=0)

		self.lblLadoBCabo = Label(self.containerCabo, text="", bg="#ff9955", width=10, height=1)
		self.lblLadoBCabo.grid(column=2, row=0)

		###--- Detalhes ---###

		####--- Lado A ---####
		#####--- Acabamento 1 ---#####
		self.lblLabelAcabamento1 = Label(self.containerAcabamento1, text="Acabamento 1", bg="#00d455", fg=bgCinza, font=self.fonte, width=20)
		self.lblLabelAcabamento1.pack(fill=BOTH, expand=1, pady=5)
		
		self.lblAcabamento1 = Label(self.containerAcabamento1, text=ACAB1.get(), bg="#00d455", fg=bgCinza, font=self.fonte)
		self.lblAcabamento1.pack(fill=BOTH, expand=1, pady=5)

		#####--- Acabamento 3 ---#####
		self.lblLabelAcabamento3 = Label(self.containerAcabamento3, text="Acabamento 3", bg="#ccc", fg=bgCinza, font=self.fonte, width=20)
		self.lblLabelAcabamento3.pack(fill=BOTH, expand=1, pady=5)
		
		self.lblAcabamento3 = Label(self.containerAcabamento3, text=ACAB3.get(), bg="#ccc", fg=bgCinza, font=self.fonte)
		self.lblAcabamento3.pack(fill=BOTH, expand=1, pady=5)
	
		####--- Quantidade ---####
		self.lblLabelQuantidade = Label(self.containerQuantidade, text="Quantidade", font=("Play", 18, "bold"), bg=bgCinza, fg=letraVerde)
		self.lblLabelQuantidade.pack()

		self.lblQuantidade = Label(self.containerQuantidade, text=QUANTIDADE.get(), font=("Play", 32, "bold"), bg=bgCinza, fg=letraVerde, anchor="ne")
		self.lblQuantidade.pack()

		self.lblQuantidadeCortada = Label(self.containerQuantidade, text=QUANTIDADE_CORTADA.get(), font=("Play", 16, "bold"), bg=bgCinza, fg="red", anchor="sw")
		#self.lblQuantidadeCortada.bind("<Button-1>", self.clicked)
		self.lblQuantidadeCortada.pack()
	   
		
		####--- Observacao ---####
		self.lblLabelObservacao = Label(self.containerObservacao, text="Observação", font=self.fonte, bg=bgCinza, fg="#999")
		self.lblLabelObservacao.pack()

		self.lblObservacao = Label(self.containerObservacao, text=OBSERVACAO.get(), font=self.fonte, bg=bgCinza, fg="white")
		self.lblObservacao.pack()
		
		####--- Gravacao ---####
		self.lblLabelGravacao = Label(self.containerObservacao, text="Gravação", font=self.fonte, bg=bgCinza, fg="#999")
		self.lblLabelGravacao.pack()

		self.lblGravacao = Label(self.containerObservacao, text=GRAVACAO.get(), font=self.fonte, bg=bgCinza, fg="white")
		self.lblGravacao.pack()
		
		####--- Labo B ---####
		#####--- Acabamento 2 ---#####
		self.lblLabelAcabamento2 = Label(self.containerAcabamento2, text="Acabamento 2", bg="#00d455", fg=bgCinza, font=self.fonte, width=20)
		self.lblLabelAcabamento2.pack(fill=BOTH, expand=1, pady=5)
		
		self.lblAcabamento2 = Label(self.containerAcabamento2, text=ACAB2.get(), bg="#00d455", fg=bgCinza, font=self.fonte)
		self.lblAcabamento2.pack(fill=BOTH, expand=1, pady=5)
		
		#####--- Acabamento 4 ---#####
		self.lblLabelAcabamento4 = Label(self.containerAcabamento4, text="Acabamento 4", bg="#ccc", fg=bgCinza, font=self.fonte, width=20)
		self.lblLabelAcabamento4.pack(fill=BOTH, expand=1, pady=5)
		
		self.lblAcabamento4 = Label(self.containerAcabamento4, text=ACAB4.get(), bg="#ccc", fg=bgCinza, font=self.fonte)
		self.lblAcabamento4.pack(fill=BOTH, expand=1, pady=5)

		#--- Botões ---#						
		self.btnStart = Button(self.containerBotoes, image=startButton, bg=bgCinza, relief=FLAT, anchor="w", command=self.opera, bd=0,	highlightthickness=0)
		self.btnStart["width"] = 130
		self.btnStart["height"] = 50
		self.btnStart.pack(pady=5)
		
		self.btnStop = Button(self.containerBotoes, image=stopButton, bg=bgCinza, relief=FLAT, anchor="w", command=self.stop, bd=0,	 highlightthickness=0)
		self.btnStop["width"] = 130
		self.btnStop["height"] = 50
		self.btnStop.pack(pady=5)

		self.btnBusca = Button(self.containerBotoes, image=searchButton, bg=bgCinza, anchor="w", command=self.exibeLista, bd=0, highlightthickness=0) 
		self.btnBusca["width"] = 130
		self.btnBusca["height"] = 50
		self.btnBusca.pack(pady=5)

		self.btnPula = Button(self.containerBotoes, image=pularButton, bg=bgCinza, relief=FLAT, anchor="w", bd=0,  highlightthickness=0)
		self.btnPula["width"] = 130
		self.btnPula["height"] = 50
		self.btnPula.pack(pady=5)

		self.btnParada = Button(self.containerBotoes, image=paradaButton, bg=bgCinza, relief=FLAT, anchor="w", bd=0,  highlightthickness=0)
		self.btnParada["width"] = 130
		self.btnParada["height"] = 50
		self.btnParada.pack(pady=5)

		self.btnMenu = Button(self.containerBotoes, image=menuButton, bg=bgCinza, relief=FLAT, anchor="w", bd=0,  highlightthickness=0)
		self.btnMenu["width"] = 130
		self.btnMenu["height"] = 50
		self.btnMenu.pack(pady=5)		 
		
		#--- Rodape ---#
		self.lblProxCabo = Label(self.containerProxCabo, text=PROX_CABO.get(), bg="#454545", fg="#888")
		self.lblProxCabo.pack(side=TOP, fill=X, expand=1)

		self.lblLabelProxDecapeA = Label(self.containerProxMedidas, text="Decape A", bg="#454545", fg="#888")
		self.lblLabelProxDecapeA.grid(column=0, row=0)
		
		self.lblLabelProxMedida = Label(self.containerProxMedidas, text="Medida", bg="#454545", fg="#888", width=30)
		self.lblLabelProxMedida.grid(column=1, row=0)
		
		self.lblLabelProxDecapeB = Label(self.containerProxMedidas, text="Decape B", bg="#454545", fg="#888")
		self.lblLabelProxDecapeB.grid(column=2, row=0)
		
		self.lblProxDecapeA = Label(self.containerProxMedidas, text=PROX_DECAPEA.get(), bg="#454545", fg="#888")
		self.lblProxDecapeA.grid(column=0, row=1)
		
		self.lblProxMedida = Label(self.containerProxMedidas, text=PROX_MEDIDA.get(), bg="#454545", fg="#888")
		self.lblProxMedida.grid(column=1, row=1)
		
		self.lblProxDecapeB = Label(self.containerProxMedidas, text=PROX_DECAPEB.get(), bg="#454545", fg="#888")
		self.lblProxDecapeB.grid(column=2, row=1)
	


	def limpaTela(self):
		for ele in root.winfo_children():
			ele.destroy()

		Application()


	def exibeLista(self):		   
		for ele in self.containerEsquerda.winfo_children():
			ele.destroy()
			
		style = ttk.Style()
		style.configure("TTvw", foreground="black", font=("Play", 16), highlightthickness=0, rowheight=30)
		style.layout("TTvw", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) 
				
		self.tvw = ttk.Treeview(self.containerEsquerda, style="TTvw")
		self.oferta = self.tvw.insert('', 'end', 'ofertas', text='Ofertas do dia')
		self.idMono = self.tvw.insert('ofertas', 'end', text='Monociclos')
		self.idDici = self.tvw.insert('ofertas', 'end', text='Diciclos')
		self.idPati = self.tvw.insert('ofertas', 'end', text='Patinetes')
		self.idBici = self.tvw.insert('ofertas', 'end', text='Bicicletas')

		self.idMonoMarca1 = self.tvw.insert(self.idMono, 'end', text='Marca1')
		self.idMonoMarca2 = self.tvw.insert(self.idMono, 'end', text='Marca2')
		self.idMonoMarca3 = self.tvw.insert(self.idMono, 'end', text='Marca3')

		self.idDiciMarca1 = self.tvw.insert(self.idDici, 'end', text='Marca11')
		self.idDiciMarca2 = self.tvw.insert(self.idDici, 'end', text='Marca21')
		self.idDiciMarca3 = self.tvw.insert(self.idDici, 'end', text='Marca31')

		self.idPatiMarca1 = self.tvw.insert(self.idPati, 'end', text='Marca12')
		self.idPatiMarca2 = self.tvw.insert(self.idPati, 'end', text='Marca22')
		self.idPatiMarca3 = self.tvw.insert(self.idPati, 'end', text='Marca32')

		self.idBiciMarca1 = self.tvw.insert(self.idBici, 'end', text='Marca12')
		self.idBiciMarca2 = self.tvw.insert(self.idBici, 'end', text='Marca22')
		self.idBiciMarca3 = self.tvw.insert(self.idBici, 'end', text='Marca32')		
		self.tvw.pack(fill=BOTH, pady=15, padx=15, expand=1)

		self.btnConfirma = Button(self.containerEsquerda, text="Carregar", font=("Play", 16), bg=bgCinza, fg="white")
		self.btnConfirma.pack(pady=10)
		
	def busca(self):
		pd = PD()
		pd.buscarPD(maquina)
		
		#tempos = TEMPOS()		  

		ID.set(pd.ID)
		REQNUM.set(pd.REQNUM)
		PDNUM.set(pd.PD)
		PAI.set(pd.PAI)
		DECAPEA.set(pd.DECAPEA)
		DECAPEB.set(pd.DECAPEB)
		MEDIDA.set(pd.MEDIDA)
		CABO.set(pd.CABO)
		QUANTIDADE.set(pd.QTD)
		QUANTIDADE_CORTADA.set(pd.QTD_CORT)
		ACAB1.set(pd.ACAB1)
		ACAB2.set(pd.ACAB2)
		ACAB3.set("-")
		ACAB4.set("-")
		OBSERVACAO.set(pd.OBS)
		GRAVACAO.set("-")
		PROX_CABO.set("-")
		PROX_DECAPEA.set("-")
		PROX_MEDIDA.set("-")
		PROX_DECAPEB.set("-")

		self.limpaTela()
		
##		  global qtdCortada
##		  global buscado
##
##		  qtdCortada = int(pd.QTD_CORT)
##		  buscado = True
##
##		  global setupTempoInicio
##
##		  setupTempoInicio = time()
###		   self.atualizaSetup()
##
##	  def atualizaSetup(self):
##		  tempos = TEMPOS()
##		  tempoAtualSetup = int(time() - setupTempoInicio)
##		  tempos.setup(tempoAtualSetup)
##		  if not operando:
##			  root.after(1000, self.atualizaSetup)
##						 
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

##		  QUANTIDADE_CORTADA.set(QUANTIDADE.get())
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
