from models.cliente import Cliente
from models.clientedao import ClienteDAO
from models.servico import Servico
from models.servicodao import ServicoDAO
from models.horario import Horario
from models.horariodao import HorarioDAO
from models.atendimento import Atendimento
from models.atendimentodao import AtendimentoDAO
from models.profissional import Profissional
from models.profissionaldao import ProfissionalDAO
from datetime import datetime, timedelta

class Service:
    @staticmethod
    def cliente_inserir(nome, email, fone, senha):
        Service._cliente_validar_email(email)
        obj = Cliente(0, nome, email, fone, senha)
        ClienteDAO().inserir(obj)
    @staticmethod
    def cliente_listar():
        r = ClienteDAO().listar()
        r.sort(key = lambda obj : obj.get_nome().casefold())
        return r
    @staticmethod
    def cliente_listar_id(id):
        return ClienteDAO().listar_id(id)
    @staticmethod
    def cliente_atualizar(id, nome, email, fone, senha):
        Service._cliente_validar_email(email, id)
        obj = Cliente(id, nome, email, fone, senha)
        ClienteDAO().atualizar(obj)
    @staticmethod
    def cliente_excluir(id):
        if any(h.get_id_cliente() == id for h in Service.horario_listar()):
            raise ValueError("Não é possível excluir um cliente com horário agendado.")
        ClienteDAO().excluir(id)

    @staticmethod
    def _cliente_validar_email(email, id_cliente=None):
        email_normalizado = email.strip().casefold()
        if email_normalizado == "admin":
            raise ValueError("O e-mail 'admin' é reservado para o administrador.")
        for cliente in ClienteDAO().listar():
            if cliente.get_id() != id_cliente and cliente.get_email().strip().casefold() == email_normalizado:
                raise ValueError("Já existe um cliente com este e-mail.")
        for profissional in ProfissionalDAO().listar():
            if profissional.get_email().strip().casefold() == email_normalizado:
                raise ValueError("Já existe um profissional com este e-mail.")
    @staticmethod
    def cliente_criar_admin():
        for c in Service.cliente_listar():
            if c.get_email() == "admin": return
        Service.cliente_inserir("admin", "admin", "fone", "1234")
    @staticmethod
    def cliente_autenticar(email, senha):
        for c in Service.cliente_listar():
            if c.get_email() == email and c.get_senha() == senha:
                return {"id": c.get_id(), "nome": c.get_nome()}
        return None        


    @staticmethod
    def servico_inserir(descricao, valor):
        obj = Servico(0, descricao, valor)
        ServicoDAO().inserir(obj)
    @staticmethod
    def servico_listar():
        r = ServicoDAO().listar()
        r.sort(key = lambda obj : obj.get_descricao().casefold())
        return r
    @staticmethod
    def servico_listar_id(id):
        return ServicoDAO().listar_id(id)
    @staticmethod
    def servico_atualizar(id, descricao, valor):
        obj = Servico(id, descricao, valor)
        ServicoDAO().atualizar(obj)
    @staticmethod
    def servico_excluir(id):
        ServicoDAO().excluir(id)


    @staticmethod
    def horario_inserir(data, confirmado, id_cliente, id_servico, id_profissional):
        Service._horario_validar_conflito(data, id_profissional)
        c = Horario(0, data)
        c.set_confirmado(confirmado)
        c.set_id_cliente(id_cliente)
        c.set_id_servico(id_servico)
        c.set_id_profissional(id_profissional)
        HorarioDAO().inserir(c)
    @staticmethod
    def horario_listar(): # select com order by
        r = HorarioDAO().listar()
        r.sort(key = lambda obj : obj.get_data())
        return r
    @staticmethod
    def horario_listar_id(id): 
        return HorarioDAO().listar_id(id)
    @staticmethod
    def horario_atualizar(id, data, confirmado, id_cliente, id_servico, id_profissional):
        Service._horario_validar_conflito(data, id_profissional, id)
        c = Horario(id, data)
        c.set_confirmado(confirmado)
        c.set_id_cliente(id_cliente)
        c.set_id_servico(id_servico)
        c.set_id_profissional(id_profissional)
        HorarioDAO().atualizar(c)
    @staticmethod
    def horario_excluir(id):
        for h in Service.horario_listar():
            if h.get_id() == id and h.get_id_cliente() is not None:
                raise ValueError("Não é possível excluir um horário já agendado por um cliente.")
        HorarioDAO().excluir(id)

    @staticmethod
    def _horario_validar_conflito(data, id_profissional, id_horario=None):
        for h in Service.horario_listar():
            if h.get_id() != id_horario \
            and h.get_id_profissional() == id_profissional \
            and h.get_data() == data:
                raise ValueError("Já existe um horário cadastrado para este profissional nesta data e hora.")

    @staticmethod
    def horario_listar_disponiveis(id_profissional):
        r = []
        agora = datetime.now()
        for h in Service.horario_listar():
            if h.get_data() >= agora and h.get_confirmado() == False \
            and h.get_id_cliente() == None and h.get_id_profissional() == id_profissional:
                r.append(h)
        r.sort (key = lambda h : h.get_data())
        return r
    @staticmethod
    def horario_abrir_agenda(data, hora_inicio, hora_fim, intervalo, id_profissional):
        data_inicio = datetime.strptime(data + " " + hora_inicio, "%d/%m/%Y %H:%M")
        data_fim = datetime.strptime(data + " " + hora_fim, "%d/%m/%Y %H:%M")
        delta = timedelta(minutes = intervalo)
        x = data_inicio
        while x <= data_fim:
            # insira um horário
            Service.horario_inserir(x, False, None, None, id_profissional)
            # vá para o próximo horário
            x = x + delta
    @staticmethod
    def horario_visualizar_minha_agenda(id_profissional):
        r = []
        for h in Service.horario_listar():
            if h.get_id_profissional() == id_profissional:
                r.append(h)
        r.sort (key = lambda h : h.get_data())
        return r
    @staticmethod
    def horario_visualizar_meus_servicos(id_cliente):  # select com where
        r = []
        for h in Service.horario_listar():
            if h.get_id_cliente() == id_cliente:
                r.append(h)
        r.sort (key = lambda h : h.get_data())
        return r
    @staticmethod
    def horario_confirmar_servico(id_profissional):
        r = []
        for h in Service.horario_listar():
            if h.get_confirmado() == False \
            and h.get_id_cliente() != None and h.get_id_profissional() == id_profissional:
                r.append(h)
        r.sort (key = lambda h : h.get_data())
        return r

    @staticmethod
    def atendimento_inserir(data, queixa_principal, historico_saude, avaliacao, prescricao, id_horario):
        obj = Atendimento(0, data, queixa_principal, historico_saude, avaliacao, prescricao, id_horario)
        AtendimentoDAO().inserir(obj)
    @staticmethod
    def atendimento_listar():
        r = AtendimentoDAO().listar()
        r.sort(key = lambda obj : obj.get_data())
        return r
    @staticmethod
    def atendimento_listar_id(id):
        return AtendimentoDAO().listar_id(id)
    @staticmethod
    def atendimento_atualizar(id, data, queixa_principal, historico_saude, avaliacao, prescricao, id_horario):
        obj = Atendimento(id, data, queixa_principal, historico_saude, avaliacao, prescricao, id_horario)
        AtendimentoDAO().atualizar(obj)
    @staticmethod
    def atendimento_excluir(id):
        AtendimentoDAO().excluir(id)


    @staticmethod
    def profissional_inserir(nome, email, especialidade, senha):
        Service._profissional_validar_email(email)
        obj = Profissional(0, nome, email, especialidade, senha)
        ProfissionalDAO().inserir(obj)
    @staticmethod
    def profissional_listar():
        r = ProfissionalDAO().listar()
        r.sort(key = lambda obj : obj.get_nome().casefold())
        return r
    @staticmethod
    def profissional_listar_id(id):
        return ProfissionalDAO().listar_id(id)
    @staticmethod
    def profissional_atualizar(id, nome, email, especialidade, senha):
        Service._profissional_validar_email(email, id)
        obj = Profissional(id, nome, email, especialidade, senha)
        ProfissionalDAO().atualizar(obj)
    @staticmethod
    def profissional_excluir(id):
        if any(h.get_id_profissional() == id for h in Service.horario_listar()):
            raise ValueError("Não é possível excluir um profissional com horário cadastrado.")
        ProfissionalDAO().excluir(id)

    @staticmethod
    def _profissional_validar_email(email, id_profissional=None):
        email_normalizado = email.strip().casefold()
        if email_normalizado == "admin":
            raise ValueError("O e-mail 'admin' é reservado para o administrador.")
        for cliente in ClienteDAO().listar():
            if cliente.get_email().strip().casefold() == email_normalizado:
                raise ValueError("Já existe um cliente com este e-mail.")
        for profissional in ProfissionalDAO().listar():
            if profissional.get_id() != id_profissional and profissional.get_email().strip().casefold() == email_normalizado:
                raise ValueError("Já existe um profissional com este e-mail.")

    @staticmethod
    def profissional_autenticar(email, senha):
        for c in Service.profissional_listar():
            if c.get_email() == email and c.get_senha() == senha:
                return {"id": c.get_id(), "nome": c.get_nome()}
        return None        
