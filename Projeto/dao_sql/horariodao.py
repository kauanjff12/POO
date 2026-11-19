from datetime import datetime
from models.horario import Horario
from dao_sql.dao import DAO


class HorarioDAO(DAO):

    def __init__(self):
        super().__init__("horarios")

    def inserir(self, obj):
        novo_id = self._executar(
            """
            INSERT INTO horarios
            (data, confirmado, id_cliente,
             id_servico, id_profissional)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                obj.get_data().strftime("%d/%m/%Y %H:%M"),
                int(obj.get_confirmado()),
                obj.get_id_cliente(),
                obj.get_id_servico(),
                obj.get_id_profissional()
            )
        )

        obj.set_id(novo_id)

    def listar(self):
        rows = self._executar(
            """
            SELECT id, data, confirmado, id_cliente,
                   id_servico, id_profissional
            FROM horarios
            ORDER BY id
            """,
            buscar=True
        )

        return [self._objeto(row) for row in rows]

    def listar_id(self, id):
        rows = self._executar(
            """
            SELECT id, data, confirmado, id_cliente,
                   id_servico, id_profissional
            FROM horarios
            WHERE id = ?
            """,
            (id,),
            buscar=True
        )

        if not rows:
            return None

        return self._objeto(rows[0])

    def atualizar(self, obj):
        self._executar(
            """
            UPDATE horarios
            SET data = ?, confirmado = ?, id_cliente = ?,
                id_servico = ?, id_profissional = ?
            WHERE id = ?
            """,
            (
                obj.get_data().strftime("%d/%m/%Y %H:%M"),
                int(obj.get_confirmado()),
                obj.get_id_cliente(),
                obj.get_id_servico(),
                obj.get_id_profissional(),
                obj.get_id()
            )
        )

    def excluir(self, id):
        self._executar(
            "DELETE FROM horarios WHERE id = ?",
            (id,)
        )

    def _objeto(self, row):
        data = datetime.strptime(row[1], "%d/%m/%Y %H:%M")

        obj = Horario(row[0], data)

        obj.set_confirmado(bool(row[2]))
        obj.set_id_cliente(row[3])
        obj.set_id_servico(row[4])
        obj.set_id_profissional(row[5])

        return obj