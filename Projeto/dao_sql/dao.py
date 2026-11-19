from abc import ABC, abstractmethod
from dao_sql.database import conectar


class DAO(ABC):

    def __init__(self, tabela):
        self._tabela = tabela

    def _executar(self, sql, valores=(), buscar=False):
        con = conectar()
        cur = con.cursor()

        cur.execute(sql, valores)

        if buscar:
            resultado = cur.fetchall()
        else:
            resultado = cur.lastrowid

        con.commit()
        con.close()

        return resultado

    @abstractmethod
    def inserir(self, obj):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def listar_id(self, id):
        pass

    @abstractmethod
    def atualizar(self, obj):
        pass

    @abstractmethod
    def excluir(self, id):
        pass
