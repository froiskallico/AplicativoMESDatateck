import serial
import datetime
from collections import OrderedDict

class etiqueta(object):

    def __init__(self):
        self.openPort()

    def openPort(self):
        self.port = serial.Serial(
            "/dev/ttyACM0",
            baudrate=115200,
            parity=serial.PARITY_NONE,
            writeTimeout=3,
            timeout=3)

        # print(self.port.isOpen())
        # print("Porta de impressao aberta...")

    def closePort(self):
        while True:
            #print("inside while")
            response = self.port.read(8)
            # print(response)
            #print("Data Received")
            break
        
        self.port.close()

    def imprimeEtiqueta(self, QTD_Cortada=None, nomeUsuario=None, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, str(value).strip().replace('None', '-'))

        configs = OrderedDict([
                              ('printConfig', '1D F9 35 30'),
                              ('printerMode', '1D F9 2D 31'),
                              ('charAlignmt', '1B 61 31'),
                              ('encode', '1D F9 37 38')
                             ])

        for value in configs.values():
                self.port.write(bytearray.fromhex(value))


        dd = str.encode(self.PD)
    
        self.port.write(bytearray.fromhex('1D 68 39 1D 48 00'))
        self.port.write(bytearray.fromhex('1D 6B 49 07') + dd)
        self.port.write(bytearray.fromhex('0A'))

        cabecalhopd = '\n PD: %s | Maquina: %s | Req: %s \n' % (
                                                self.PD,
                                                self.MAQUINA,
                                                self.REQUISICAO)
        
        self.port.write(str.encode(cabecalhopd))

        self.port.write(bytearray.fromhex('1B 61 30'))
        self.port.write(str.encode('CPD: %s | Cabo: %s \n' % (self.CPD, self.CABO)))
        self.port.write(str.encode('Bitola: %s X %s%s \n' % (
                                            self.VIAS,
                                            self.BITOLA,
                                            self.UNIDADE)))

        
        self.port.write(bytearray.fromhex('1B 61 31'))
        self.port.write(bytearray.fromhex('1B 45'))
        self.port.write(str.encode('Medida: %s mm \n' % self.MEDIDA))
        
        self.port.write(bytearray.fromhex('1B 61 30 1B 44 16 17 18 19 20 21 22 23 00')) 
        
        self.port.write(str.encode('Decape A'))
        self.port.write(bytearray.fromhex('09 7C 09'))
        self.port.write(str.encode('Decape B'))
        self.port.write(bytearray.fromhex('0A'))
        
        self.port.write(str.encode(self.DECAPE_A))        
        self.port.write(bytearray.fromhex('09 7C 09'))
        self.port.write(str.encode(self.DECAPE_B))
        self.port.write(bytearray.fromhex('0A'))
        
        self.port.write(str.encode(self.ACABAMENTO_1))        
        self.port.write(bytearray.fromhex('09 7C 09'))
        self.port.write(str.encode(self.ACABAMENTO_2))
        self.port.write(bytearray.fromhex('0A'))
        
        self.port.write(str.encode(self.ACABAMENTO_3))        
        self.port.write(bytearray.fromhex('09 7C 09'))
        self.port.write(str.encode(self.ACABAMENTO_4))
        self.port.write(bytearray.fromhex('0A'))
        
        self.port.write(bytearray.fromhex('1B 61 31'))
        self.port.write(str.encode('Quantidade: %s pcs' % QTD_Cortada))
        self.port.write(bytearray.fromhex('0A'))
        
        self.port.write(bytearray.fromhex('1B 46'))
        self.port.write(bytearray.fromhex('1B 61 30'))
        self.port.write(str.encode('Observacao: %s \n\n' % self.OBSERVACAO))
        self.port.write(str.encode('Gravacao: %s \n' % self.GRAVACAO))

        self.port.write(str.encode('Produto Final: %s \n' % self.CHICOTE))
        self.port.write(str.encode('Data de Entrega: %s \n' % self.DATA_ENTREGA))
        self.port.write(str.encode('Usuário: %s \n' % nomeUsuario))
        self.port.write(str.encode(
            'Data de Impressao: %s \n' % datetime.datetime.now().strftime(
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

        #self.port.write(str.encode(stringTeste))
            
        #self.port.write(bytearray.fromhex('1B 69'))
        
        self.closePort()
