# Sistema de Controle IoT

Este projeto implementa um sistema de controle IoT para gerenciar dispositivos (LEDs e portas) em múltiplos prédios através de uma interface web e comunicação MQTT.

## Funcionalidades

- Controle de LEDs e portas em 5 prédios diferentes
- Interface web responsiva com atualizações em tempo real
- Comunicação bidirecional via MQTT
- Feedback visual do estado dos dispositivos
- Suporte a múltiplos cômodos por prédio (Sala, Cozinha, Quarto, Garagem)
- Controle da porta principal de cada prédio

## Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conexão com a internet (para acesso ao broker MQTT)

## Dependências

O projeto utiliza as seguintes bibliotecas Python:
- Flask 3.0.0
- paho-mqtt 1.6.1
- flask-socketio
- python-socketio

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITÓRIO]
cd IOTTrabalho2
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Execução

O projeto requer dois componentes em execução simultânea:

1. Servidor Web (Interface):
```bash
python app.py
```
A interface web estará disponível em: http://localhost:5000

2. Cliente MQTT (em outro terminal):
```bash
python main.py
```

## Estrutura do Projeto

```
IOTTrabalho2/
├── app.py              # Servidor web e WebSocket
├── main.py             # Cliente MQTT
├── requirements.txt    # Dependências do projeto
├── config/            # Configurações
│   ├── dispositivos.py # Estado dos dispositivos
│   └── topicos.py     # Tópicos MQTT
├── controladores/     # Lógica de controle
│   ├── controle_led.py
│   └── controle_porta.py
├── templates/         # Interface web
│   └── index.html
└── utils/            # Utilitários
    └── estado.py
```

## Uso

### Interface Web
1. Acesse http://localhost:5000
2. Selecione o prédio desejado
3. Use os botões para controlar os dispositivos:
   - LEDs: Ligar/Desligar
   - Porta Principal: Abrir/Fechar

### Comunicação MQTT
O sistema utiliza o broker público broker.emqx.io na porta 1883.

Tópicos MQTT:
- Formato: `predioX/Comodo`
- Exemplo: `predio1/Sala`, `predio2/PortaPrincipal`

Mensagens:
- LEDs: "ligar" ou "desligar"
- Porta: "abrir" ou "fechar"

## Testando o Sistema

1. Inicie o servidor web e o cliente MQTT conforme instruções acima
2. Acesse a interface web
3. Teste o controle dos dispositivos pela interface
4. Use um cliente MQTT (como MQTT Explorer) para enviar mensagens diretamente
5. Verifique as atualizações em tempo real na interface web

## Solução de Problemas

1. Se a interface web não carregar:
   - Verifique se o servidor web está rodando
   - Confirme se a porta 5000 está disponível

2. Se não houver atualizações em tempo real:
   - Verifique se o cliente MQTT está rodando
   - Confirme a conexão com o broker MQTT

3. Se os dispositivos não responderem:
   - Verifique os logs do terminal
   - Confirme se as mensagens MQTT estão sendo enviadas corretamente






