"""
Configurações globais de fixtures para testes de API com Playwright.

Este módulo contém fixtures compartilhadas entre todos os testes,
incluindo o contexto de API e autenticação com token.
"""

import pytest
from playwright.sync_api import sync_playwright

# Credenciais de teste utilizadas para autenticação na API
EMAIL_TESTE = 'teste_patrick@email.com'
SENHA_TESTE = '123456'

@pytest.fixture(scope='session')
def api_context():
    """
    Fixture que cria e gerencia o contexto de requisições da API do Playwright.
    
    Esta fixture é executada uma única vez por sessão de testes (scope='session'),
    criando um contexto reutilizável para todas as requisições HTTP.
    
    Yields:
        APIRequestContext: Contexto configurado para fazer requisições à API do ServeRest.
        
    Configurações:
        - base_url: URL base da API (https://serverest.dev)
        - ignore_https_errors: Ignora erros de certificados SSL
    """
    with sync_playwright() as p:
        # Cria um novo contexto de requisição com configurações específicas
        request_context = p.request.new_context(
            base_url='https://serverest.dev',
            ignore_https_errors=True
        )

        # Disponibiliza o contexto para os testes
        yield request_context

        # Limpa os recursos após todos os testes
        request_context.dispose()

@pytest.fixture(scope='session')
def token(api_context):
    """
    Fixture que obtém um token de autenticação válido para testes.
    
    Esta fixture verifica se o usuário de teste já existe no sistema.
    Caso não exista, cria um novo usuário administrador e, em seguida,
    realiza o login para obter o token de autorização.
    
    Args:
        api_context: Contexto de API fornecido pela fixture api_context.
        
    Returns:
        str: Token de autorização no formato Bearer para uso nos testes.
        
    Fluxo:
        1. Busca todos os usuários cadastrados
        2. Verifica se o usuário de teste já existe
        3. Se não existir, cria o usuário
        4. Realiza login e retorna o token de autenticação
    """
    # Busca todos os usuários cadastrados na API
    response_usuario = api_context.get('/usuarios')

    usuario = response_usuario.json()['usuarios']

    # Verifica se o usuário de teste já existe no sistema
    if any(u['email'] == EMAIL_TESTE for u in usuario):
        print('Usuário já existe.')
    else:
        # Usuário não existe, cria um novo usuário administrador
        print('Usuário não existe. Criando usuário.')
        response_create = api_context.post('/usuarios', 
                                           data={'nome': 'Teste Patrick',
                                                 'email': EMAIL_TESTE,
                                                 'password': SENHA_TESTE,
                                                 'administrador': 'true'})
        # Valida que o usuário foi criado com sucesso
        assert response_create.status == 201
        
    # Realiza login para obter o token de autenticação
    print('Login realizado.')
    response_login = api_context.post('/login', data={'email': EMAIL_TESTE,
                                                      'password': SENHA_TESTE})
    
    # Valida que o login foi bem-sucedido
    assert response_login.status == 200
    assert response_login.json()['message'] == 'Login realizado com sucesso'

    # Extrai o token de autorização da resposta
    token_str = response_login.json()['authorization']
    print(f'Login realizado com sucesso: {token_str}')
    
    return token_str
