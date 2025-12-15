from typing import Optional, Self


__all__ = (
    "ByteBuffer",
)


class ByteBuffer:
    def __init__(self: Self, data: bytearray, position: int) -> None:
        self.data = data
        self.position = position

    @property
    def remaining(self: Self) -> int:
        return self.size - self.position

    @property
    def size(self: Self) -> int:
        return len(self.data)

    def find(
        self: Self,
        value: bytes,
        start: Optional[int] = None,
        stop: int = -1
    ) -> Optional[int]:
        start = self.position if start is None else start
        position = self.data.find(value, start, stop)

        return None if position == -1 else position

    def read_to(self: Self, position: int) -> memoryview:
        view = memoryview(self.data)[self.position:position]

        self.position = position

        return view

    def skip_to(self: Self, position: int) -> None:
        self.position = position
