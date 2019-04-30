from datetime import datetime as dt
from banco import BANCO

class TEMPOS():

    def __init__(self):
        self.info = {}

    def tomaTempoInicioCiclo(self, ID, USU, MAQ):

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
                            """ %   (agora,
                                    ID,
                                    1,
                                    USU,
                                    MAQ))

        banco.conexao.commit()