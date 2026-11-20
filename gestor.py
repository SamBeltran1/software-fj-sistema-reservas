import logging
from excepciones import (
    ErrorSistemaFJ,
    DatoInvalidoError,
    ReservaInvalidaError,
)
from modelos import Cliente, Servicio, Reserva


class GestorSoftwareFJ:
    """Administra clientes, servicios y reservas en memoria con registro de logs."""

    def __init__(self, archivo_log: str = "registro_eventos.log"):
        self._clientes: list[Cliente] = []
        self._servicios: list[Servicio] = []
        self._reservas: list[Reserva] = []
        self._configurar_logger(archivo_log)

    def _configurar_logger(self, archivo_log: str) -> None:
        self.logger = logging.getLogger("SoftwareFJ")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.FileHandler(archivo_log, mode="w", encoding="utf-8")
            formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            handler.setFormatter(formato)
            self.logger.addHandler(handler)

    def registrar_cliente(self, cliente: Cliente) -> bool:
        try:
            for c in self._clientes:
                if c.codigo == cliente.codigo or c.correo == cliente.correo:
                    raise DatoInvalidoError(
                        f"Ya existe un cliente con código '{cliente.codigo}' o correo '{cliente.correo}'."
                    )
        except ErrorSistemaFJ as err:
            self.logger.error(f"Error al registrar cliente: {err}")
            print(f"[ERROR CONTROLADO] {err}")
            return False
        else:
            self._clientes.append(cliente)
            self.logger.info(f"Cliente registrado: {cliente.obtener_detalle()}")
            print(f"[OK] {cliente.obtener_detalle()}")
            return True
        finally:
            self.logger.info("Intento de registro de cliente finalizado.")

    def agregar_servicio(self, servicio: Servicio) -> bool:
        try:
            for s in self._servicios:
                if s.codigo == servicio.codigo:
                    raise DatoInvalidoError(f"El servicio con código '{servicio.codigo}' ya existe.")
            self._servicios.append(servicio)
            self.logger.info(f"Servicio agregado: {servicio.obtener_detalle()}")
            print(f"[OK] {servicio.obtener_detalle()}")
            return True
        except ErrorSistemaFJ as err:
            self.logger.error(f"Error al agregar servicio: {err}")
            print(f"[ERROR CONTROLADO] {err}")
            return False

    def crear_reserva(
        self,
        codigo_res: str,
        cod_cliente: str,
        cod_servicio: str,
        duracion: int,
        descuento: float = 0.0,
    ):
        try:
            cliente = next((c for c in self._clientes if c.codigo == cod_cliente.upper()), None)
            if not cliente:
                raise ReservaInvalidaError(f"No existe el cliente con código '{cod_cliente}'.")

            servicio = next((s for s in self._servicios if s.codigo == cod_servicio.upper()), None)
            if not servicio:
                raise ReservaInvalidaError(f"No existe el servicio con código '{cod_servicio}'.")

            reserva = Reserva(codigo_res, cliente, servicio, duracion, descuento)
        except ErrorSistemaFJ as err:
            self.logger.error(f"No se pudo crear la reserva '{codigo_res}': {err}")
            print(f"[ERROR CONTROLADO] Reserva '{codigo_res}' fallida: {err}")
            return None
        else:
            self._reservas.append(reserva)
            self.logger.info(f"Reserva creada: {reserva.obtener_detalle()}")
            print(f"[OK] {reserva.obtener_detalle()}")
            return reserva
        finally:
            self.logger.info(f"Cierre de transacción de creación para reserva '{codigo_res}'.")

    def resumen_general(self) -> None:
        print("\n=== RESUMEN FINAL DEL SISTEMA SOFTWARE FJ ===")
        print(f"Clientes registrados : {len(self._clientes)}")
        print(f"Servicios registrados: {len(self._servicios)}")
        print(f"Reservas registradas : {len(self._reservas)}")
