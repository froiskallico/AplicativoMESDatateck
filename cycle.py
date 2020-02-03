from pymongo import MongoClient
from pprint import pprint
import datetime
import os
import configparser

class cycle(object):
  def __init__(self):
    self.define_parameters()

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

  def cycle_start_cut(self):
    self.hora_inicio_corte = datetime.datetime.now()
    self.tempo_setup = self.hora_inicio_corte - self.hora_inicio_ciclo

  def cycle_pause(self, motivo_parada, hora_incio_parada, tempo_total_parada):
    self.paradas.append({
      "motivo": motivo_parada,
      "hora_inicio_parada": hora_incio_parada,
      "tempo_total_parada": tempo_total_parada
    })

  def cycle_stop(self, quantidade_requisicao, quantidade_cortada, motivo_corte_parcial = None):
    self.hora_final_ciclo = datetime.datetime.now()
    self.quantidade_requisicao = quantidade_requisicao
    self.quantidade_cortada = quantidade_cortada
    self.motivo_corte_parcial = motivo_corte_parcial
    self.tempo_total_ciclo = self.hora_final_ciclo - self.hora_inicio_ciclo
    self.tempo_total_corte = self.hora_final_ciclo - self.hora_inicio_corte
    self.tempo_total_paradas = 0
    if len(paradas) > 0:
      for parada in self.paradas:
        self.tempo_total_paradas += parada.get('tempo_total_parada')
    
    
  def print_cycle(self):
    print(self.maquina)
    print(self.operador)
    print(self.dados_PD)
    print(self.inicioCiclo)
    print(self.paradas)

