# Curso API Playwright

Projeto educacional de testes automatizados de API utilizando **Playwright** e **Pytest**. Este repositório contém exemplos práticos de como testar uma API RESTful usando a biblioteca Playwright com foco em boas práticas de automação e validação de dados.

## 🎯 Objetivo

Demonstrar como criar testes automatizados para APIs RESTful de forma organizada, mantível e escalável, utilizando:
- **Playwright**: Para requisições HTTP síncronas
- **Pytest**: Como framework de testes
- **Page Objects**: Para organização e reutilização de código
- **Validação de Schema**: Para garantir conformidade com contratos de API
- **Fixtures**: Para setup compartilhado entre testes

## 🛠️ Tecnologias Utilizadas

| Dependência | Versão | Descrição |
|---|---|---|
| **Python** | 3.x | Linguagem de programação |
| **Playwright** | 1.58.0 | Biblioteca para automação e testes |
| **Pytest** | 9.0.2 | Framework de testes |
| **pytest-playwright** | 0.7.2 | Plugin Pytest para Playwright |
| **Requests** | 2.32.5 | Biblioteca HTTP (alternativa) |
| **Faker** | Latest | Geração de dados fake para testes |
| **jsonschema** | Latest | Validação de schemas JSON |
| **pytest-html** | Latest | Relatórios HTML |
| **allure-pytest** | Latest | Relatórios Allure |
| **pytest-xdist** | Latest | Execução paralela de testes |

## 📁 Estrutura do Projeto

```
curso-api-playwright/
├── README.md                      # Este arquivo
├── conftest.py                    # Configurações e fixtures globais
├── pytest.ini                     # Configuração do Pytest
├── requirements.txt               # Dependências do projeto
│
├── page_objects/                  # Padrão Page Object Model
│   ├── __pycache__/
│   └── usuarios.py               # Serviço para endpoint de usuários
│
├── helpers/                       # Funções auxiliares e utilitários
│   ├── __pycache__/
│   └── validators.py             # Funções de validação comuns
│
├── tests/                        # Suite de testes
│   ├── __pycache__/
│   ├── test_crud_usuarios.py
│   ├── test_crud_usuarios_v1.py
│   ├── test_crud_usuarios_requests.py
│   ├── test_login.py
│   ├── test_primeiro_get.py
│   ├── test_primeiro_get_requests.py
│   ├── test_cadastrar_produto.py
│   ├── test_cadastrar_usuarios.py
│   ├── test_respostas.py
│   ├── test_validar_erros_ao_cadastrar_usuario.py
│   └── test_validar_schema_usuario.py
│
├── data/                         # Dados de teste (fixtures, massa de dados)
│   └── test_cadastrar_usuarios/
│
├── allure-results/               # Resultados de testes (Allure)
├── report.html                   # Relatório HTML de testes
└── relatorio.txt                 # Relatório em texto
```

## 🚀 Como Começar

### Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Git (opcional)

### Instalação

1. **Clone o repositório** (se aplicável):
```bash
git clone https://github.com/seu-usuario/curso-api-playwright.git
cd curso-api-playwright
```

2. **Crie um ambiente virtual**:
```bash
# Linux/macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

4. **Instale os navegadores do Playwright** (necessário para execução):
```bash
playwright install
```

## 📝 Executando os Testes

### Executar todos os testes:
```bash
pytest
```

### Executar testes com saída verbosa:
```bash
pytest -v -s
```

### Executar um arquivo de teste específico:
```bash
pytest tests/test_crud_usuarios.py
```

### Executar um teste específico:
```bash
pytest tests/test_crud_usuarios.py::test_crud_usuarios
```

### Executar testes em paralelo (usando pytest-xdist):
```bash
pytest -n auto
```

### Gerar relatório HTML:
```bash
pytest --html=report.html --self-contained-html
```

### Gerar relatório Allure:
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

## 🏗️ Arquitetura e Padrões

### 1. **Page Object Model (POM)**
Encapsula a lógica de interação com a API em classes específicas:

```python
# page_objects/usuarios.py
class Usuarios:
    def __init__(self, api_context):
        self.api_context = api_context
    
    def criar_usuarios(self, nome, email, password, administrador):
        return self.api_context.post(self.endpoint, data={...})
```

### 2. **Fixtures Compartilhadas**
O arquivo `conftest.py` define fixtures reutilizáveis:

#### `api_context` (scope='session')
Cria um contexto de requisições HTTP com configuração padrão:
- Base URL: `https://serverest.dev`
- Reutilizado em toda a sessão de testes

#### `token` (scope='session')
Obtém um token de autenticação válido:
- Verifica se usuário de teste existe
- Cria usuário se necessário
- Realiza login e retorna token Bearer

#### `usuario_servico`
Instância do serviço de usuários com contexto de API

### 3. **Validadores Reutilizáveis**
Funções no `helpers/validators.py` para validações comuns:

```python
def validar_status(response, status_esperado):
    """Valida o status HTTP da resposta"""
    
def validar_mensagem_json(response, mensagem_esperada):
    """Valida mensagem JSON na resposta"""
    
def validar_schema(response, schema):
    """Valida a resposta contra um schema JSON"""
```

## 📚 Exemplos de Uso

