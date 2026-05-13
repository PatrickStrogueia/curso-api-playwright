import pytest, random, json
from helpers.validators import validar_status
from faker import Faker

fake = Faker()
nome = fake.name()
email = fake.email()
password = fake.password()
adminstrador = random.choice(["true", "false"])
print(nome, email, password, adminstrador)

@pytest.mark.parametrize(
    'nome, email, password, administrador, status_esperado',
    [
        (nome, email, password, adminstrador, 201),
        ('', email, password, adminstrador, 400),
        (nome, '', password, adminstrador, 400),
        (nome, email, '', adminstrador, 400),
        (nome, email, password, '', 400)
    ]
)
def test_cadastrar_usuarios(usuario_servico, nome, email, password, administrador, status_esperado):
    response = usuario_servico.criar_usuarios(
        nome=nome,
        email=email,
        password=password,
        administrador=administrador
    )
    validar_status(response, status_esperado)

def carregar_dados_json():
    with open('data/test_cadastrar_usuarios/usuario.json', encoding='utf-8') as json_file:
        return json.load(json_file)

@pytest.mark.parametrize("dados", carregar_dados_json())
def test_cadastrar_usuarios1(usuario_servico, dados):
    response = usuario_servico.criar_usuarios(
        nome=dados['nome'],
        email=dados['email'],
        password=dados['password'],
        administrador=dados['administrador']
    )
    validar_status(response, dados['esperado'])
    