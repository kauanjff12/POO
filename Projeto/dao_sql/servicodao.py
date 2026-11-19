from models.servico import Servico
from dao_sql.dao import DAO


class ServicoDAO(DAO):

    def __init__(self):
        super().__init__("servicos")

    def inserir(self, obj):
        novo_id = self._executar(
            """
            INSERT INTO servicos (descricao, valor)
            VALUES (?, ?)
            """,
            (
                obj.get_descricao(),
                obj.get_valor()
            )
        )

        obj.set_id(novo_id)

    def listar(self):
        rows = self._executar(
            """
            SELECT id, descricao, valor
            FROM servicos
            ORDER BY id
            """,
            buscar=True
        )

        return [
            Servico(row[0], row[1], row[2])
            for row in rows
        ]

    def listar_id(self, id):
        rows = self._executar(
            """
            SELECT id, descricao, valor
            FROM servicos
            WHERE id = ?
            """,
            (id,),
            buscar=True
        )

        if not rows:
            return None

        row = rows[0]

        return Servico(row[0], row[1], row[2])

    def atualizar(self, obj):
        self._executar(
            """
            UPDATE servicos
            SET descricao = ?, valor = ?
            WHERE id = ?
            """,
            (
                obj.get_descricao(),
                obj.get_valor(),
                obj.get_id()
            )
        )

    def excluir(self, id):
        self._executar(
            "DELETE FROM servicos WHERE id = ?",
            (id,)
        )