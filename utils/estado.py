def mostrar_estado(estado_dispositivos):
    print("\nEstado Atual:")
    for predio, comodos in estado_dispositivos.items():
        print(f"\n{predio}")
        for dispositivo, estado in comodos.items():
            print(f" - {dispositivo}: {estado}")
    print("-" * 40)