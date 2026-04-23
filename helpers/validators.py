def validar_status(response, status_esperado):
    assert response.status == status_esperado, (f'Status esperado: {status_esperado}, mas recebeu: {response.status}'
                                                f'\n{response.text()}')
    
def validar_mensagem_json(response, mensagem_esperada):
    body = response.json()
    assert body['message'] == mensagem_esperada, f'Esperado: {mensagem_esperada}, recebeu: {body['message']}'
