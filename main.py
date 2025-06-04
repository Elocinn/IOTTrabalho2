import paho.mqtt.client as mqtt
from config.topicos import topicos
from config.dispositivos import estado_dispositivos
from controladores.controle_led import controla_led
from controladores.controle_porta import controla_porta
from utils.estado import mostrar_estado

broker = "broker.emqx.io"
port = 1883

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
    predio, comodo = partes[0], partes[1]

    if comodo == "PortaPrincipal":
        controla_porta(estado_dispositivos, predio, mensagem)
    else:
        controla_led(estado_dispositivos, predio, comodo, mensagem)

    mostrar_estado(estado_dispositivos)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Conectando...")
client.connect(broker, port)
client.loop_forever()