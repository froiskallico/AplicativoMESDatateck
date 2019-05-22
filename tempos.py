from datetime import datetime as dt
from banco import BANCO

class TEMPOS():

    def __init__(self):
        self.info = {}

    def tomaTempoEvento(self, FK_ID, FK_TTM, FK_USU, MAQ):
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
                            ("%s",
                            %i,
                            %i,
                            %i,
                            "%s")
                            """ % (agora,
                                    FK_ID,
                                    FK_TTM,
                                    FK_USU,
                                    MAQ))

        banco.conexao.commit()

    def tomaTempoParada(self, FK_ID, FK_TTM, FK_USU, MAQ, MOT):
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
                                    ("%s",
                                    %i,
                                    %i,
                                    %i,
                                    "%s",
                                    %i)
                                    """ % (agora,
                                           FK_ID,
                                           FK_TTM,
                                           FK_USU,
                                           MAQ,
                                           MOT))

        banco.conexao.commit()

