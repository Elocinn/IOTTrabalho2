import paho.mqtt.client as mqtt
import time

BROKER = "test.mosquitto.org"
PORT = 8080
TOPICO_TEMPERATURA = "Quarto/temperatura"
TOPICO_AR = "Quarto/Ar Condicionado"

TEMPO_OBSERVACAO = 20  # segundos para observar a mudança de temperatura
TEMPO_INICIAL = 5      # segundos para garantir subscribe antes do teste

class TesteSensorTemperatura:
    def __init__(self):
        self.temperaturas = []
        self.todas_temperaturas = []  # Armazena todas as temperaturas recebidas
        self.client = mqtt.Client(transport="websockets")
        self.client.ws_set_options(path="/")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(BROKER, PORT)
        self.client.loop_start()
        self.testando = False

    def on_connect(self, client, userdata, flags, rc):
        print("Conectado ao broker para teste!")
        client.subscribe(TOPICO_TEMPERATURA)

    def on_message(self, client, userdata, msg):
        if msg.topic == TOPICO_TEMPERATURA:
            temp = float(msg.payload.decode())
            print(f"[DEBUG] Temperatura recebida: {temp}°C")
            self.todas_temperaturas.append(temp)
            if self.testando:
                self.temperaturas.append(temp)

    def testar(self):
        print(f"Aguardando {TEMPO_INICIAL}s para garantir subscribe...")
        time.sleep(TEMPO_INICIAL)
        print("\n--- Teste: LIGAR ar-condicionado ---")
        self.temperaturas.clear()
        self.testando = True
        self.client.publish(TOPICO_AR, "ligar")
        print("Comando enviado: ligar")
        time.sleep(TEMPO_OBSERVACAO)
        self.testando = False
        if len(self.temperaturas) < 2:
            print("Poucas leituras recebidas. Verifique se o simulador está rodando e publicando.")
            print(f"Temperaturas recebidas durante o teste: {self.temperaturas}")
            print(f"Temperaturas recebidas desde o início: {self.todas_temperaturas}")
            return
        if self.temperaturas[-1] < self.temperaturas[0]:
            print("OK: Temperatura caiu após ligar o ar-condicionado!")
        else:
            print("ERRO: Temperatura não caiu após ligar o ar-condicionado!")

        print("\n--- Teste: DESLIGAR ar-condicionado ---")
        self.temperaturas.clear()
        self.testando = True
        self.client.publish(TOPICO_AR, "desligar")
        print("Comando enviado: desligar")
        time.sleep(TEMPO_OBSERVACAO)
        self.testando = False
        if len(self.temperaturas) < 2:
            print("Poucas leituras recebidas. Verifique se o simulador está rodando e publicando.")
            print(f"Temperaturas recebidas durante o teste: {self.temperaturas}")
            print(f"Temperaturas recebidas desde o início: {self.todas_temperaturas}")
            return
        if self.temperaturas[-1] > self.temperaturas[0]:
            print("OK: Temperatura subiu após desligar o ar-condicionado!")
        else:
            print("ERRO: Temperatura não subiu após desligar o ar-condicionado!")

        print("\nTeste finalizado!")
        self.client.loop_stop()
        self.client.disconnect()

if __name__ == "__main__":
    teste = TesteSensorTemperatura()
    teste.testar() 