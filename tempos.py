from datetime import datetime as dt
from banco import BANCO
import logger

class TEMPOS():

    def __init__(self):
        self.info = {}

    def tomaTempoEvento(self, FK_ID, FK_TTM, FK_USU, MAQ):
        try:
            banco = BANCO()
            agora = dt.now()

            cur = banco.conexao.cursor()

            cur.execute("""INSERT INTO TEMPOS (
                                DATA,
                                FK_ID,
                                FK_TTM,
                                FK_USU,
                                MAQUINA)
                            VALUES
                                (datetime(?),
                                ?,
                                ?,
                                ?,
                                ?)
                                """, (agora,
                                      FK_ID,
                                      FK_TTM,
                                      FK_USU,
                                      MAQ))

            banco.conexao.commit()
        except Exception as e:
            logger.logError("Erro ao tomar tempo de Evento    -    Details: {}".format(str(e)))

    def tomaTempoParada(self, FK_ID, FK_TTM, FK_USU, MAQ, MOT):
        try:
            banco = BANCO()
            agora = dt.now()

            cur = banco.conexao.cursor()

            cur.execute("""INSERT INTO TEMPOS (
                                        DATA,
                                        FK_ID,
                                        FK_TTM,
                                        FK_USU,
                                        MAQUINA,
                                        FK_MOT)
                                    VALUES
                                        (datetime(?),
                                         ?,
                                         ?,
                                         ?,
                                         ?,
                                         ?)
                                        """, (agora,
                                              FK_ID,
                                              FK_TTM,
                                              FK_USU,
                                              MAQ,
                                              MOT))

            banco.conexao.commit()
        except Exception as e:
            logger.logError("Erro ao tomar tempo de parada    -    Details: {}".format(str(e)))

