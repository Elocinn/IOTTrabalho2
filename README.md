# Sistema de Controle IoT

Este projeto implementa um sistema de controle IoT para gerenciar dispositivos (luzes e portas) em múltiplos prédios através de uma interface web em tempo real.

## Funcionalidades

- Controle de luzes e portas em 5 prédios diferentes
- Interface web responsiva e atualização em tempo real
- Integração com MQTT para comunicação com dispositivos IoT
- Atualizações automáticas via WebSocket
- Suporte a múltiplos cômodos por prédio:
  - Sala
  - Cozinha
  - Quarto
  - Garagem
  - Porta Principal

## Requisitos

- Python 3.8+
- Flask
- Flask-SocketIO
- Paho-MQTT
- Python-SocketIO

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd IOTTrabalho2
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Executando o Projeto

1. Inicie o servidor:
```bash
python app.py
```

2. Acesse a interface web:
- Abra http://localhost:5000 no seu navegador

## Estrutura do Projeto

```
IOTTrabalho2/
├── app.py              # Aplicação principal Flask
├── main.py            # Ponto de entrada alternativo
├── requirements.txt   # Dependências do projeto
├── config/           # Configurações
│   ├── dispositivos.py
│   └── topicos.py
├── controladores/    # Lógica de controle
│   ├── controle_led.py
│   └── controle_porta.py
├── templates/        # Templates HTML
│   └── index.html
└── utils/           # Utilitários
```

## Uso

### Interface Web

A interface web permite:
- Visualizar o estado atual de todos os dispositivos
- Ligar/desligar luzes
- Abrir/fechar portas
- Ver atualizações em tempo real

### MQTT

O sistema usa o broker MQTT público (broker.emqx.io) para comunicação.

Tópicos MQTT:
- Formato: `{predio}/{comodo}`
- Exemplo: `predio1/Sala`

Mensagens:
- Luzes: "ligar" ou "desligar"
- Portas: "abrir" ou "fechar"

### WebSocket

O sistema implementa WebSocket para atualizações em tempo real:
- Atualizações automáticas quando o estado muda
- Sem necessidade de recarregar a página
- Comunicação bidirecional entre servidor e cliente

## Exemplos de Mensagens MQTT

```
# Ligar luz da sala do prédio 1
predio1/Sala -> "ligar"

# Desligar luz da cozinha do prédio 2
predio2/Cozinha -> "desligar"

# Abrir porta do prédio 3
predio3/PortaPrincipal -> "abrir"

# Fechar porta do prédio 4
predio4/PortaPrincipal -> "fechar"
```




