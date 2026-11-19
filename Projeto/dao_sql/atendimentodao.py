from datetime import datetime
from models.atendimento import Atendimento
from dao_sql.dao import DAO


class AtendimentoDAO(DAO):

    def __init__(self):
        super().__init__("atendimentos")

    def inserir(self, obj):
        novo_id = self._executar(
            """
            INSERT INTO atendimentos
            (data, queixa_principal, historico_saude,
             avaliacao, prescricao, id_horario)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                obj.get_data().strftime("%d/%m/%Y %H:%M"),
                obj.get_queixa_principal(),
                obj.get_historico_saude(),
                obj.get_avaliacao(),
                obj.get_prescricao(),
                obj.get_id_horario()
            )
        )

        obj.set_id(novo_id)

    def listar(self):
        rows = self._executar(
            """
            SELECT id, data, queixa_principal,
                   historico_saude, avaliacao,
                   prescricao, id_horario
            FROM atendimentos
            ORDER BY id
            """,
            buscar=True
        )

        return [self._objeto(row) for row in rows]

    def listar_id(self, id):
        rows = self._executar(
            """
            SELECT id, data, queixa_principal,
                   historico_saude, avaliacao,
                   prescricao, id_horario
            FROM atendimentos
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
            UPDATE atendimentos
            SET data = ?, queixa_principal = ?,
                historico_saude = ?, avaliacao = ?,
                prescricao = ?, id_horario = ?
            WHERE id = ?
            """,
            (
                obj.get_data().strftime("%d/%m/%Y %H:%M"),
                obj.get_queixa_principal(),
                obj.get_historico_saude(),
                obj.get_avaliacao(),
                obj.get_prescricao(),
                obj.get_id_horario(),
                obj.get_id()
            )
        )

    def excluir(self, id):
        self._executar(
            "DELETE FROM atendimentos WHERE id = ?",
            (id,)
        )

    def _objeto(self, row):
        data = datetime.strptime(row[1], "%d/%m/%Y %H:%M")

        return Atendimento(
            row[0],
            data,
            row[2],
            row[3],
            row[4],
            row[5],
            row[6]
        )