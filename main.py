import paho.mqtt.client as mqtt
from config.topicos import topicos
from config.dispositivos import estado_dispositivos
from controladores.controle_led import controla_led
from controladores.controle_porta import controla_porta
from utils.estado import mostrar_estado
import threading
import random
import time

broker = "test.mosquitto.org"
port = 8080

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT")
        for topico in topicos:
            client.subscribe(topico)
            print(f"Inscrito no tópico: {topico}")
    else:
        print("Falha na conexão. Código:", rc)

def on_message(client, userdata, msg):
    mensagem = msg.payload.decode()
    topico = msg.topic
    print(f"\nMensagem recebida | {topico}: {mensagem}")
    partes = topico.split("/")
    if len(partes) != 2:
        print(f"Tópico inválido: {topico}")
        return
    comodo, dispositivo = partes
    if "Porta" in dispositivo or "Janela" in dispositivo or "Cortinas" in dispositivo:
        controla_porta(estado_dispositivos, comodo, dispositivo, mensagem)
    else:
        controla_led(estado_dispositivos, comodo, dispositivo, mensagem)
    mostrar_estado(estado_dispositivos)

def simular_temperatura(client):
    predios = [f"predio{i}" for i in range(1, 6)]
    while True:
        for predio in predios:
            temperatura = round(random.uniform(18.0, 30.0), 1)
            topico = f"{predio}/temperatura"
            mensagem = str(temperatura)
            client.publish(topico, mensagem)
            print(f"[Simulação] Publicado {mensagem}°C em {topico}")
        time.sleep(5)

client = mqtt.Client(transport="websockets")
client.ws_set_options(path="/")
client.on_connect = on_connect
client.on_message = on_message
print("Conectando ao broker MQTT...")
client.connect(broker, port)
threading.Thread(target=simular_temperatura, args=(client,), daemon=True).start()
client.loop_forever()
