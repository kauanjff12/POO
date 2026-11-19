import os


def tipo_persistencia():
    try:
        import streamlit as st
        return st.session_state.get("tipo_persistencia", "JSON")
    except Exception:
        return os.environ.get("TIPO_PERSISTENCIA", "JSON")


def criar_dao(tipo):
    tipo = tipo.lower()

    if tipo_persistencia().lower() in ("sqlite", "sql", "dao_sql"):

        from dao_sql.clientedao import ClienteDAO
        from dao_sql.profissionaldao import ProfissionalDAO
        from dao_sql.servicodao import ServicoDAO
        from dao_sql.horariodao import HorarioDAO
        from dao_sql.atendimentodao import AtendimentoDAO

    else:

        from dao_json.clientedao import ClienteDAO
        from dao_json.profissionaldao import ProfissionalDAO
        from dao_json.servicodao import ServicoDAO
        from dao_json.horariodao import HorarioDAO
        from dao_json.atendimentodao import AtendimentoDAO

    classes = {
        "cliente": ClienteDAO,
        "profissional": ProfissionalDAO,
        "servico": ServicoDAO,
        "horario": HorarioDAO,
        "atendimento": AtendimentoDAO
    }

    if tipo not in classes:
        raise ValueError("Tipo de DAO desconhecido: " + tipo)

    return classes[tipo]()