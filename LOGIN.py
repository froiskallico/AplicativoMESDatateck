#--- Imports ---#

from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import functools as partial

vKBVisible = False

#--- Tela Principal ---#
root = Tk()
root.title('Login')
root.geometry("1024x600+0+0")
root.attributes('-fullscreen', True)
root.bind('<Escape>',lambda e: root.destroy())
root.resizable(width=False, height=False)

#--- CORES ---#
bgCinza     = "#333333"
bgVerde     = "#00d455"
letraVerde  = "#66ff00"

#--- IMAGENS ---#
logo            = PhotoImage(file="logoL.png")
loginIcon       = PhotoImage(file="loginIcon.png")
loginButton     = PhotoImage(file="loginButton.png")

sts = False

class Application:

    def __init__(self, master=None):
        self.app()
        
    def app(self, master=None):
        #--- Fonte Padrão ---#
        self.fonte = ("Play", 12)

        #--- Containers ---#
        ##--- Cabecalho ----##
        self.containerCabecalho = Frame(master, bg=bgCinza)
        self.containerCabecalho["pady"] = 5
        self.containerCabecalho.pack(fill=X, side=TOP)

        ##--- Meio ---##
        self.containerMeio = Frame(master, bg=bgCinza)
        self.containerMeio["pady"] = 15
        self.containerMeio.pack(fill=BOTH, side=TOP, expand=1)

        #--- Labels ---#
        ##------ Cabeçalho ------##
        self.logoLabel = Label(self.containerCabecalho, text="Datateck", font=("Play", 18, "bold"), image=logo, bg=bgCinza, fg="white")
        self.logoLabel.pack(side=TOP)

        self.Icon = Label(self.containerMeio, text="Faça seu Login", font=("Play", 18), image=loginIcon, bg=bgCinza, fg="white")
        self.Icon.pack(side=TOP, fill=X, pady=10)

        #--- Campos ---#
        self.user = Entry(self.containerMeio, font=("Play", 12), width=15, justify="center")
        self.user.pack(side=TOP, pady=5)
        self.user.insert(0, "Usuário")
        self.user.bind("<Button-1>", self.vKBUser)
                
        self.password = Entry(self.containerMeio, font=("Play", 12), width=15, justify="center", show="*")
        self.password.pack(side=TOP, pady=5)
        self.password.insert(0, "Senha")
        self.password.bind("<Button-1>", self.vKBPass)
        
        #--- Botão ---#                        
        self.btnLogin = Button(self.containerMeio, image=loginButton, bg=bgCinza, relief=FLAT, anchor="w", command=self.btn)
        self.btnLogin["width"] = 130
        self.btnLogin["height"] = 50
        self.btnLogin.pack(side=TOP)


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
        
            self.kbFrame = Frame(root, bg=bgCinza)
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
            root.destroy()
            sts = not sts
            return sts
        
        
    



Application(root)            
root.mainloop()                                
