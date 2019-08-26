import numpy as np
from datetime import datetime
from datetime import timedelta
import configparser
import os


class TempoRestanteAteOFinalDoExpediente():
    def __init__(self):
        self.definicoes()

    def definicoes(self):
        self.diretorio = os.path.dirname(os.path.abspath(__file__))

        self.configFile = configparser.ConfigParser()
        self.configFile.read(self.diretorio + '/config.ini')
        self.horaInicio = self.configFile['EXPEDIENTE']['horaInicio']
        self.horaAlmoco = self.configFile['EXPEDIENTE']['horaAlmoco']
        self.retornoAlmoco = self.configFile['EXPEDIENTE']['retornoAlmoco']
        self.finalExpediente = self.configFile['EXPEDIENTE']['finalExpediente']

    def convTime(self, hora=None):
        hora = datetime.strptime(hora, '%H:%M:%S').time()
        hora = datetime.combine(datetime.today(), hora)
        return hora

    def tempoRestante(self):
        self.horaAtual = datetime.now()

        diff = self.convTime(self.finalExpediente) - self.horaAtual

        if self.horaAtual < self.convTime(self.horaAlmoco):
            diff -= self.convTime(self.retornoAlmoco) - self.convTime(self.horaAlmoco)

        return timedelta.total_seconds(diff)

    def totalExpediente(self):
        diff = self.convTime(self.finalExpediente) - self.convTime(self.horaInicio)
        diff -= self.convTime(self.retornoAlmoco) - self.convTime(self.horaAlmoco)

        return timedelta.total_seconds(diff)

    def percentRestante(self):
        percent = self.tempoRestante() / self.totalExpediente()
        return percent