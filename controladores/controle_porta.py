def controla_porta(estado_dispositivos, comodo, dispositivo, mensagem):
    comando = mensagem.strip().lower()
    if comando == "abrir":
        estado_dispositivos[comodo][dispositivo] = "Aberta"
        print(f"{comodo}/{dispositivo}: Aberta")
    elif comando == "fechar":
        estado_dispositivos[comodo][dispositivo] = "Fechada"
        print(f"{comodo}/{dispositivo}: Fechada")
    else:
        print(f"Comando inválido para {comodo}/{dispositivo}: {mensagem}")
