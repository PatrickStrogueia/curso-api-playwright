import requests
from faker import Faker

fake = Faker()
nome = fake.name()
email = fake.email()
password = fake.password()
print(nome, email, password)

BASE_URL = 'https://serverest.dev/usuarios'

def test_crud_usuarios():

    response_create = requests.post(
        BASE_URL,
        data={'nome': nome,
                'email': email,
                'password': password,
                'administrador': 'true'}
    )

    print(response_create.text)
    assert response_create.status_code == 201
    assert response_create.json()['message'] == 'Cadastro realizado com sucesso'
    user_id = response_create.json()['_id']

    response_read = requests.get(f"{BASE_URL}/{user_id}")
    assert response_read.status_code == 200
    assert response_read.json()['_id'] == user_id
    assert response_read.json()['email'] == email
    
    response_update = requests.put(
        f'{BASE_URL}/{user_id}',
        data={'nome': f'{nome} Update',
                'email': email,
                'password': password,
                'administrador': 'true'}
    )

    assert response_update.status_code == 200
    assert response_update.json()['message'] == 'Registro alterado com sucesso'

    response_read = requests.get(f'{BASE_URL}/{user_id}')
    assert response_read.status_code == 200
    assert response_read.json()['email'] == email

    response_delete = requests.delete(f'{BASE_URL}/{user_id}')
    print(response_delete.text)
    assert response_delete.status_code == 200
    assert response_delete.json()['message'] == 'Registro excluído com sucesso'
    