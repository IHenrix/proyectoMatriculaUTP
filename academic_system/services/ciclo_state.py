"""
State Pattern para el ciclo académico.

Encapsula el comportamiento según el estado del ciclo: abierto,
cerrado o terminado. Se usa en el modelo Ciclo para centralizar
la lógica de validación de matrícula y edición de notas.
"""

from datetime import date


class CicloState:
    """Estado base del ciclo."""

    def __init__(self, ciclo):
        self.ciclo = ciclo

    def puede_matricularse(self):
        """Indica si se permite matrícula en este estado."""
        raise NotImplementedError

    def permite_editar_notas(self):
        """Indica si se permite editar notas en este estado."""
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__


class MatriculaAbiertaState(CicloState):
    def puede_matricularse(self):
        hoy = date.today()
        return (
            self.ciclo.matricula_abierta
            and self.ciclo.fecha_inicio_matricula <= hoy <= self.ciclo.fecha_fin_matricula
            and not self.ciclo.ciclo_terminado
        )

    def permite_editar_notas(self):
        return not self.ciclo.ciclo_terminado


class MatriculaCerradaState(CicloState):
    def puede_matricularse(self):
        return False

    def permite_editar_notas(self):
        return not self.ciclo.ciclo_terminado


class CicloTerminadoState(CicloState):
    def puede_matricularse(self):
        return False

    def permite_editar_notas(self):
        return False


class CicloStateFactory:
    """Factory para devolver el estado adecuado de un ciclo."""

    @staticmethod
    def from_ciclo(ciclo):
        if ciclo.ciclo_terminado:
            return CicloTerminadoState(ciclo)
        if ciclo.matricula_abierta:
            return MatriculaAbiertaState(ciclo)
        return MatriculaCerradaState(ciclo)

