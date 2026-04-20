class Usuarios:
    def __init__(self, api_context):
        self.api_context = api_context
        self.endpoint = "/usuarios"

    def criar_usuarios(self, nome, email, password, administrador):
        return self.api_context.post(self.endpoint, data={
            'nome': nome,
            'email': email,
            'password': password,
            'administrador': administrador
        })
    
    def listar_todos_usuarios(self):
        return self.api_context.get(self.endpoint)

    def listar_usuario(self, id_usuario):
        return self.api_context.get(f'{self.endpoint}/{id_usuario}')
    
    def deletar_usuario(self, id_usuario):
        return self.api_context.delete(f'{self.endpoint}/{id_usuario}')
    
    def alterar_usuario(self, id_usuario, nome, email, password, administrador):
        return self.api_context.put(f'{self.endpoint}/{id_usuario}', data={
            'nome': nome,
            'email': email,
            'password': password,
            'administrador': administrador
        })
    