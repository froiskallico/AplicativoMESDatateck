from banco import BANCO
import logger

class MOTIVOS(object):

    def __init__(self):
        self.listaMotivos = []

    def buscaListaMotivosDivergencia(self):
        banco = BANCO()

        try:
            c = banco.conexao.cursor()
            c.execute('''SELECT 
                             DESCRICAO
                         FROM 
                             MOTIVOS_DIVERGENCIAS
                         ORDER BY
                             DESCRICAO
                       ''')

            linhas = c.fetchall()

            for linha in linhas:
                self.listaMotivos.append(linha[0])

            c.close()

            return self.listaMotivos
        except Exception as e:
            logger.logError("Ocorreu um erro na busca dos motivos    -    Details: {}".format(str(e)))


    def buscaListaMotivosParada(self):
        banco = BANCO()

        try:
            c = banco.conexao.cursor()
            c.execute('''SELECT 
                             DESCRICAO
                         FROM 
                             MOTIVOS_PARADA
                         ORDER BY
                             PK_MOT
                       ''')

            linhas = c.fetchall()

            for linha in linhas:
                self.listaMotivos.append(linha[0])

            c.close()

            return self.listaMotivos
        except Exception as e:
            logger.logError("Ocorreu um erro na busca dos motivos    -    Details: {}".format(str(e)))
