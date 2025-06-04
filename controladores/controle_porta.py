def controla_porta(estado_dispositivos, predio, mensagem):
    if mensagem.lower() == "abrir":
        estado_dispositivos[predio]["PortaPrincipal"] = "Aberta"
        print(f"{predio}/PortaPrincipal: Aberta")
    elif mensagem.lower() == "fechar":
        estado_dispositivos[predio]["PortaPrincipal"] = "Fechada"
        print(f"{predio}/PortaPrincipal: Fechada")
    else:
        print(f"Comando inválido para {predio}/PortaPrincipal: {mensagem}")