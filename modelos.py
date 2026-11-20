from abc import ABC, abstractmethod
from excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    CalculoInconsistenteError,
)


class Entidad(ABC):
    """Clase abstracta base para las entidades del sistema."""

    def __init__(self, codigo: str):
        if not codigo or not isinstance(codigo, str) or not codigo.strip():
            raise ParametroFaltanteError("El código de la entidad es obligatorio.")
        self._codigo = codigo.strip().upper()

    @property
    def codigo(self) -> str:
        return self._codigo

    @abstractmethod
    def obtener_detalle(self) -> str:
        """Devuelve una descripción legible de la entidad."""
        pass


class Cliente(Entidad):
    """Representa un cliente de Software FJ con atributos encapsulados."""

    def __init__(self, codigo: str, nombre: str, correo: str, telefono: str):
        super().__init__(codigo)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError("El nombre del cliente debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatoInvalidoError(f"El correo '{valor}' no tiene un formato válido.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if not valor or not valor.strip().isdigit() or len(valor.strip()) < 7:
            raise DatoInvalidoError("El teléfono debe contener solo números (mínimo 7 dígitos).")
        self._telefono = valor.strip()

    def obtener_detalle(self) -> str:
        return f"Cliente [{self.codigo}] - {self.nombre} | Email: {self.correo} | Tel: {self.telefono}"


class Servicio(Entidad, ABC):
    """Clase abstracta para los servicios ofrecidos por Software FJ."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(codigo)
        if not nombre or not nombre.strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        if not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatoInvalidoError("La tarifa base debe ser un número mayor a cero.")

        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self, duracion: int) -> None:
        """Valida reglas específicas del servicio según la duración."""
        pass

    @abstractmethod
    def calcular_costo_base(self, duracion: int) -> float:
        """Calcula el costo sin impuestos ni descuentos (polimorfismo)."""
        pass

    def calcular_total(
        self,
        duracion: int,
        impuesto: float = 0.19,
        descuento: float = 0.0,
        recargo_extra: float = 0.0,
    ) -> float:
        """
        Método sobrecargado mediante parámetros opcionales:
        permite calcular solo con duración, con IVA, con descuento o con recargo.
        """
        try:
            self.validar_parametros(duracion)
            if not (0 <= descuento <= 0.5):
                raise CalculoInconsistenteError("El descuento debe estar entre 0% y 50%.")
            if impuesto < 0 or recargo_extra < 0:
                raise CalculoInconsistenteError("Impuestos y recargos no pueden ser negativos.")

            subtotal = self.calcular_costo_base(duracion)
            con_descuento = subtotal * (1 - descuento)
            total = con_descuento * (1 + impuesto) + recargo_extra

            if total <= 0:
                raise CalculoInconsistenteError("El total calculado no puede ser menor o igual a 0.")
            return round(total, 2)
        except (TypeError, ZeroDivisionError) as err:
            raise CalculoInconsistenteError("Error matemático al calcular el total del servicio.") from err


class SalaReuniones(Servicio):
    """Servicio especializado para reserva de salas por horas."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, capacidad: int, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        if not isinstance(capacidad, int) or capacidad < 2:
            raise DatoInvalidoError("La capacidad de la sala debe ser de al menos 2 personas.")
        self.capacidad = capacidad

    def validar_parametros(self, duracion: int) -> None:
        if not isinstance(duracion, int) or duracion < 1 or duracion > 12:
            raise DatoInvalidoError("Las salas se reservan entre 1 y 12 horas.")

    def calcular_costo_base(self, duracion: int) -> float:
        return (self.tarifa_base * duracion) + 15000.0

    def obtener_detalle(self) -> str:
        estado = "Disponible" if self.disponible else "Ocupada"
        return f"Sala [{self.codigo}] {self.nombre} (Cap: {self.capacidad} pers.) - ${self.tarifa_base:,.0f}/h [{estado}]"


class EquipoComputo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos por días."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, categoria: str, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        if not categoria or not categoria.strip():
            raise ParametroFaltanteError("Debe indicar la categoría del equipo (ej. Portátil, Servidor).")
        self.categoria = categoria.strip()

    def validar_parametros(self, duracion: int) -> None:
        if not isinstance(duracion, int) or duracion < 1 or duracion > 30:
            raise DatoInvalidoError("El alquiler de equipos debe ser entre 1 y 30 días.")

    def calcular_costo_base(self, duracion: int) -> float:
        return (self.tarifa_base * duracion) * 1.05

    def obtener_detalle(self) -> str:
        estado = "Disponible" if self.disponible else "Alquilado"
        return f"Equipo [{self.codigo}] {self.nombre} ({self.categoria}) - ${self.tarifa_base:,.0f}/día [{estado}]"


class AsesoriaTecnica(Servicio):
    """Servicio especializado de consultoría y soporte profesional por horas."""

    TARIFAS_NIVEL = {"basico": 1.0, "intermedio": 1.25, "experto": 1.5}

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, nivel: str, disponible: bool = True):
        super().__init__(codigo, nombre, tarifa_base, disponible)
        nivel_limpio = nivel.strip().lower() if isinstance(nivel, str) else ""
        if nivel_limpio not in self.TARIFAS_NIVEL:
            raise DatoInvalidoError("El nivel de asesoría debe ser: basico, intermedio o experto.")
        self.nivel = nivel_limpio

    def validar_parametros(self, duracion: int) -> None:
        if not isinstance(duracion, int) or duracion < 1 or duracion > 8:
            raise DatoInvalidoError("Las asesorías técnicas duran entre 1 y 8 horas.")

    def calcular_costo_base(self, duracion: int) -> float:
        multiplicador = self.TARIFAS_NIVEL[self.nivel]
        return self.tarifa_base * duracion * multiplicador

    def obtener_detalle(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Asesoría [{self.codigo}] {self.nombre} (Nivel {self.nivel}) - ${self.tarifa_base:,.0f}/h [{estado}]"


class Reserva(Entidad):
    """Integra un Cliente, un Servicio, la duración y el ciclo de vida de la reserva."""

    def __init__(self, codigo: str, cliente: Cliente, servicio: Servicio, duracion: int, descuento: float = 0.0):
        super().__init__(codigo)
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Se requiere un objeto Cliente válido para reservar.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Se requiere un objeto Servicio válido para reservar.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible actualmente.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.descuento = descuento
        self.estado = "PENDIENTE"
        self.costo_total = self.servicio.calcular_total(duracion, descuento=descuento)

    def confirmar(self) -> None:
        """Usa try / except / else para confirmar la reserva de forma segura."""
        try:
            if self.estado != "PENDIENTE":
                raise ReservaInvalidaError(
                    f"No se puede confirmar la reserva {self.codigo} porque está en estado '{self.estado}'."
                )
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(f"El servicio '{self.servicio.nombre}' ya fue ocupado.")
        except ReservaInvalidaError:
            raise
        else:
            self.estado = "CONFIRMADA"
            self.servicio.disponible = False

    def cancelar(self) -> None:
        if self.estado == "PROCESADA":
            raise ReservaInvalidaError("No se puede cancelar una reserva que ya fue procesada y pagada.")
        if self.estado == "CANCELADA":
            raise ReservaInvalidaError("La reserva ya se encuentra cancelada.")
        if self.estado == "CONFIRMADA":
            self.servicio.disponible = True
        self.estado = "CANCELADA"

    def procesar(self, monto_pagado: float) -> str:
        """Usa try / except / finally para procesar el pago de la reserva."""
        try:
            if self.estado != "CONFIRMADA":
                raise ReservaInvalidaError("Solo se pueden procesar reservas en estado CONFIRMADA.")
            if monto_pagado < self.costo_total:
                raise DatoInvalidoError(
                    f"Pago insuficiente (${monto_pagado:,.2f}). El total es ${self.costo_total:,.2f}."
                )
            self.estado = "PROCESADA"
            cambio = monto_pagado - self.costo_total
            return f"Reserva {self.codigo} procesada con éxito. Cambio devuelto: ${cambio:,.2f}"
        except Exception as error:
            raise ReservaInvalidaError(f"Fallo al procesar la reserva {self.codigo}.") from error
        finally:
            pass

    def obtener_detalle(self) -> str:
        return (
            f"Reserva [{self.codigo}] | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Duración: {self.duracion} | "
            f"Total: ${self.costo_total:,.2f} | Estado: {self.estado}"
        )
