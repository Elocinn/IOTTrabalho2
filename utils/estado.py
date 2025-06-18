def mostrar_estado(estado_dispositivos):
    print("\nEstado Atual da Casa:")
    for comodo, dispositivos in estado_dispositivos.items():
        print(f"\n{comodo}:")
        for dispositivo, estado in dispositivos.items():
            print(f"  - {dispositivo}: {estado}")
    print("-" * 40)