### Exemplo 1: Teste CRUD Simples
```python
def test_crud_usuarios(api_context):
    service = Usuarios(api_context=api_context)
    
    # CREATE
    response = service.criar_usuarios(
        nome="João Silva",
        email="joao@email.com",
        password="senha123",
        administrador="true"
    )
    validar_status(response, 201)
    user_id = response.json()['_id']
    
    # READ
    response = service.listar_usuario(user_id)
    validar_status(response, 200)
    assert response.json()['email'] == "joao@email.com"
```

### Exemplo 2: Teste com Dados Fake
```python
from faker import Faker

fake = Faker()

def test_com_dados_fake(api_context):
    service = Usuarios(api_context=api_context)
    
    response = service.criar_usuarios(
        nome=fake.name(),
        email=fake.email(),
        password=fake.password(),
        administrador="true"
    )
    validar_status(response, 201)
```

### Exemplo 3: Teste com Validação de Schema
```python
from jsonschema import validate

usuario_schema = {
    "type": "object",
    "properties": {
        "_id": {"type": "string"},
        "nome": {"type": "string"},
        "email": {"type": "string"}
    }
}

def test_validar_schema(api_context):
    service = Usuarios(api_context=api_context)
    response = service.listar_todos_usuarios()
    validar_status(response, 200)
    validar_schema(response, usuario_schema)
```

## 🔐 Credenciais de Teste

O projeto utiliza as seguintes credenciais para testes:
- **Email**: `teste_patrick@email.com`
- **Senha**: `123456`

> ⚠️ **Importante**: Não use credenciais reais em testes. Estas credenciais são apenas para fins de demonstração.

## 📊 Relatórios

O projeto gera múltiplos tipos de relatórios:

1. **HTML Report** (`report.html`): Relatório interativo em HTML
2. **Allure Report**: Relatórios visuais com análise detalhada
3. **Text Report** (`relatorio.txt`): Saída em texto simples

## 🧪 Testes Disponíveis

| Arquivo | Descrição |
|---|---|
| `test_crud_usuarios.py` | CRUD completo com validações |
| `test_login.py` | Testes de autenticação |
| `test_primeiro_get.py` | Teste GET básico com Playwright |
| `test_primeiro_get_requests.py` | Teste GET básico com Requests |
| `test_cadastrar_usuarios.py` | Testes de cadastro |
| `test_validar_schema_usuario.py` | Validação de esquema JSON |
| `test_validar_erros_ao_cadastrar_usuario.py` | Testes de validação de erros |
| `test_respostas.py` | Análise de respostas |
| `test_cadastrar_produto.py` | Testes de cadastro de produtos |

## 🔧 Configuração do Pytest

O arquivo `pytest.ini` define:
```ini
[pytest]
addopts = -v -s
testpaths = tests
```

- `-v`: Modo verboso (exibe nome de cada teste)
- `-s`: Mostra saída padrão (print statements)
- `testpaths`: Diretório onde os testes são procurados

## 📖 API Testada

Este projeto testa a API **ServeRest**, uma API pública REST de exemplo disponível em: https://serverest.dev

Endpoints principais:
- `POST /login` - Autenticação
- `GET/POST /usuarios` - Gerenciamento de usuários
- `GET/PUT/DELETE /usuarios/{id}` - Usuários específicos
- `GET/POST /produtos` - Gerenciamento de produtos

## 💡 Dicas e Boas Práticas

1. **Use fixtures** para setup e teardown compartilhado
2. **Prefira Page Objects** para encapsular lógica de API
3. **Valide schemas** para garantir conformidade com contrato da API
4. **Use dados fake** para testes isolados e independentes
5. **Execute testes em paralelo** para melhor performance
6. **Crie relatórios** para análise de resultados
7. **Mantenha credenciais em variáveis de ambiente** (não em código)

## 📋 Exemplo de Estrutura de Teste

```python
import pytest
from page_objects.usuarios import Usuarios
from helpers.validators import validar_status, validar_mensagem_json

class TestUsuarios:
    """Suite de testes para o endpoint de usuários"""
    
    def test_criar_usuario(self, usuario_servico):
        """Teste para criação de usuário"""
        # Arrange
        dados = {
            'nome': 'João Silva',
            'email': 'joao@test.com',
            'password': '123456',
            'administrador': 'true'
        }
        
        # Act
        response = usuario_servico.criar_usuarios(**dados)
        
        # Assert
        validar_status(response, 201)
        validar_mensagem_json(response, 'Cadastro realizado com sucesso')
```

## 🐛 Resolução de Problemas

### Erro: "No module named 'playwright'"
Solução: Execute `pip install -r requirements.txt`

### Erro: "Browsers not found"
Solução: Execute `playwright install`

### Testes lentos
Solução: Use `pytest -n auto` para execução paralela

### Erro de conexão com API
Solução: Verifique conexão com internet e acesso a https://serverest.dev

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação do [Playwright](https://playwright.dev/python/)
2. Consulte a documentação do [Pytest](https://docs.pytest.org/)
3. Abra uma issue no repositório

## 📄 Licença

Este projeto é de código aberto e está disponível sob a Licença MIT.

## 🙌 Contribuições

Contribuições são bem-vindas! Sinta-se livre para:
- Abrir issues
- Enviar pull requests
- Sugerir melhorias

---

**Desenvolvido para fins educacionais** | Curso API com Playwright
