from pymongo import MongoClient
from pprint import pprint
import datetime
import os
import configparser
import json

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
    self.tempo_setup = None
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
    self.tempo_setup = self.hora_inicio_corte - self.hora_inicio_ciclo

  def cycle_pause(self, motivo_parada, hora_incio_parada, tempo_total_parada, estado_equipamento_parada):
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
    self.tempo_total_ciclo = self.hora_final_ciclo - self.hora_inicio_ciclo
    self.tempo_total_corte = self.hora_final_ciclo - self.hora_inicio_corte
    self.tempo_total_paradas = 0
    self.tempo_total_paradas_ocioso = 0
    self.tempo_total_paradas_setup = 0
    self.tempo_total_paradas_corte = 0

    if len(self.paradas) > 0:
      for parada in self.paradas:
        self.tempo_total_paradas += parada.get('stopTotalTime')
        
        if parada.get('stopReason') == 'ocioso':
          self.tempo_total_paradas_ocioso += parada.get('stopTotalTime')
        elif parada.get('stopReason') == 'setup':
          self.tempo_total_paradas_setup += parada.get('stopTotalTime')
        elif parada.get('stopReason') == 'corte':
          self.tempo_total_paradas_corte += parada.get('stopTotalTime') 

      self.tempo_total_setup.total_seconds() -= self.tempo_total_paradas_setup
      self.tempo_total_corte.total_seconds() -= self.tempo_total_paradas_corte

    self.format_to_json()
    
  def justify_partial_cut(self, motivo_corte_parcial):
    self.motivo_corte_parcial = motivo_corte_parcial

  def print_cycle(self):
    print("Máquina: {}".format(str(self.maquina)))
    print("Operador: {}".format(str(self.operador)))
    print("PD: {}".format(str(self.dados_PD)))
    print("----------------------------------------------------------")
    print("Horário do Inicio do Ciclo: {}".format(str(self.hora_inicio_ciclo)))
    print("Horário do Final do Ciclo: {}".format(str(self.hora_final_ciclo)))
    print("----------------------------------------------------------")
    print("Horário do Inicio do Corte: {}".format(str(self.hora_inicio_corte)))
    print("----------------------------------------------------------")
    print("Quantidade da Requisicao: {}".format(str(self.quantidade_requisicao)))
    print("Quantidade Cortada no Ciclo: {}".format(str(self.quantidade_cortada)))
    print("Motivo para Corte Parcial: {}".format(str(self.motivo_corte_parcial)))
    print("----------------------------------------------------------")
    print("Paradas: {}".format(str(self.paradas)))
    print("----------------------------------------------------------")
    print("Tempo Total do Ciclo: {}".format(str(self.tempo_total_ciclo)))
    print("Tempo do Setup: {}".format(str(self.tempo_setup)))
    print("Tempo Total do Corte: {}".format(str(self.tempo_total_corte)))
    print("Tempo Total de Paradas: {}".format(str(self.tempo_total_paradas)))

  def format_to_json(self):
    self.cycle_data = {
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
      "setupTotalTime" : self.tempo_setup,
      "cutTotalTime" : self.tempo_total_corte,
      "stopsTotalTime" : self.tempo_total_paradas,
    }

    def my_converter(o):
      if isinstance(o, datetime.datetime):
        return o.__str__()
      elif isinstance(o, datetime.timedelta):
        return o.total_seconds()

    self.json_object = json.dumps(self.cycle_data, default = my_converter, indent=4)
 
    print(self.json_object)