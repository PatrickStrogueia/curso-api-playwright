import random
from faker import Faker
from page_objects.usuarios import Usuarios
from helpers.validators import validar_status, validar_mensagem_json

fake = Faker()
nome = fake.name()
email = fake.email()
password = fake.password()
administrador = random.choice(["true", "false"])
print(nome, email, password, administrador)


def test_crud_usuarios(api_context):
        service = Usuarios(api_context=api_context)

        # CREATE
        response_create = service.criar_usuarios(nome=nome, 
                                                 email=email, 
                                                 password=password, 
                                                 administrador=administrador)

        print(response_create.json())
        validar_status(response_create, 201)
        validar_mensagem_json(response_create, 'Cadastro realizado com sucesso')
        user_id = response_create.json()['_id']

        # READ

        response_read = service.listar_usuario(id_usuario=user_id)
        validar_status(response_read, 200)
        assert response_read.json()['_id'] == user_id
        assert response_read.json()['email'] == email

        # UPDATE
        
        response_update = service.alterar_usuario(id_usuario=user_id,
                                                  nome=f'{nome} Update',
                                                  email=email,
                                                  password=password,
                                                  administrador=administrador)

        validar_status(response_update, 200)

        validar_mensagem_json(response_update, 'Registro alterado com sucesso')

        response_read = service.listar_usuario(id_usuario=user_id)
        validar_status(response_read, 200)
        assert response_read.json()['email'] == email

        #DELETE
        response_delete = service.deletar_usuario(id_usuario=user_id)
        print(response_delete.json())
        validar_status(response_delete, 200)
        validar_mensagem_json(response_delete, 'Registro excluído com sucesso')
