Projeto MVP - Agenda Fácil Naf

Desenvolvedores : Alexandre de Oliveira Silveira 06007233 // Tatiana Claussen Correa Beigelman 06006978 // Giovana de Araujo Machado 06007320
                  
## Sobre o Projeto

Este projeto visa desenvolver uma aplicação para gestão de agendas do Núcleo de Apoio Fiscal (NAF) da Universidade do Feso (Unifeso). A aplicação permite que administradores e usuários comuns possam criar, editar e gerenciar suas agendas de maneira eficiente.

## Tecnologias Utilizadas

### Front-End

- *HTML 5*: Utilizado para estruturar as páginas web de maneira semântica e acessível.
- *CSS 3*: Utilizado para estilizar e melhorar a aparência das páginas web.
- *JavaScript*: Utilizado para adicionar interatividade às páginas web.

### Back-End

- *FastAPI*: Framework utilizado para desenvolver a API RESTful de maneira rápida e eficiente.
- *SQLAlchemy*: Biblioteca ORM utilizada para fazer a conexão e manipulação do banco de dados.
- *SQLite*: Banco de dados utilizado para armazenar as informações da aplicação.
- *JWT (JSON Web Tokens)*: Utilizado para autenticação e autorização dos usuários.
- *Pydantic*: Utilizado para validação de dados e criação de modelos.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

- **back_end**: Contém todo o código relacionado ao back-end da aplicação.
  - **models**: Contém os modelos de dados para as tabelas do banco de dados.
  - **route**: Contém as rotas da API.
  - **dtos**: Contém os Data Transfer Objects (DTOs) utilizados na aplicação.
  - **utils**: Contém utilitários e funções auxiliares.
  - **create_db.py**: Script para criação e configuração do banco de dados.
  - **app.py**: Arquivo principal que inicia a aplicação FastAPI.

## Como Executar o Projeto

### Pré-requisitos

- Python 3.7 ou superior
- Pip (gerenciador de pacotes do Python)
- Virtualenv (opcional, mas recomendado)

### Passo a Passo

1. Clone o repositório:
   git clone https://github.com/Aosil803/AgendaFacil_NAF_Unifeso
   cd seu_repositorio
   
2. Crie um ambiente virtual e ative-o:
   python -m venv venv
   source venv/bin/activate  # No Windows use venv\Scripts\activate
   
3. Instale as dependências:
   pip install -r requirements.txt

4. Execute a aplicação:
   uvicorn back_end.app:app --reload

5. Acesse a aplicação no navegador:
   http://127.0.0.1:8000

