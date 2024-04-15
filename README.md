# Registro de agendamento de serviços para Petshop - API

Esta API (Application Programming Interface) é um MVP para registro de agendamento de serviços para um petshop.
Tem como objetivo validar os conteúdos passados nas disciplinas da sprint de Desenvolvimento Full-Stack Básico da pós-graduação em Engenharia de Software, pela PUC-Rio.

# Requisitos

- A API deverá ser implementada em Python e com Flask com pelo menos 3 rotas (por exemplo, “/cadastrar_usuario”, “/buscar_usuario” e “/deletar_usuario”), sendo que pelo menos uma delas deve implementar o método POST (por exemplo, na rota de cadastro).
- Fazer o uso de um banco de dados SQLite, PostgreSQL ou MySQL com pelo menos uma tabela (por exemplo, tabela de usuários cadastrados).
- Qualidade da Documentação da API em Swagger.
- Criatividade e Inovação.

# Funcionalidades

- Listagem de serviços ativos na base;
- Listagem de serviços agendados por período de datas;
- Criação de registro de agendamentos de serviços para clientes;
- Cancelamento de agendamento por ID;
- Exclusão de agendamento por ID;

# Tecnologias

- Python 3.11.8;
- SQLite (Persistencia em banco de dados);
- Flask;
- SQLALchemy;
- Dados retornados no formato JSON;
- Documentação da API no padrao Swagger.

# Como executar

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

Este comando criar o ambiente virtual para o projeto:

```
py -3 -m venv .venv
```

Este comando ativa o ambiente virtual para o terminal:

```
.\.venv\Scripts\activate
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`:

```
pip install -r requirements.txt
```

Para executar a API  basta executar:

```
flask --app .\app\app.py  run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
flask --app .\app\app.py  run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/api/](http://localhost:5000/api) no navegador para verificar o status da API em execução.
