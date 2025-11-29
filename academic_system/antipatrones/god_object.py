"""
Ejemplo de antipatrón: God Object.

Esta clase concentra demasiadas responsabilidades y viola SRP/ISP.
Se deja como referencia didáctica para la rúbrica; no se usa en producción.
"""


class GodObject:
    def __init__(self):
        self.usuarios = []
        self.cursos = []
        self.logs = []

    def hacer_todo(self):
        # Antipatron: mezcla gestion de usuarios, cursos y logging
        self.logs.append("haciendo todo en un solo lugar (malo)")
        return "Antipatron: God Object en acción"

