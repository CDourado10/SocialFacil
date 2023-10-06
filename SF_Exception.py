

class UsuarioNaoEncontradoException(Exception):
    def __init__(self, usuario_id):
        super().__init__(f"Usuário com ID {usuario_id} não encontrado.")

class InformacoesPaginaNaoEncontradasException(Exception):
    def __init__(self, informacoes_id):
        super().__init__(f"Página com ID {informacoes_id} não encontrada.")

class SiteNaoEncontradoException(Exception):
    def __init__(self, site_id):
        self.site_id = site_id
        self.message = f"O site com o ID {site_id} não foi encontrado."
        super().__init__(self.message)

class AssuntoNaoEncontradoException(Exception):
    def __init__(self, assunto_id):
        self.assunto_id = assunto_id
        self.message = f"O assunto com o ID {assunto_id} não foi encontrado."
        super().__init__(self.message)