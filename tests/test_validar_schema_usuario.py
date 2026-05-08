from helpers.validators import validar_schema

def test_schema_usuario(usuario_servico):
    response = usuario_servico.listar_todos_usuarios()
    print(response.json())

    usuario_schema = {
        'type': 'object',
        'properties': {
            'quantidade': {'type': 'integer'},
            'usuarios': {'type': 'array',
                         'items': {'type': 'object',
                                   'properties': {'nome': {'type': 'string'},
                                                  'email': {'type': 'string'},
                                                  'password': {'type': 'string'},
                                                  'administrador': {'type': 'string'},
                                                  '_id': {'type': 'string'},
                                                  },
                                                  'required': ['nome', 'email', 'password', 'administrador', '_id']
                                }
                        }
        },
        'required': ['quantidade', 'usuarios'],
    }

    validar_schema(response, usuario_schema)
