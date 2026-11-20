# software-fj-sistema-reservas

Sistema orientado a objetos sin base de datos y con manejo robusto de excepciones para **Software FJ** (UNAD - Curso Programación 213023 - Fase 4).

## Estructura del proyecto
- `excepciones.py`: Jerarquía de excepciones personalizadas del sistema.
- `modelos.py`: Clase abstracta `Entidad`, `Cliente` (encapsulado y validado), clase abstracta `Servicio`, servicios especializados (`SalaReuniones`, `EquipoComputo`, `AsesoriaTecnica`) con polimorfismo y sobrecarga mediante parámetros opcionales, y `Reserva`.
- `gestor.py`: Administración de listas en memoria (sin base de datos) y registro de eventos/errores en `registro_eventos.log`.
- `main.py`: Simulación de 12 operaciones (válidas e inválidas) con bloques `try/except/else/finally` y encadenamiento de excepciones.

## Ejecución
```bash
python main.py
```
