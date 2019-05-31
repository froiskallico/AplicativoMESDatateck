import serial
import datetime
from collections import OrderedDict

class etiqueta(object):

	def __init__(self):
		pass

	def openPort(self):
		port = serial.Serial(
		"/dev/ttyACM0",
		baudrate=115200,
		parity=serial.PARITY_NONE,
		writeTimeout=3,
		timeout =3)

		print(port.isOpen())
		print("Port opened...")

	def closePort(self):
		port.close()

		while True:
			print("inside while")
			response=port.read(8)
			print(response)
			print ("Data Received")
			break

	def imprimeEtiqueta(self, QTD_Cortada=None, **kwargs):
		for key, value in kwargs.items():
			setattr(self, key, str(value).strip().replace('None', '-'))

		print(QTD_Cortada)
		#Todo: self.dados.get(['nome_do_campo'])

		# valor = '1234567'
		# pd = '1811'
		# maquina = 'Junquan'
		# req = '83940'
		# cabo = 'COND C.F 1,0 PT 750V 105C'
		# bitola = '1X1 mm'
		# medida = '900'
		# deca = '11'
		# decb = '11'
		# acab1 = 'ZV3MA0039'
		# acab2 = 'ZV3MA0039'
		# acab3 = '-'
		# acab4 = '-'
		# qtd = '36'
		# obs = 'teste obs'
		# grav = 'teste grav'
		# prod = '05903199'
		# entr = '06/07/2019'
		# impressao = '29/05/2019'


		# port.write(bytearray.fromhex('0A'))

		configs = OrderedDict([
					          ('printConfig', '1D F9 35 30'),
					          ('printerMode', '1D F9 2D 31'),
							  ('charAlignmt', '1B 61 31')
							 ])

		for value in configs.values():
				print(bytearray.fromhex(value))


		n = (str.encode(str(len(self.PD))))
		dd = (str.encode(self.PD))
		#print(bytearray.fromhex('1D 6B 49 07') + dd)
		print(bytearray.fromhex('1D 68 39 1D 6B 49 07') + dd)

		cabecalhopd = 'PD: %s | Maquina: %s | Req: %s \n' % (
												self.PD,
												self.MAQUINA,
												self.REQUISICAO)
		
		print(str.encode(cabecalhopd))

		print(bytearray.fromhex('1B 61 30'))
		print(str.encode('Cabo: %s \n' % self.CABO))
		print(str.encode('Bitola: %s X %s%s \n' % (
			                                self.VIAS,
			                                self.BITOLA,
			                                self.UNIDADE)))

		print(bytearray.fromhex('1B 61 31'))
		print(bytearray.fromhex('1B 45'))
		print(str.encode('Medida: %s mm \n' % self.MEDIDA))

		print(str.encode('Decape A \t Decape B \n'))

		print(str.encode('%s \t %s \n' % (self.DECAPE_A, self.DECAPE_B)))

		print(str.encode('%s \t %s \n' % (self.ACABAMENTO_1, self.ACABAMENTO_2)))
		print(str.encode('%s \t %s \n' % (self.ACABAMENTO_3, self.ACABAMENTO_4)))

		print(str.encode('\n Quantidade: %s pcs \n' % QTD_Cortada))

		print(bytearray.fromhex('1B 46'))
		print(bytearray.fromhex('1B 61 30'))
		print(str.encode('Observacao: %s \n\n' % self.OBSERVACAO))
		print(str.encode('Gravacao: %s \n' % self.GRAVACAO))

		print(str.encode('Produto Final: %s \n' % self.CHICOTE))
		print(str.encode('Data de Entrega: %s \n' % self.DATA_ENTREGA))
		print(str.encode(
			'Data de Impressao: %s \n' % datetime.datetime.now().strftime(
				'%d-%m-%Y  %H:%M:%S')))

		print(bytearray.fromhex('1B 69'))