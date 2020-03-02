from pymongo import MongoClient
import datetime
import os
import configparser

class cycle(object):
  def __init__(self):
    self.reset_values()
    self.define_parameters()

  def reset_values(self):
    self.maquina = None
    self.operador = None
    self.dados_PD = None
    self.hora_inicio_ciclo = None
    self.hora_final_ciclo = None
    self.hora_inicio_corte = None
    self.quantidade_requisicao = None
    self.quantidade_cortada = None
    self.motivo_corte_parcial = None
    self.paradas = None
    self.tempo_total_ciclo = None
    self.tempo_total_setup = None
    self.tempo_total_corte = None
    self.tempo_total_paradas = None
    self.tempo_total_paradas_ocioso = None
    self.tempo_total_paradas_setup = None
    self.tempo_total_paradas_corte = None

  def faker_values(self):
    self.maquina = "CLN-06"
    self.operador = "Kallico"
    self.dados_PD = {'PK_IRP': 891407, 'REQUISICAO': 123547, 'CELULA': 'RASTREADORES', 'DATA_GERACAO': '2019-12-10 12:16:55.156000', 'DATA_ENTREGA': '2020-01-06 00:00:00', 'OBSERVACAO_REQ': '6001098 - NOVO CHICOTE 34V SMARTGATE - FEVEREIRO', 'CHICOTE': '6001010 - NOVO CHICOTE PORTA RELE', 'PD': 13059, 'CPD': 7754, 'CABO': 'COND C.F 1,5 PT 105 300V', 'FK_CRS': 7, 'VIAS': '1                        ', 'BITOLA': 1.5, 'UNIDADE': 'MM2', 'NORMA': 'DIN 72551-6', 'QTD_PD_REQ': 300, 'QTD_CORTADA': 0, 'MEDIDA': 500, 'DECAPE_A': 'S/6', 'DECAPE_B': '5', 'ACABAMENTO_1': 'G-99761BS-0', 'PONTE_1': 'S', 'ACABAMENTO_2': '881111-1 (BUFFER)', 'PONTE_2': 'N', 'ACABAMENTO_3': None, 'PONTE_3': 'N', 'ACABAMENTO_4': None, 'PONTE_4': 'N', 'OBSERVACAO': 'CRIMPAR ACABAMENTO 1 (G-99761BS-0) JUNTO COM DIODO. COLOCAR ESPAGUETE', 'GRAVACAO': None, 'MAQUINA': 'CLN-06', 'NR_ORDEM_CORTE': 0, 'PRIORIDADE': 19119, 'DESCRICAO': 'PT', 'PRIMARIA': '#000000', 'SECUNDARIA': '#000000', 'COR_TEXTO': '#ffffff'}
    self.hora_inicio_ciclo = datetime.datetime(2020, 2, 7, 8, 34, 40)
    self.hora_final_ciclo = datetime.datetime(2020, 2, 7, 8, 35, 27)
    self.hora_inicio_corte = datetime.datetime(2020, 2, 7, 8, 35, 9)
    self.quantidade_requisicao = 300
    self.quantidade_cortada = 1
    self.motivo_corte_parcial = 7
    self.paradas = [
        {
            "stopReason": "REUNIÃO/TREINAMENTO",
            "stopStartTime": "2020-02-07 08:34:43.645670",
            "stopTotalTime": 2.467489,
            "stopEquipmentStatus": "ocioso"
        },
        {
            "stopReason": "BANHEIRO",
            "stopStartTime": "2020-02-07 08:34:58.080354",
            "stopTotalTime": 2.28129,
            "stopEquipmentStatus": "setup"
        },
        {
            "stopReason": "FALTA DE PROGRAMA\\u00c7\\u00c3O (PCP)",
            "stopStartTime": "2020-02-07 08:35:05.125849",
            "stopTotalTime": 3.406472,
            "stopEquipmentStatus": "ocioso"
        },
        {
            "stopReason": "MANUTEN\\u00c7\\u00c3O",
            "stopStartTime": "2020-02-07 08:35:12.909366",
            "stopTotalTime": 5.484992,
            "stopEquipmentStatus": "corte"
        }
    ]
    self.tempo_total_ciclo = None
    self.tempo_total_setup = self.hora_inicio_corte - self.hora_inicio_ciclo
    self.tempo_total_corte = None
    self.tempo_total_paradas = None
    self.tempo_total_paradas_ocioso = None
    self.tempo_total_paradas_setup = None
    self.tempo_total_paradas_corte = None

  def define_parameters(self):
    diretorio = os.path.dirname(os.path.abspath(__file__))
    
    configFile = configparser.ConfigParser()
    configFile.read(diretorio + './config.ini')

    self.maquina = configFile['DEFAULT']['maquina']
    self.paradas = []

  def cycle_start(self, operador, dados_PD):
    self.operador = operador
    
    self.dados_PD = dados_PD
    self.hora_inicio_ciclo = datetime.datetime.now()

  def cut_start(self):
    self.hora_inicio_corte = datetime.datetime.now()

  def cycle_pause(self, motivo_parada, hora_incio_parada, tempo_total_parada, estado_equipamento_parada):
    print(tempo_total_parada)

    self.paradas.append({
      "stopReason": motivo_parada,
      "stopStartTime": hora_incio_parada,
      "stopTotalTime": tempo_total_parada.total_seconds(),
      "stopEquipmentStatus": estado_equipamento_parada
    })

  def cycle_stop(self, quantidade_requisicao, quantidade_cortada):
    self.hora_final_ciclo = datetime.datetime.now()
    self.quantidade_requisicao = quantidade_requisicao
    self.quantidade_cortada = quantidade_cortada

    self.compute_cycle_times()

  def compute_cycle_times(self):
    self.tempo_total_corte = self.hora_final_ciclo - self.hora_inicio_corte
    self.tempo_total_setup = self.hora_inicio_corte - self.hora_inicio_ciclo
    self.tempo_total_ciclo = self.hora_final_ciclo - self.hora_inicio_ciclo
    self.tempo_total_paradas = 0
    self.tempo_total_paradas_ocioso = 0
    self.tempo_total_paradas_setup = 0
    self.tempo_total_paradas_corte = 0    

    for parada in self.paradas:
      self.tempo_total_paradas += parada.get('stopTotalTime')

      if parada.get('stopEquipmentStatus') == 'ocioso':
        self.tempo_total_paradas_ocioso += parada.get('stopTotalTime')
      elif parada.get('stopEquipmentStatus') == 'setup':
        self.tempo_total_paradas_setup += parada.get('stopTotalTime')
      elif parada.get('stopEquipmentStatus') == 'corte':
        self.tempo_total_paradas_corte += parada.get('stopTotalTime') 

    self.tempo_total_ciclo = self.tempo_total_ciclo.total_seconds()
    print(self.tempo_total_ciclo)
    self.tempo_total_setup = self.tempo_total_setup.total_seconds() 
    print(self.tempo_total_setup)
    self.tempo_total_corte = self.tempo_total_corte.total_seconds()
    print(self.tempo_total_corte)

    self.consolidate_data()
        
  def justify_partial_cut(self, motivo_corte_parcial):
    self.motivo_corte_parcial = motivo_corte_parcial

  def consolidate_data(self):
    self.cycle_data = {
      "created" : datetime.datetime.now(),
      "machine" : self.maquina,
      "operator" : self.operador,
      "PD-Data" : self.dados_PD,
      "cycleStartTime" : self.hora_inicio_ciclo,
      "cycleFinishTime" : self.hora_final_ciclo,
      "cutStartTime" : self.hora_inicio_corte,
      "requiredQuantity" : self.quantidade_requisicao,
      "cuttedQuantity" : self.quantidade_cortada,
      "partialCutReason" : self.motivo_corte_parcial,
      "stops" : self.paradas,
      "cycleTotalTime" : self.tempo_total_ciclo,
      "setupTotalTime" : self.tempo_total_setup,
      "cutTotalTime" : self.tempo_total_corte,
      "stopsTotalTime" : self.tempo_total_paradas,
      "busyStopsTotalTime" : self.tempo_total_paradas_ocioso,
      "setupStopsTotalTime" : self.tempo_total_paradas_setup,
      "cutStopsTotalTime" : self.tempo_total_paradas_corte,
      "setupEffectiveTotalTime" : self.tempo_total_setup - self.tempo_total_paradas_setup,
      "cutEffectiveTotalTime" : self.tempo_total_corte - self.tempo_total_paradas_corte
    }    

    self.send_data_to_mongodb()
 
  def send_data_to_mongodb(self):
    mongo_client = MongoClient("mongodb://deploy:Data2803@datateck0-shard-00-00-yjact.mongodb.net:27017,datateck0-shard-00-01-yjact.mongodb.net:27017,datateck0-shard-00-02-yjact.mongodb.net:27017/test?ssl=true&replicaSet=Datateck0-shard-0&authSource=admin&retryWrites=true&w=majority")

    db = mongo_client['smartPrep']
    collection = db.produtividade

    inserted = collection.insert_one(self.cycle_data)
    return inserted
    
    