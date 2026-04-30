from __future__ import annotations
from typing import Optional

from .field import Field


class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.fields: dict[tuple[int, int], Field] = {}

    def get_field(self, x: int, y: int) -> Optional[Field]:
        return self.fields.get((x, y))

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_neighbors(self, x: int, y: int, n: int = 4) -> list[Field]:
        if n == 4:
            offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        else:
            offsets = [
                (dx, dy)
                for dx in [-1, 0, 1]
                for dy in [-1, 0, 1]
                if not (dx == 0 and dy == 0)
            ]
        result = []
        for dx, dy in offsets:
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny):
                f = self.get_field(nx, ny)
                if f is not None:
                    result.append(f)
        return result

    def get_all_fields(self) -> list[Field]:
        return list(self.fields.values())
