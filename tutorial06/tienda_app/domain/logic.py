class CalculadorImpuestos:
    """
    S - Responsabilidad Única (SRP): solo calcula impuestos.
    O - Abierto/Cerrado (OCP): podríamos heredar para otros países
        sin modificar el cálculo base. El IVA deja de estar "hardcoded"
        dentro de la vista (como ocurría en la versión Spaghetti).
    """

    IVA = 1.19  # Regla de negocio pura (19 %)

    @staticmethod
    def obtener_total_con_iva(precio_base: float) -> float:
        return float(precio_base) * CalculadorImpuestos.IVA
