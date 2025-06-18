from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from config.dispositivos import estado_dispositivos
from controladores.controle_led import controla_led
from controladores.controle_porta import controla_porta
from controladores.ativar_alarme import ativar_alarme
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

client = mqtt.Client()
broker = "broker.emqx.io"
port = 1883

def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker MQTT com código: {rc}")
    for comodo in estado_dispositivos.keys():
        client.subscribe(f"{comodo}/#")

def on_message(client, userdata, msg):
    try:
        topic_parts = msg.topic.split('/')
        comodo = topic_parts[0]
        dispositivo = topic_parts[1]
        mensagem = msg.payload.decode()
        
        if dispositivo == "PortaPrincipal":
            controla_porta(estado_dispositivos, comodo, mensagem)
        if comodo == "Sistema de Alarme" and dispositivo == "Alarme":
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
client.loop_start()

@app.route('/')
def index():
    return render_template('index.html', dispositivos=estado_dispositivos)

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
    socketio.run(app, debug=True) 