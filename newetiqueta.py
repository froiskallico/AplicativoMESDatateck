from escpos.printer import Usb, Serial
import datetime
from collections import OrderedDict
import configparser as cfgprsr
import os
import logger

#ToDo: Tentar importar escpos.escpos para usar method textln() e ln() e outros.....

class etiqueta(object):

    def __init__(self):
        diretorio = os.path.dirname(os.path.abspath(__file__))
        configFile = cfgprsr.ConfigParser()

        configFile.read(diretorio + '/config.ini')
        self.printer_type = configFile['PRINTER']['tipo']
        self.printer_device = configFile['PRINTER']['dispositivo']
        self.printer_vid = configFile['PRINTER']['vid']
        self.printer_pid = configFile['PRINTER']['pid']
        self.printer_baudrate = configFile['PRINTER']['baudrate']
        self.printer_timeout = configFile['PRINTER']['timeout']
        self.printer_parity = configFile['PRINTER']['parity']

        self.openPort()
        self.testeImpressora()

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
        except Exception as e:
            logger.logError("Erro ao comunicar com a impressora.    -    Details: {}".format(str(e)))

    def closePort(self):
        self.printer.close()

    def imprimeEtiqueta(self, QTD_Cortada=None, nomeUsuario=None, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, str(value).strip().replace('None', '-'))

        self.printer.set(align='center')

        self.printer.barcode(code=self.pd,
                             bc='ITF',
                             height=64,
                             width=6,
                             pos='OFF')

        cabecalhopd = 'PD: {} | Maquina: {} | Req: {}\n'.format(self.PD,
                                                              self.MAQUINA,
                                                              self.REQUISICAO)
        
        self.printer.text(cabecalhopd)

        self.printer.set(align='left')
        self.printer.text('CPD: {} | Cabo: {}\n'.format(self.CPD, self.CABO))

        self.printer.text('Bitola: {} X {}\n'.format(self.VIAS,
                                                     self.BITOLA + self.UNIDADE))
        
        self.printer.set(align='center', bold=True)

        self.printer.text(str.encode('Medida: {} mm\n' % self.MEDIDA))

        # ToDo: Contiuar conversão do código a partir daqui...........
        self.port.write(bytearray.fromhex('1B 61 30 1B 44 16 17 18 19 20 21 22 23 00')) 
        
        self.port.write(str.encode('Decape A'))
        self.port.write(bytearray.fromhex('09 7C 09'))
        self.port.write(str.encode('Decape B'))
        self.port.write(bytearray.fromhex('0A'))
        
        self.port.write(str.encode(self.DECAPE_A))        
        self.port.write(bytearray.fromhex('09 7C 09'))
        self.port.write(str.encode(self.DECAPE_B))
        self.port.write(bytearray.fromhex('0A'))

        if self.PONTE_1 == "S":
            self.port.write(str.encode("* "))
        self.port.write(str.encode(self.ACABAMENTO_1))

        self.port.write(bytearray.fromhex('09 7C 09'))

        if self.PONTE_2 == "S":
            self.port.write(str.encode("* "))
        self.port.write(str.encode(self.ACABAMENTO_2))

        self.port.write(bytearray.fromhex('0A'))
        
        self.port.write(str.encode(self.ACABAMENTO_3))        
        self.port.write(bytearray.fromhex('09 7C 09'))
        self.port.write(str.encode(self.ACABAMENTO_4))
        self.port.write(bytearray.fromhex('0A'))
        
        self.port.write(bytearray.fromhex('1B 61 31'))
        self.port.write(str.encode('Quantidade: %s de %s pcs' % (QTD_Cortada, self.QTD_PD_REQ)))
        self.port.write(bytearray.fromhex('0A'))
        
        self.port.write(bytearray.fromhex('1B 46'))
        self.port.write(bytearray.fromhex('1B 61 30'))
        self.port.write(str.encode('Observacao: %s \n\n' % self.OBSERVACAO))
        self.port.write(str.encode('Gravacao: %s \n' % self.GRAVACAO))

        self.port.write(str.encode('Produto Final: %s \n' % self.CHICOTE))
        self.port.write(str.encode('Célula de Produção: %s \n' % self.CELULA))
        self.port.write(str.encode('Data de Entrega: %s \n' % self.DATA_ENTREGA))
        self.port.write(str.encode('Usuário: %s \n' % nomeUsuario))
        self.port.write(str.encode('Data de Impressao: %s \n' % datetime.datetime.now().strftime(
                '%d-%m-%Y  %H:%M:%S')))



        self.port.write(bytearray.fromhex('1B 69'))
 
        self.closePort()

    def testeImpressora(self):
        configs = OrderedDict([
                              ('printConfig', '1D F9 35 30'),
                              ('printerMode', '1D F9 2D 31'),
                              ('charAlignmt', '1B 61 31'),
                              ('encode', '1D F9 37 38')
                             ])

        for value in configs.values():
                self.port.write(bytearray.fromhex(value))

        
        stringTeste = '''Bem vindo ao MES - Datateck
Teste de impressão de etiqueta

A Vontade de Crescer nos Conecta

Powered by TRI
www.TRITEC.rf.gd'''

        self.port.write(str.encode(stringTeste))
            
        self.port.write(bytearray.fromhex('1B 69'))
        
        self.closePort()


etiqueta()
