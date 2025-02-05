# Servidor de Transferência de Mensagens com Fila de Prioridade

## Descrição:
Implemente um servidor de mensagens que permita que as mensagens sejam enviadas com diferentes níveis de prioridade. O servidor deve processar e entregar as mensagens com base na prioridade delas.

## Tecnologias Utilizadas:
- Python: Linguagem de programação utilizada para implementar o servidor e o cliente.
- Socket: Biblioteca padrão do Python utilizada para implementar a comunicação entre o servidor e o cliente.
- Threading: Biblioteca padrão do Python utilizada para implementar o servidor multithread.
- Queue: Biblioteca padrão do Python utilizada para implementar a fila de mensagens.
- Python-dotenv: Biblioteca utilizada para carregar as variáveis de ambiente a partir de um arquivo `.env`.
- Poetry: Gerenciador de dependências utilizado para instalar as dependências do projeto.


## Requisitos:
- Implementar um mecanismo para atribuir prioridades às mensagens (alta, média, baixa).
- O servidor deve processar as mensagens de alta prioridade antes das de média e baixa prioridade.
- Implementar um sistema de fila para armazenar e gerenciar as mensagens com suas respectivas prioridades.


# Instruções para instalação:
## Pré-requisitos:
- [Python](https://www.python.org/) 3.8 ou superior
- [Poetry](https://python-poetry.org/) (para instalar as dependências)

## Instalação:
1. Instale o Poetry:
```bash
pip install poetry
```

2. Clone o repositório:
```bash
git clone https://github.com/RenanCampista/Trab2-Redes
```

3. Dentro da pasta do projeto, instale as dependências:
```bash
poetry install
```

## Configuração:
Antes de executar o servidor, é necessário criar um arquivo `.env` para defirnir as variáveis de ambiente como mostrado no arquivo [.env.example](.env.example).

1. Copie o arquivo `.env.example`:
```bash
cp .env.example .env
```

2. Abrar o arquivo `.env` e defina as variáveis de ambiente:
```bash
SERVER_HOST= IP do servidor. Ex: "localhost"
SERVER_PORT= Porta do servidor. Ex: "8080"
```

## Execução:
Inicie o servidor:
```bash
poetry run server
```

Após iniciar o servidor, você pode enviar mensagens para ele utilizando o cliente:
```bash
poetry run client
```

O cliente, por sua vez, irá ler o conteúdo do arquivo [messages.txt](messages.txt) e enviar as mensagens para o servidor. A prioridade das mensagens é definido aleatoriamente.


## Funcionalidades implementadas:
- [x] Implementação do servidor de mensagens.
- [x] Implementação do cliente de mensagens.
- [x] Implementação da fila de prioridade.
- [x] Implementação do servidor multithread.
- [x] Implementação do sistema de leitura de mensagens.


## Possíveis Melhorias Futuras:
- [ ] Implementar um sistema de autenticação para o servidor.
- [ ] Implementar um sistema de criptografia para as mensagens.
- [ ] Implementar um sistema de logs para registrar as mensagens recebidas e enviadas.
- [ ] Implementar um sistema de notificação para informar o cliente sobre o status das mensagens.
- [ ] Implementar um sistema de armazenamento para salvar as mensagens recebidas em um banco de dados.