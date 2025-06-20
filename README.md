# Sistema de Controle IoT

Este projeto implementa um sistema de controle IoT para gerenciar dispositivos (LEDs, portas, ar-condicionado, etc.) em múltiplos cômodos através de uma interface web e comunicação MQTT.

## Funcionalidades

- Controle de LEDs, portas, ar-condicionado e outros dispositivos em diferentes cômodos
- Interface web responsiva com atualizações em tempo real
- Comunicação bidirecional via MQTT
- Feedback visual do estado dos dispositivos
- Simulação de temperatura por ambiente e por prédio
- Controle do ar-condicionado do Quarto, afetando a temperatura
- Teste automatizado do sensor de temperatura

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

O projeto possui três componentes principais que podem ser executados em terminais separados:

1. **Simulador de Temperatura dos Ambientes (ar-condicionado/quarto):**
```bash
python simulador_sensor.py
```
> Sempre inicie este simulador antes do servidor web para garantir que ele receba os comandos MQTT corretamente.

2. **Servidor Web (Interface):**
```bash
python app.py
```
A interface web estará disponível em: http://localhost:5000

3. **Simulador de Temperatura dos Prédios:**
```bash
python main.py
```

### Teste Automatizado do Sensor de Temperatura
Para testar automaticamente o comportamento do ar-condicionado do Quarto:
```bash
python teste_sensor_temperatura.py
```
O teste verifica se a temperatura do Quarto cai ao ligar o ar-condicionado e sobe ao desligar.

## Estrutura do Projeto

```
IOTTrabalho2/
├── app.py                    # Servidor web e WebSocket
├── main.py                   # Simulador de temperatura dos prédios
├── simulador_sensor.py       # Simulador de temperatura dos ambientes e ar-condicionado
├── teste_sensor_temperatura.py # Teste automatizado do sensor de temperatura
├── requirements.txt          # Dependências do projeto
├── config/                   # Configurações
│   ├── dispositivos.py       # Estado dos dispositivos e temperaturas
│   └── topicos.py            # Tópicos MQTT
├── controladores/            # Lógica de controle
│   ├── controle_led.py
│   ├── controle_porta.py
│   └── ativar_alarme.py
├── templates/                # Interface web
│   └── index.html
└── utils/                    # Utilitários
    └── estado.py
```

## Uso

### Interface Web
1. Acesse http://localhost:5000
2. Visualize e controle os dispositivos de cada cômodo:
   - LEDs: Ligar/Desligar
   - Porta Principal, Portão, Janelas, Cortinas: Abrir/Fechar
   - Ar Condicionado do Quarto: Ligar/Desligar (afeta a temperatura do Quarto)
3. As temperaturas dos ambientes são exibidas em tempo real na interface.

### Comunicação MQTT
O sistema utiliza o broker público **test.mosquitto.org** na porta **8080** (WebSockets).

#### Tópicos MQTT
- **Dispositivos dos ambientes:**
  - Formato: `<Comodo>/<Dispositivo>`
  - Exemplos: `Quarto/Ar Condicionado`, `Sala/Luz`, `Garagem/PortaPrincipal`
  - Mensagens: "ligar", "desligar", "abrir", "fechar"
- **Temperatura dos ambientes:**
  - Formato: `<Comodo>/temperatura`
  - Exemplo: `Quarto/temperatura`
  - Publicado pelo simulador_sensor.py
- **Temperatura dos prédios:**
  - Formato: `predioX/temperatura` (X = 1 a 5)
  - Exemplo: `predio1/temperatura`
  - Publicado pelo main.py

## Solução de Problemas

1. Se a interface web não carregar:
   - Verifique se o servidor web está rodando
   - Confirme se a porta 5000 está disponível

2. Se não houver atualizações em tempo real:
   - Verifique se o simulador_sensor.py está rodando
   - Confirme a conexão com o broker MQTT

3. Se os dispositivos não responderem:
   - Verifique os logs do terminal
   - Confirme se as mensagens MQTT estão sendo enviadas corretamente

4. Se o teste automatizado não funcionar:
   - Certifique-se de que o simulador_sensor.py está rodando antes do teste

## Observações
- Sempre inicie o `simulador_sensor.py` antes do `app.py` para garantir o funcionamento correto dos comandos MQTT.
- O sistema foi desenvolvido para fins didáticos e pode ser adaptado para outros cenários de automação residencial.






