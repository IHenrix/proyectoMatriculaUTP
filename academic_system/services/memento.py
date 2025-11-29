"""
Memento Pattern para conservar historial de notas.

Se guarda un snapshot previo al cambio para auditoría o posible rollback.
"""

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class NotaMemento:
    nota_id: int
    estado: Dict[str, Any]


class NotaCaretaker:
    """Caretaker sencillo en memoria."""

    _historial: List[NotaMemento] = []

    @classmethod
    def guardar_snapshot(cls, nota_id: int, estado: Dict[str, Any]):
        cls._historial.append(NotaMemento(nota_id=nota_id, estado=estado))

    @classmethod
    def obtener_historial(cls, nota_id: int):
        return [m for m in cls._historial if m.nota_id == nota_id]

