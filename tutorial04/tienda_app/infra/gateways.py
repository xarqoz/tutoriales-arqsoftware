import datetime

from ..domain.interfaces import ProcesadorPago


class BancoNacionalProcesador(ProcesadorPago):
    """
    Implementación concreta de infraestructura (Paso 4 del tutorial).

    Cumple el contrato ProcesadorPago (DIP) y simula un banco local
    escribiendo cada transacción en un archivo de auditoría (.log).
    """

    def pagar(self, monto: float) -> bool:
        # ──────────────────────────────────────────────────────────────
        # IMPORTANTE: sustituya "SU_NOMBRE" por su nombre y apellido real.
        # El tutorial exige que el nombre del archivo sea único por
        # estudiante para validar la evidencia de ejecución.
        # Ejemplo: "pagos_locales_JUAN_PEREZ.log"
        # ──────────────────────────────────────────────────────────────
        archivo_log = "pagos_locales_SU_NOMBRE.log"

        with open(archivo_log, "a", encoding="utf-8") as f:
            f.write(
                f"[{datetime.datetime.now()}] Transaccion exitosa por: ${monto}\n"
            )
        return True
