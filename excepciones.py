class ErrorSistemaFJ(Exception):
    """Excepción base del sistema de Software FJ."""
    pass


class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un dato ingresado no cumple el formato o regla."""
    pass


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando falta un dato obligatorio para crear un objeto."""
    pass


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando el servicio está inactivo o supera su capacidad."""
    pass


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza cuando se intenta realizar una acción no permitida en una reserva."""
    pass


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando un cálculo financiero da un resultado inválido."""
    pass
