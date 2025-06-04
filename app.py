from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from config.dispositivos import estado_dispositivos
from controladores.controle_led import controla_led
from controladores.controle_porta import controla_porta
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuração do cliente MQTT
client = mqtt.Client()
broker = "broker.emqx.io"
port = 1883

def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker MQTT com código: {rc}")
    # Inscreve-se nos tópicos de todos os prédios
    for predio in estado_dispositivos.keys():
        client.subscribe(f"{predio}/#")

def on_message(client, userdata, msg):
    try:
        # Extrai o prédio e o cômodo do tópico
        topic_parts = msg.topic.split('/')
        predio = topic_parts[0]
        comodo = topic_parts[1]
        mensagem = msg.payload.decode()
        
        # Atualiza o estado local
        if comodo == "PortaPrincipal":
            controla_porta(estado_dispositivos, predio, mensagem)
        else:
            controla_led(estado_dispositivos, predio, comodo, mensagem)
            
        # Emite evento WebSocket com o novo estado
        socketio.emit('estado_atualizado', estado_dispositivos)
            
    except Exception as e:
        print(f"Erro ao processar mensagem MQTT: {e}")

# Configura callbacks
client.on_connect = on_connect
client.on_message = on_message

# Conecta ao broker
client.connect(broker, port)
client.loop_start()

@app.route('/')
def index():
    return render_template('index.html', dispositivos=estado_dispositivos)

@app.route('/atualizar_led', methods=['POST'])
def atualizar_led():
    data = request.json
    predio = data['predio']
    comodo = data['comodo']
    acao = data['acao']
    
    # Publica no tópico MQTT
    topic = f"{predio}/{comodo}"
    client.publish(topic, acao)
    
    # Atualiza estado local
    controla_led(estado_dispositivos, predio, comodo, acao)
    
    # Emite evento WebSocket com o novo estado
    socketio.emit('estado_atualizado', estado_dispositivos)
    
    return jsonify(estado_dispositivos)

@app.route('/atualizar_porta', methods=['POST'])
def atualizar_porta():
    data = request.json
    predio = data['predio']
    acao = data['acao']
    
    # Publica no tópico MQTT
    topic = f"{predio}/PortaPrincipal"
    client.publish(topic, acao)
    
    # Atualiza estado local
    controla_porta(estado_dispositivos, predio, acao)
    
    # Emite evento WebSocket com o novo estado
    socketio.emit('estado_atualizado', estado_dispositivos)
    
    return jsonify(estado_dispositivos)

if __name__ == '__main__':
    socketio.run(app, debug=True) 