from http.client import responses
from playwright.sync_api import sync_playwright

def test_listar_usuario():
    with sync_playwright() as p:
        request_context = p.request.new_context()

        response = request_context.get('https://serverest.dev/usuarios')

        assert response.status == 200

        data = response.json()
        assert "usuarios" in data
        print(data)
