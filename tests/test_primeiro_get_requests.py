import requests

def test_listar_usuario():
    response = requests.get('https://serverest.dev/usuarios')
    assert response.status_code == 200

    data = response.json()
    assert 'usuarios' in data
    print(data)
    