from tkinter import *

class Application:

    def __init__(self):
        self.montaScreen()

        def montaScreen(self):
            self.popUpParada = Toplevel(bg=Cores.bgCinza,
                                        bd=7,
                                        relief=RAISED)
            self.popUpParada.overrideredirect(1)
            self.popUpParada.attributes('-topmost', 'true')
            self.popUpParada.bind('<Escape>',
                                  lambda e: cancelaParada())
            self.popUpParada.geometry(Definicoes.configFile['DISPLAY']['RES'])
            self.popUpParada.focus()

            self.frameTitulo = Frame(self.popUpParada,
                                     bg=Cores.bgCinza)
            self.frameTitulo.pack(side=TOP,
                                  pady=(20, 5))

            self.frameLista = Frame(self.popUpParada,
                                    bg=Cores.bgCinza)
            self.frameLista.pack(side=TOP,
                                 fill=BOTH,
                                 expand=1,
                                 pady=(5, 20),
                                 padx=20)

            self.frameButtons = Frame(self.popUpParada,
                                      bg=Cores.bgCinza)
            self.frameButtons.pack(side=BOTTOM,
                                   pady=(30, 25))

        def montaWidgets(self):
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

            self.listaParadas = Listbox(self.frameLista,
                                        bg=Cores.bgAcabamentosAux,
                                        fg='black',
                                        font=('Play', 18))

            self.vsb = Scrollbar(self.frameLista,
                                 orient="vertical",
                                 width=80)
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
                                pady=(20, 10),
                                fill=BOTH,
                                expand=1)

            self.listaParadas.pack(side=LEFT,
                                   fill=BOTH,
                                   expand=1,
                                   padx=(15, 0))

            self.vsb.pack(side=LEFT,
                          padx=(0, 15),
                          fill=Y)

            self.lblMensagem.pack(side=TOP,
                                  fill=X,
                                  expand=1)

            self.btnConfirma.pack(side=LEFT)

            self.btnCancela.pack(side=LEFT)

            carregaLista()
