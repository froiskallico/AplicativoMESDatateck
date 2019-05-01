#--- Imports ---#
from tkinter import *
from banco import BANCO
import configparser as cfgprsr

class Definicoes():
    configFile = cfgprsr.ConfigParser()
    configFile.read('config.ini')


root = Tk()
root.title('Login')
root.geometry(Definicoes.configFile['DISPLAY']['RES'])
root.attributes('-fullscreen', Definicoes.configFile['DISPLAY']['Tela Cheia'])
root.bind('<Escape>', lambda e: root.destroy())
root.resizable(width=True, height=True)


vKBVisible = False
global idUsuario
idUsuario = 0


class Fontes():
    fontePadrao = ("Play", 12)
    fontePadraoBold = ("Play", 12, "bold")
    fonteCabecalho = ("Play", 18, "bold")


class Cores():
    bgCinza     = "#333333"
    bgVerde     = "#00d455"
    letraVerde  = "#66ff00"


class Imagens():
    logo            = PhotoImage(
        file="src/images/logos/logoL.png")
    loginIcon       = PhotoImage(
        file="src/images/icons/loginIcon.png")
    loginButton     = PhotoImage(
        file="src/images/buttons/loginButton.png")


class Application:

    def __init__(self, master=None):
        self.montaTelaLogin()
        
    def montaTelaLogin(self):
        self.montaContainers()
        self.montaLabels()
        self.montaBotoes()

    def montaContainers(self, master=None):
        #--- Containers ---#
        ##--- Cabecalho ----##
        self.containerCabecalhoLogin = Frame(master,
                                             bg=Cores.bgCinza)
        self.containerCabecalhoLogin["pady"] = 5
        self.containerCabecalhoLogin.pack(fill=X,
                                          side=TOP)

        ##--- Meio ---##
        self.containerMeioLogin = Frame(master,
                                        bg=Cores.bgCinza)
        self.containerMeioLogin["pady"] = 15
        self.containerMeioLogin.pack(fill=BOTH,
                                     side=TOP,
                                     expand=1)

    def montaLabels(self):
        #--- Labels ---#
        ##------ Cabeçalho ------##
        self.logoLabel = Label(self.containerCabecalhoLogin,
                               text="Datateck",
                               font=Fontes.fonteCabecalho,
                               image=Imagens.logo,
                               bg=Cores.bgCinza,
                               fg="white")
        self.logoLabel.pack(side=TOP)

        self.Icon = Label(self.containerMeioLogin,
                          text="Faça seu Login",
                          font=Fontes.fonteCabecalho,
                          image=Imagens.loginIcon,
                          bg=Cores.bgCinza,
                          fg="white")
        self.Icon.pack(side=TOP,
                       fill=X,
                       pady=10)

        #--- Campos ---#
        self.user = Entry(self.containerMeioLogin,
                          font=Fontes.fontePadrao,
                          width=15,
                          justify="center")
        self.user.pack(side=TOP,
                       pady=5)
        self.user.bind("<Button-1>", self.vKBUser)
        self.user.insert(0, "Usuário")
                
        self.password = Entry(self.containerMeioLogin,
                              font=Fontes.fontePadrao,
                              width=15,
                              justify="center",
                              show="*")
        self.password.pack(side=TOP,
                           pady=5)
        self.password.bind("<Button-1>", self.vKBPass)
        self.password.insert(0, "Senha")

        # --- Mensagem ---#
        self.lblMensagem = Label(self.containerMeioLogin,
                                 text='',
                                 font=Fontes.fontePadrao,
                                 bg=Cores.bgCinza,
                                 fg='yellow',
                                 justify="center")
        self.lblMensagem.pack(side=TOP,
                              pady=15)

    def montaBotoes(self):
        #--- Botão ---#                        
        self.btnLogin = Button(self.containerMeioLogin,
                               image=Imagens.loginButton,
                               bg=Cores.bgCinza,
                               relief=FLAT,
                               anchor="w",
                               command=self.botaoLogin)
        self.btnLogin["width"] = 130
        self.btnLogin["height"] = 50
        self.btnLogin.pack(side=TOP)

    def vKBUser(self, master=None):
        self.user.delete(0, END)

        self.lblMensagem["text"] = ''

        self.vKB(self, self.user) 
    
    def vKBPass(self, master=None):
        self.password.delete(0, END)

        self.lblMensagem["text"] = ''

        self.vKB(self, self.password)

    def vKB(self, master, parent):
        global vKBVisible

        if vKBVisible:
            self.containerTeclado.destroy()
            vKBVisible = False
            self.vKB(self, parent)
            
        else:
            vKBVisible = True

            self.containerCabecalhoLogin.pack_forget()
        
            self.containerTeclado = Frame(root,
                                          bg=Cores.bgCinza)
            self.containerTeclado.pack(side=BOTTOM,
                                       fill=BOTH,
                                       expand=1)
            
            self.listaDeTeclas = [
                ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
                ['Z', 'X', 'C', 'V', 'B', 'N', 'M']]

            self.containerTecladoLinha = list(range(len(self.listaDeTeclas)))
            
            for linha in self.containerTecladoLinha:
                self.containerTecladoLinha[linha] = Frame(self.containerTeclado)
                self.containerTecladoLinha[linha].pack(side=TOP)

                self.Teclas = list(range(len(self.listaDeTeclas[linha])))

                for tecla in self.Teclas:
                    cmd = lambda x = self.listaDeTeclas[linha][tecla]: self.kp(self,
                                                                       x,
                                                                       parent)
                    
                    self.Teclas[tecla] = Button(self.containerTecladoLinha[linha],
                                                text=self.listaDeTeclas[linha][tecla],
                                                width=5,
                                                height=3,
                                                relief=FLAT,
                                                bg='black',
                                                fg='white',
                                                font=Fontes.fontePadraoBold)
                    self.Teclas[tecla]['command'] = cmd
                    self.Teclas[tecla].pack(side=LEFT,
                                            padx=1,
                                            pady=1)

    def kp(self, master, keyValue, parent):
        parent.insert(END, keyValue)

    def botaoLogin(self):
        global idUsuario

        banco = BANCO()
        cur = banco.conexao.cursor()

        usr = self.user.get()
        pwd = self.password.get()
        pwdbco = None

        try:
            cur.execute(""" SELECT
                                    PK_USU,
                                    SENHA
                                FROM
                                    USUARIOS
                                WHERE
                                    NOME = "%s"
                            """ % usr)

            dados = cur.fetchone()
            idUsuario = dados[0]
            pwdbco = dados[1]

            if pwdbco == pwd:
                self.lblMensagem["text"] = "Login OK"

                root.destroy()

                return idUsuario

            else:
                self.lblMensagem["text"] = "Senha incorreta"

        except:
            self.lblMensagem["text"] = "Usuário não encontrado"


Application(root)
root.mainloop()