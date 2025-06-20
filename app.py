from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from config.dispositivos import estado_dispositivos, temperaturas_ambientes
from controladores.controle_led import controla_led
from controladores.controle_porta import controla_porta
from controladores.ativar_alarme import ativar_alarme
import paho.mqtt.client as mqtt
import json
import gevent

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

client = mqtt.Client(transport="websockets")
client.ws_set_options(path="/")
broker = "test.mosquitto.org"
port = 8080

predios_temperatura = {f"predio{i}": None for i in range(1, 6)}
# Novo: temperaturas dos ambientes
ambientes = list(temperaturas_ambientes.keys())

def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker MQTT com código: {rc}")
    for comodo in estado_dispositivos.keys():
        client.subscribe(f"{comodo}/#")
    # Subscrever também aos tópicos de temperatura dos ambientes
    for ambiente in ambientes:
        client.subscribe(f"{ambiente}/temperatura")

def on_message(client, userdata, msg):
    try:
        topic_parts = msg.topic.split('/')
        # Temperatura de prédios (antigo)
        if len(topic_parts) == 2 and topic_parts[1] == 'temperatura' and topic_parts[0].startswith('predio'):
            predio = topic_parts[0]
            temperatura = msg.payload.decode()
            predios_temperatura[predio] = temperatura
            socketio.emit('temperatura_atualizada', {predio: temperatura})
            return
        # Temperatura de ambientes (novo)
        if len(topic_parts) == 2 and topic_parts[1] == 'temperatura' and topic_parts[0] in ambientes:
            ambiente = topic_parts[0]
            temperatura = float(msg.payload.decode())
            print(f"Recebido do MQTT: {ambiente} = {temperatura}")
            temperaturas_ambientes[ambiente] = temperatura
            socketio.emit('temperatura_ambiente_atualizada', {ambiente: temperatura})
            return
        comodo = topic_parts[0]
        dispositivo = topic_parts[1]
        mensagem = msg.payload.decode()
        if dispositivo == "PortaPrincipal":
            controla_porta(estado_dispositivos, comodo, mensagem)
        elif comodo == "Sistema de Alarme" and dispositivo == "Alarme":
            if mensagem.lower() == "ligar":
                ativar_alarme(estado_dispositivos)
        else:
            controla_led(estado_dispositivos, comodo, dispositivo, mensagem)
        socketio.emit('estado_atualizado', estado_dispositivos)
    except Exception as e:
        print(f"Erro ao processar mensagem MQTT: {e}")

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port)
gevent.spawn(client.loop_forever)

@app.route('/')
def index():
    return render_template('index.html', dispositivos=estado_dispositivos, temperaturas=predios_temperatura, temperaturas_ambientes=temperaturas_ambientes)

@app.route('/atualizar_led', methods=['POST'])
def atualizar_led():
    data = request.json
    comodo = data['comodo']
    dispositivo = data['dispositivo']
    acao = data['acao']
    topic = f"{comodo}/{dispositivo}"
    client.publish(topic, acao)
    controla_led(estado_dispositivos, comodo, dispositivo, acao)
    socketio.emit('estado_atualizado', estado_dispositivos)
    return jsonify(estado_dispositivos)

@app.route('/atualizar_porta', methods=['POST'])
def atualizar_porta():
    data = request.json
    comodo = data['comodo']
    dispositivo = data['dispositivo']
    acao = data['acao']
    topic = f"{comodo}/{dispositivo}"
    client.publish(topic, acao)
    controla_porta(estado_dispositivos, comodo, dispositivo, acao)
    socketio.emit('estado_atualizado', estado_dispositivos)
    return jsonify(estado_dispositivos)

@app.route('/ativar_alarme', methods=['POST'])
def ativar_alarme_endpoint():
    ativar_alarme(estado_dispositivos)
    socketio.emit('estado_atualizado', estado_dispositivos)
    return jsonify(estado_dispositivos)
    
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 