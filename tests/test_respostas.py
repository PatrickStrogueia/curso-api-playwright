from playwright.sync_api import sync_playwright

def teste_resposta_detalhada():
    with sync_playwright() as p:
        request_context = p.request.new_context()

        response = request_context.get('https://serverest.dev/usuarios')

        assert response.status == 200
        assert response.ok

        headers = response.headers
        assert 'application/json; charset=utf-8' in headers['content-type']
        print(headers)

        body = response.json()
        assert isinstance(body['usuarios'], list)
        assert isinstance(body['quantidade'], int)
        print(body)
