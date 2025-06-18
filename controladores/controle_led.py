def controla_led(estado_dispositivos, comodo, dispositivo, mensagem):
    if mensagem.lower() == "ligar":
        estado_dispositivos[comodo][dispositivo] = True
        print(f"{comodo}/{dispositivo}: Ligado")
    elif mensagem.lower() == "desligar":
        estado_dispositivos[comodo][dispositivo] = False
        print(f"{comodo}/{dispositivo}: Desligado")
    else:
        print(f"Comando inválido para {comodo}/{dispositivo}: {mensagem}")