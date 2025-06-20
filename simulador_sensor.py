import paho.mqtt.client as mqtt
import time
import random
from config.dispositivos import estado_dispositivos, temperaturas_ambientes

# Estado local do ar-condicionado
ar_condicionado_ligado = estado_dispositivos['Quarto']['Ar Condicionado']

def on_connect(client, userdata, flags, rc):
    print("[Simulador] Conectado ao broker MQTT")
    client.subscribe('Quarto/Ar Condicionado')

def on_message(client, userdata, msg):
    global ar_condicionado_ligado
    topic = msg.topic
    payload = msg.payload.decode().lower()
    if topic == 'Quarto/Ar Condicionado':
        if payload == 'ligar':
            ar_condicionado_ligado = True
        elif payload == 'desligar':
            ar_condicionado_ligado = False
        estado_dispositivos['Quarto']['Ar Condicionado'] = ar_condicionado_ligado
        print(f"[Simulador] Ar Condicionado {'LIGADO' if ar_condicionado_ligado else 'DESLIGADO'}")

def simular_temperatura_ambientes(client):
    while True:
        for ambiente in temperaturas_ambientes.keys():
            if ambiente == 'Quarto':
                if ar_condicionado_ligado:
                    temperaturas_ambientes['Quarto'] -= random.uniform(0.2, 0.5)
                else:
                    temperaturas_ambientes['Quarto'] += random.uniform(0.05, 0.2)
                temperaturas_ambientes['Quarto'] = max(18.0, min(30.0, temperaturas_ambientes['Quarto']))
            else:
                temperaturas_ambientes[ambiente] += random.uniform(-0.1, 0.1)
                temperaturas_ambientes[ambiente] = max(18.0, min(30.0, temperaturas_ambientes[ambiente]))
            topico = f"{ambiente}/temperatura"
            mensagem = f"{temperaturas_ambientes[ambiente]:.1f}"
            client.publish(topico, mensagem)
            print(f"[Simulação] Publicado {mensagem}°C em {topico}")
        time.sleep(5)

broker = "test.mosquitto.org"
port = 8080
client = mqtt.Client(transport="websockets")
client.ws_set_options(path="/")
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)
client.loop_start()

if __name__ == "__main__":
    simular_temperatura_ambientes(client) 