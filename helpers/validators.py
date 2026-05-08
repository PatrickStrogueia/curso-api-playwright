from jsonschema import validate, ValidationError

def validar_status(response, status_esperado):
    assert response.status == status_esperado, (f'Status esperado: {status_esperado}, mas recebeu: {response.status}'
                                                f'\n{response.text()}')
    
def validar_mensagem_json(response, mensagem_esperada):
    body = response.json()
    assert body['message'] == mensagem_esperada, f'Esperado: {mensagem_esperada}, recebeu: {body['message']}'

def validar_schema(response, schema):
    body = response.json()

    try:
        validate(instance=body, schema=schema)
    except ValidationError as e:
        assert False, (f'Validação de schema falhou: {e.message}\n'
                       f'Corpo: {body}')
        