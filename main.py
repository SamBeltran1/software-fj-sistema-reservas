from excepciones import ErrorSistemaFJ
from modelos import Cliente, SalaReuniones, EquipoComputo, AsesoriaTecnica
from gestor import GestorSoftwareFJ


def ejecutar_simulacion() -> None:
    gestor = GestorSoftwareFJ("registro_eventos.log")
    print("=== INICIANDO SIMULACIÓN DE OPERACIONES - SOFTWARE FJ ===\n")

    # 1. Registro válido de cliente 1
    try:
        c1 = Cliente("CLI-01", "Sammi Saray Beltrán", "sammi.beltran@correo.com", "3104567890")
        gestor.registrar_cliente(c1)
    except ErrorSistemaFJ as e:
        gestor.logger.error(f"Op 1 fallida: {e}")

    # 2. Registro válido de cliente 2
    try:
        c2 = Cliente("CLI-02", "Carlos Mendoza", "carlos.mendoza@empresa.co", "3209876543")
        gestor.registrar_cliente(c2)
    except ErrorSistemaFJ as e:
        gestor.logger.error(f"Op 2 fallida: {e}")

    # 3. Registro INVÁLIDO de cliente (correo sin @)
    try:
        c_invalido = Cliente("CLI-03", "Laura Gómez", "laura.gomez.sin.arroba", "3001112233")
        gestor.registrar_cliente(c_invalido)
    except ErrorSistemaFJ as e:
        gestor.logger.error(f"Op 3 (Cliente inválido): {e}")
        print(f"[ERROR CONTROLADO] Op 3: {e}")

    # 4. Registro INVÁLIDO de cliente duplicado
    try:
        c_duplicado = Cliente("CLI-01", "Otro Nombre", "otro@correo.com", "3112223344")
        gestor.registrar_cliente(c_duplicado)
    except ErrorSistemaFJ as e:
        gestor.logger.error(f"Op 4 (Duplicado): {e}")

    # 5. Creación válida de Sala de Reuniones
    try:
        s1 = SalaReuniones("SER-01", "Sala Innovación Norte", 80000, capacidad=10)
        gestor.agregar_servicio(s1)
    except ErrorSistemaFJ as e:
        gestor.logger.error(f"Op 5 fallida: {e}")

    # 6. Creación válida de Equipo de Cómputo
    try:
        s2 = EquipoComputo("SER-02", "Workstation Dell Precision", 55000, categoria="Estación Gráfica")
        gestor.agregar_servicio(s2)
    except ErrorSistemaFJ as e:
        gestor.logger.error(f"Op 6 fallida: {e}")

    # 7. Creación válida de Asesoría Técnica
    try:
        s3 = AsesoriaTecnica("SER-03", "Arquitectura Cloud y Seguridad", 120000, nivel="experto")
        gestor.agregar_servicio(s3)
    except ErrorSistemaFJ as e:
        gestor.logger.error(f"Op 7 fallida: {e}")

    # 8. Creación INVÁLIDA de servicio (tarifa negativa)
    try:
        s_malo = SalaReuniones("SER-04", "Sala Defectuosa", -25000, capacidad=4)
        gestor.agregar_servicio(s_malo)
    except ErrorSistemaFJ as e:
        gestor.logger.error(f"Op 8 (Servicio inválido): {e}")
        print(f"[ERROR CONTROLADO] Op 8: {e}")

    # 9. Reserva EXITOSA + confirmación + procesamiento de pago
    res1 = gestor.crear_reserva("RES-01", "CLI-01", "SER-01", duracion=3, descuento=0.10)
    if res1:
        try:
            res1.confirmar()
            mensaje_pago = res1.procesar(monto_pagado=300000)
            gestor.logger.info(mensaje_pago)
            print(f"[OK] {mensaje_pago}")
        except ErrorSistemaFJ as e:
            gestor.logger.error(f"Error en ciclo de RES-01: {e}")
            print(f"[ERROR CONTROLADO] {e}")

    # 10. Reserva FALLIDA porque la sala SER-01 ya quedó ocupada
    gestor.crear_reserva("RES-02", "CLI-02", "SER-01", duracion=2)

    # 11. Reserva FALLIDA por cliente inexistente
    gestor.crear_reserva("RES-03", "CLI-99", "SER-02", duracion=4)

    # 12. Reserva creada pero FALLIDA al procesar por pago insuficiente (con encadenamiento)
    res4 = gestor.crear_reserva("RES-04", "CLI-02", "SER-03", duracion=2)
    if res4:
        try:
            res4.confirmar()
            res4.procesar(monto_pagado=10000)
        except ErrorSistemaFJ as e:
            gestor.logger.error(f"Op 12 (Encadenamiento de error): {e} | Causa: {e.__cause__}")
            print(f"[ERROR CONTROLADO] Op 12: {e} (Causa: {e.__cause__})")
        finally:
            gestor.logger.info("Finalizó verificación de pago de RES-04.")

    gestor.resumen_general()
    print("\nSimulación completada sin interrupciones. Revisa 'registro_eventos.log'.")


if __name__ == "__main__":
    ejecutar_simulacion()
