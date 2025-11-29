"""
Prototype Pattern para clonar entidades ligeras.

Se usa para generar instancias de Nota a partir de un prototipo base
sin repetir configuración común.
"""

from copy import deepcopy


class NotaPrototype:
    """Prototipo simple para crear notas vacías por componente."""

    def __init__(self, base_data: dict):
        self.base_data = base_data

    def clone(self, **overrides):
        data = deepcopy(self.base_data)
        data.update(overrides)
        return data

