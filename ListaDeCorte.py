#--- Imports ---#

from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import functools as partial

vKBVisible = False

#--- Tela Principal ---#
new = Tk()
new.title('Login')
new.geometry("1024x600+0+0")
new.attributes('-fullscreen', True)
new.bind('<Escape>',lambda e: new.destroy())
new.resizable(width=False, height=False)

#--- CORES ---#
bgCinza     = "#333333"
bgVerde     = "#00d455"
letraVerde  = "#66ff00"

#--- IMAGENS ---#
logo            = PhotoImage(file="logoL.png")
startButton     = PhotoImage(file="startButton.png")
stopButton      = PhotoImage(file="stopButton.png")
searchButton    = PhotoImage(file="searchButton.png")
pularButton     = PhotoImage(file="pularButton.png")
paradaButton    = PhotoImage(file="paradaButton.png")
menuButton      = PhotoImage(file="menuButton.png")


class Application:
    def __import__(self, master=None):
        self.app()
    
    def __init__ (self, master=None):
        self.app()
    
    def app(self, master=None):
        self.maquina = "CLN-06"
        
        #--- Fonte Padrão ---#
        self.fonte = ("Play", 12)

        #--- Containers ---#
        ##--- Cabecalho ----##
        self.containerCabecalho = Frame(master, bg=bgCinza)
        self.containerCabecalho["pady"] = 5
        self.containerCabecalho.pack(fill=X, side=TOP)

        ##--- Esquerda ---##
        self.containerEsquerda = Frame(master, bg=bgCinza)
        self.containerEsquerda["pady"] = 15
        self.containerEsquerda.pack(fill=BOTH, side=LEFT, expand=1)

        ##--- Direita ---##
        self.containerBotoes = Frame(master, bg=bgCinza)
        self.containerBotoes["pady"] = 15
        self.containerBotoes.pack(fill=Y, side=RIGHT, expand=0)

        #--- Labels ---#
        ##------ Cabeçalho ------##
        self.logoLabel = Label(self.containerCabecalho, text="Datateck", font=("Play", 18, "bold"), image=logo, bg=bgCinza, fg="white")
        self.logoLabel.pack(side=LEFT)

        self.labelListaDeCorte = Label(self.containerCabecalho, text="LISTA DE CORTE", font=("Play", 24), bg=bgCinza, fg="white")
        self.labelListaDeCorte.pack(side=TOP, fill=X, pady=20)

        self.labelMaquina = Label(self.containerCabecalho, text="Máquina: " + self.maquina, font=("Play", 18), bg=bgCinza, fg="white")
        self.labelMaquina.pack(side=TOP, fill=X, pady=5)

        #--- ListBox ---#
        self.lbPDs = Listbox(self.containerEsquerda, font=("Play", 16), height=80, bg="seashell3", fg="black")
        self.lbPDs.pack()

        self.lbPDs.insert(1, "A")
        self.lbPDs.insert(2, "B")
        self.lbPDs.insert(3, "C")
        self.lbPDs.insert(4, "D")
        
        #--- Botões ---#                         
        self.btnStart = Button(self.containerBotoes, image=startButton, bg=bgCinza, relief=FLAT, anchor="w")
        self.btnStart["width"] = 130
        self.btnStart["height"] = 50
        self.btnStart.pack(pady=5)
        
        self.btnStop = Button(self.containerBotoes, image=stopButton, bg=bgCinza, relief=FLAT, anchor="w")
        self.btnStop["width"] = 130
        self.btnStop["height"] = 50
        self.btnStop.pack(pady=5)

        self.btnBusca = Button(self.containerBotoes, image=searchButton, bg=bgCinza, relief=FLAT, anchor="w")
        self.btnBusca["width"] = 130
        self.btnBusca["height"] = 50
        self.btnBusca.pack(pady=5)

        self.btnPula = Button(self.containerBotoes, image=pularButton, bg=bgCinza, relief=FLAT, anchor="w")
        self.btnPula["width"] = 130
        self.btnPula["height"] = 50
        self.btnPula.pack(pady=5)

        self.btnParada = Button(self.containerBotoes, image=paradaButton, bg=bgCinza, relief=FLAT, anchor="w")
        self.btnParada["width"] = 130
        self.btnParada["height"] = 50
        self.btnParada.pack(pady=5)

        self.btnMenu = Button(self.containerBotoes, image=menuButton, bg=bgCinza, relief=FLAT, anchor="w")
        self.btnMenu["width"] = 130
        self.btnMenu["height"] = 50
        self.btnMenu.pack(pady=5)  


    def vKBUser(self, master):
        self.user.delete(0, END)
        self.vKB(self, self.user) 
    
    def vKBPass(self, master):
        self.password.delete(0, END)
        self.vKB(self, self.password)

    def vKB(self, master, parent):
        global vKBVisible

        if vKBVisible:
            global kbFrame
            self.kbFrame.destroy()
            vKBVisible = False
            self.vKB(self, parent)
            
        else:
            vKBVisible = True

            self.containerCabecalho.pack_forget()
        
            self.kbFrame = Frame(new, bg=bgCinza)
            self.kbFrame.pack(side=BOTTOM, fill=BOTH, expand=1)
            
            self.btn_list = [
                ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ç'],
                ['Z', 'X', 'C', 'V', 'B', 'N', 'M']]

            self.kbRowFrame = list(range(len(self.btn_list)))
            
            for r in self.kbRowFrame:
                self.kbRowFrame[r] = Frame(self.kbFrame)
                self.kbRowFrame[r].pack(side=TOP)

                self.kbKey = list(range(len(self.btn_list[r])))

                for k in self.kbKey:
                    cmd = lambda x = self.btn_list[r][k]: self.kp(self, x, parent)
                    
                    self.kbKey[k] = Button(self.kbRowFrame[r], text=self.btn_list[r][k], width=5, height=3, bg="black", fg="white", font=("Play", 12, "bold"))
                    self.kbKey[k]['command'] = cmd
                    self.kbKey[k].pack(side=LEFT)
                    

    def kp(self, master, keyValue, parent):
        parent.insert(END, keyValue)
    
        
        
    ##    btn = list(range(len(btn_list)))

    ##    for r in btn_list:
    ##        
    ##    for label in btn_list:
    ##        #cmd = partial(click, label)
    ##        btn[n] = Button(kbFrame, text=label, width=5, height=3)
    ##        btn[n].pack(side=LEFT)
    ##        n += 1
    ##        c += 1
    ##        if c == 10:
    ##            c = 0
    ##            r += 1
        
    def btn(self):
        global sts
        usr = self.user.get()
        pwd = self.password.get()

        if usr == "K" and pwd == "F":
            print ("Fazendo Login como: " + usr)
            new.destroy()
            sts = not sts
            return sts
        
        
    



Application(new)            
new.mainloop()                                
