def ativar_alarme(estado_dispositivos):
    print("\nAlarme ativado! Desligando e fechando tudo...")

    for comodo, dispositivos in estado_dispositivos.items():
        for dispositivo in dispositivos:
            estado = dispositivos[dispositivo]

            if isinstance(estado, bool):
                estado_dispositivos[comodo][dispositivo] = False
                print(f"{comodo}/{dispositivo}: Desligado")

            elif isinstance(estado, str):
                estado_dispositivos[comodo][dispositivo] = "Fechada"
                print(f"{comodo}/{dispositivo}: Fechada")

    estado_dispositivos['Sistema de Alarme']['Alarme'] = True
    print("\nTodos os dispositivos desligados e portas/janelas fechadas.")
