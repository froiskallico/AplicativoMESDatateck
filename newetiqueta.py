from escpos.printer import Usb, Serial,Dummy
import datetime
import configparser as cfgprsr
import os
import logger

class etiqueta(object):

    def __init__(self):
        debugMode = False

        diretorio = os.path.dirname(os.path.abspath(__file__))
        configFile = cfgprsr.ConfigParser()

        configFile.read(diretorio + '/config.ini')
        self.printer_type = configFile['PRINTER']['tipo']
        self.printer_device = configFile['PRINTER']['dispositivo']
        self.printer_vid = int(configFile['PRINTER']['vid'], 16)
        self.printer_pid = int(configFile['PRINTER']['pid'], 16)
        self.printer_baudrate = int(configFile['PRINTER']['baudrate'])
        self.printer_timeout = int(configFile['PRINTER']['timeout'])
        self.printer_parity = configFile['PRINTER']['parity']

        if debugMode:
            self.openDummy()
        else:
            self.openPort()

        # self.testeImpressora()

    def openPort(self):
        try:
            if self.printer_type.lower() == 'serial':
                self.printer = Serial(devfile=self.printer_device,
                                  baudrate=int(self.printer_baudrate),
                                  timeout=int(self.printer_timeout),
                                  parity=self.printer_parity)
            elif self.printer_type.lower() == 'usb':
                self.printer = Usb(idVendor=self.printer_vid,
                                   idProduct=self.printer_pid,
                                   timeout=self.printer_timeout)

            self.printer.codepage = 'UTF8'
        except Exception as e:
            logger.logError("Erro ao comunicar com a impressora.    -    Details: {}".format(str(e)))

    def openDummy(self):
        self.printer = Dummy()

    def closePort(self):
        self.printer.close()

    def imprimeEtiqueta(self, QTD_Cortada=None, nomeUsuario=None, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, str(value).strip().replace('None', '-'))

        self.printer.set(align='center', font='b')

        self.printer.barcode(code=self.PD,
                             bc='ITF',
                             height=64,
                             width=6,
                             pos='OFF')

        cabecalhopd = 'PD: {} | Maquina: {} | Req: {}\n'.format(self.PD,
                                                              self.MAQUINA,
                                                              self.REQUISICAO)
        
        self.printer.text(cabecalhopd)

        self.printer.set(align='left', font='a')
        self.printer.text('CPD: {} | Cabo: {}\n'.format(self.CPD, self.CABO))

        self.printer.text('Bitola: {} X {}\n\n'.format(self.VIAS,
                                                     self.BITOLA + self.UNIDADE))
        
        self.printer.set(align='center', text_type='b', width=2, height=2)

        self.printer.text('Medida: {} mm\n'.format(self.MEDIDA))

        self.printer.set(align='left', text_type='b', width=1, height=1, font='b')

        self.printer.text('{} | {}\n'.format('Decape A'[:31].ljust(30, ' '),
                                           'Decape B'[:31].ljust(30, ' ')))

        self.printer.text('{} | {}\n'.format(self.DECAPE_A[:31].ljust(30, ' '),
                                           self.DECAPE_B[:31].ljust(30, ' ')))

        self.printer.text('{} | {}\n'.format(self.ACABAMENTO_1[:31].ljust(30, ' '),
                                           self.ACABAMENTO_2[:31].ljust(30, ' ')))

        self.printer.text('{} | {}\n'.format(self.ACABAMENTO_3[:31].ljust(30, ' '),
                                           self.ACABAMENTO_4[:31].ljust(30, ' ')))

        self.printer.set(align='center', text_type='b', width=2, height=1, font='a')

        self.printer.text('Qtd: {} de {} pcs\n'.format(QTD_Cortada, self.QTD_PD_REQ))

        self.printer.set(align='left', text_type='normal', width=1, height=1)

        self.printer.text('\nObservacao: {}\n'.format(self.OBSERVACAO))

        self.printer.text('Gravacao: {}\n'.format(self.GRAVACAO))

        self.printer.set(font='b')

        self.printer.text('Produto Final: {}\n'.format(self.CHICOTE))
        self.printer.text('Célula de Produção: {}\n'.format(self.CELULA))
        self.printer.text('Data de Entrega: {}\n'.format(self.DATA_ENTREGA))
        self.printer.text('Usuário: {}\n'.format(nomeUsuario))
        self.printer.text('Data de Impressao: {}\n'.format(datetime.datetime.now().strftime('%d-%m-%Y  %H:%M:%S')))

        self.printer.cut()

        self.printer.close()

    def testeImpressora(self):
        self.printer.set(align='center')

        stringTeste = '''Bem vindo ao MES - Datateck
Teste de impressão de etiqueta

A Vontade de Crescer nos Conecta

Powered by TRI
www.TRITEC.rf.gd'''

        self.printer.text(stringTeste)

        self.printer.close()

etq = etiqueta()
etq.imprimeEtiqueta(3,
                           'K',
                           PD='46338',
                           MAQUINA='KOMAX ALPHA 530',
                           REQUISICAO='115915',
                           CPD='8054',
                           BITOLA='0.5',
                           UNIDADE='MM2',
                           CABO='COND C.F 0,50 VD/AM 300V',
                           VIAS='1',
                           MEDIDA='6080',
                           DECAPE_A='5',
                           DECAPE_B='',
                           ACABAMENTO_1='201.3456-01',
                           ACABAMENTO_2='626437-1 (ET-25)',
                           ACABAMENTO_3='-',
                           ACABAMENTO_4='-',
                           QTD_PD_REQ='10',
                           OBSERVACAO='',
                           GRAVACAO='-',
                           CHICOTE='3X.0564.GB.8',
                           CELULA='KITS DIÁRIA',
                           DATA_ENTREGA='2019-09-11 00:00:00'
                           )

