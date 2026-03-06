from playwright.sync_api import sync_playwright
from faker import Faker

fake = Faker()
nome = fake.name()
email = fake.email()
password = fake.password()
print(nome, email, password)

BASE_URL = 'https://serverest.dev/usuarios'

def test_crud_usuarios():
    with sync_playwright() as p:
        request_context = p.request.new_context()

        response_create = request_context.post(
            BASE_URL,
            data={'nome': nome,
                  'email': email,
                  'password': password,
                  'administrador': 'true'}
        )

        print(response_create.body())
        assert response_create.status == 201
        assert response_create.json()['message'] == 'Cadastro realizado com sucesso'
        user_id = response_create.json()['_id']

        response_read = request_context.get(f"{BASE_URL}/{user_id}")
        assert response_read.status == 200
        assert response_read.json()['_id'] == user_id
        assert response_read.json()['email'] == email
        
        response_update = request_context.put(
            f'{BASE_URL}/{user_id}',
            data={'nome': f'{nome} Update',
                  'email': email,
                  'password': password,
                  'administrador': 'true'}
        )

        assert response_update.status == 200
        assert response_update.json()['message'] == 'Registro alterado com sucesso'

        response_read = request_context.get(f'{BASE_URL}/{user_id}')
        assert response_read.status == 200
        assert response_read.json()['email'] == email

        response_delete = request_context.delete(f'{BASE_URL}/{user_id}')
        print(response_delete.body())
        assert response_delete.status == 200
        assert response_delete.json()['message'] == 'Registro excluído com sucesso'