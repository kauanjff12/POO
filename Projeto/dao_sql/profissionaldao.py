from models.profissional import Profissional
from dao_sql.dao import DAO


class ProfissionalDAO(DAO):

    def __init__(self):
        super().__init__("profissionais")

    def inserir(self, obj):
        novo_id = self._executar(
            """
            INSERT INTO profissionais
            (nome, email, especialidade, senha)
            VALUES (?, ?, ?, ?)
            """,
            (
                obj.get_nome(),
                obj.get_email(),
                obj.get_especialidade(),
                obj.get_senha()
            )
        )

        obj.set_id(novo_id)

    def listar(self):
        rows = self._executar(
            """
            SELECT id, nome, email, especialidade, senha
            FROM profissionais
            ORDER BY id
            """,
            buscar=True
        )

        return [
            Profissional(
                row[0], row[1], row[2], row[3], row[4]
            )
            for row in rows
        ]

    def listar_id(self, id):
        rows = self._executar(
            """
            SELECT id, nome, email, especialidade, senha
            FROM profissionais
            WHERE id = ?
            """,
            (id,),
            buscar=True
        )

        if not rows:
            return None

        row = rows[0]

        return Profissional(
            row[0], row[1], row[2], row[3], row[4]
        )

    def atualizar(self, obj):
        self._executar(
            """
            UPDATE profissionais
            SET nome = ?, email = ?, especialidade = ?, senha = ?
            WHERE id = ?
            """,
            (
                obj.get_nome(),
                obj.get_email(),
                obj.get_especialidade(),
                obj.get_senha(),
                obj.get_id()
            )
        )

    def excluir(self, id):
        self._executar(
            "DELETE FROM profissionais WHERE id = ?",
            (id,)
        )