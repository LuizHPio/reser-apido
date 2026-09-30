# Reser-Apido 📅

## 📖 Sobre o Projeto

O **Reser-Apido** é um sistema de gerenciamento de reservas de salas e equipamentos desenvolvido no **3º semestre de Engenharia de Software** para a disciplina de **Programação Orientada a Objetos (OO)**.

Mais do que um simples CRUD, o principal objetivo deste projeto foi construir uma arquitetura robusta e escalável a partir do zero, aplicando princípios sólidos de engenharia de software e design de classes, sem depender de frameworks "mágicos" que escondem a complexidade.

## 🔐 Destaque Arquitetural: Segurança e Autenticação

Um dos pilares deste projeto é a sua camada de segurança, implementada sob medida para garantir a integridade das sessões e proteger os dados dos usuários contra interceptações e manipulações.

A arquitetura de autenticação opera em três frentes principais:

- **Hashing de Senhas (Bcrypt):** Nenhuma senha é armazenada em texto plano. O sistema utiliza a biblioteca `bcrypt` com _salt_ dinâmico para hashear as credenciais no momento do registro (`Registration.register_user`). Isso mitiga ataques de força bruta e _rainbow tables_.
- **Sessões Criptografadas (Fernet):** Em vez de depender do gerenciamento de sessão padrão em memória do Bottle, o Reser-Apido implementa tokens baseados em criptografia simétrica utilizando a biblioteca `cryptography` (Fernet). A chave secreta (`SECRET_KEY`) injetada via `.env` garante que os _cookies_ ou _tokens_ de sessão assinados pelo servidor não possam ser forjados ou lidos pelo cliente.
- **Controle de Acesso Desacoplado:** A verificação de identidade é extraída da lógica de roteamento. Controladores como `Auth.verify_authentication(request, response)` e `Auth.get_token_pair(request)` atuam como _middlewares_ rigorosos, barrando o acesso a endpoints privados ou de administração antes mesmo da renderização da view.

## Outros Diferenciais Técnicos

- **Padrão MVC Customizado:** Construído sobre o micro-framework minimalista Bottle. O roteamento, as regras de negócio e a persistência de dados (`db/models`) foram isolados estruturalmente para garantir alto desacoplamento e facilitar injeções de dependências.
- **Comunicação Bidirecional em Tempo Real:** Implementação nativa de WebSockets (`python-socketio` + `eventlet`) para refletir mudanças de estado instantaneamente. A manipulação de eventos de reserva ocorre via processamento assíncrono, atualizando a interface de todos os clientes conectados sem recarregamento da página.
- **Developer Experience (DX) e Containerização:** Infraestrutura projetada para reprodutibilidade e isolamento. O repositório conta com containers Docker e scripts em Bash (`bmvc_setup.sh`, `develop.sh`) que automatizam o provisionamento do ambiente, o tratamento de portas e o _hot-reloading_.

## 🛠️ Stack Tecnológica Base

- **Linguagem:** Python 3
- **Framework Web:** Bottle
- **Comunicação:** WebSockets
- **Segurança:** Criptografia via Fernet (`cryptography`)
- **Banco de Dados:** SQLite (arquivo local `reserve.db`)
- **Infraestrutura:** Docker & Bash Scripts
- **Frontend:** Templates nativos (`.tpl`), HTML5, CSS3, JavaScript puro.

## 🚀 Como Rodar o Código

### Passos Prévios: Ambiente e Banco de Dados

Antes de rodar a aplicação, é necessário configurar as chaves de segurança e inicializar o banco.

**1. Configurar a Chave Secreta (.env)**
O sistema utiliza Fernet para gerenciar tokens/sessões de forma segura. Gere uma chave secreta e a guarde em um arquivo .env no terminal:

```bash
python -c "import base64, os; print('SECRET_KEY=' + base64.urlsafe_b64encode(os.urandom(32)).decode())" > .env
```

---

### Iniciando a Aplicação

**Opção A: A forma mais rápida (Com Docker)**
Recomendamos o uso do Docker para não poluir sua máquina com dependências locais:

```bash
# 1. Instale o docker caso não tenha (OPCIONAL)
chmod +x docker_install.sh
./docker_install.sh

# 2. Inicie o container
./start_docker.sh
```

**Opção B: O método manual (Python Local)**
Caso prefira rodar usando o ambiente Python nativo:

```bash
# 1. Crie e ative um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Inicialize o banco de dados
python -m app.controllers.db.init_db

# 4. Inicie a aplicação.
./develop.sh # ou rode 'python route.py' diretamente
```

Acesse `http://localhost:3000` no seu navegador para utilizar o sistema.
