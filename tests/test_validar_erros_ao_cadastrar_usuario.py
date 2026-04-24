from page_objects.usuarios import Usuarios
from helpers.validators import validar_status
from faker import Faker
import random

fake = Faker()
nome = fake.name()
email = fake.email()
password = fake.password()
administrador = random.choice(['true', 'false'])

def test_cadastro_usuario_sem_nome(api_context):
    service = Usuarios(api_context)

    response = service.criar_usuarios(nome='',
                                      email=email,
                                      password=password,
                                      administrador=administrador)
    
    validar_status(response, 400)
    print(response.json())

    assert response.json()['nome'] == 'nome não pode ficar em branco'

def test_cadastro_usuario_sem_email(api_context):
    service = Usuarios(api_context)

    response = service.criar_usuarios(nome=nome,
                                      email='',
                                      password=password,
                                      administrador=administrador)
    
    validar_status(response, 400)
    print(response.json())

    assert response.json()['email'] == 'email não pode ficar em branco'
    
def test_cadastro_usuario_sem_password(api_context):
    service = Usuarios(api_context)

    response = service.criar_usuarios(nome=nome,
                                      email=email,
                                      password='',
                                      administrador=administrador)
    
    validar_status(response, 400)
    print(response.json())

    assert response.json()['password'] == 'password não pode ficar em branco'

def test_cadastro_usuario_sem_administrador(api_context):
    service = Usuarios(api_context)

    response = service.criar_usuarios(nome=nome,
                                      email=email,
                                      password=password,
                                      administrador='')
    
    validar_status(response, 400)
    print(response.json())

    assert response.json()['administrador'] == "administrador deve ser 'true' ou 'false'"
