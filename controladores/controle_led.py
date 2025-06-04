def controla_led(estado_dispositivos, predio, comodo, mensagem):
    if mensagem.lower() == "ligar":
        estado_dispositivos[predio][comodo] = True
        print(f"{predio}/{comodo}: Ligado")
    elif mensagem.lower() == "desligar":
        estado_dispositivos[predio][comodo] = False
        print(f"{predio}/{comodo}: Desligado")
    else:
        print(f"Comando inválido para {predio}/{comodo}: {mensagem}")