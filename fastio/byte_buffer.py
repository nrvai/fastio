from typing import Optional, Self


__all__ = (
    "ByteBuffer",
)


class ByteBuffer:
    def __init__(self: Self, data: bytearray, position: int = 0) -> None:
        self.data = data
        self.position = position

    @property
    def remaining(self: Self) -> int:
        return self.size - self.position

    @property
    def size(self: Self) -> int:
        return len(self.data)

    def extend(self: Self, data: bytearray) -> None:
        self.data.extend(data)

    def find(
        self: Self,
        value: bytes,
        start: Optional[int] = None,
        stop: Optional[int] = None
    ) -> Optional[int]:
        start = self.position if start is None else start

        position = self.data.find(value, start, stop)

        return None if position == -1 else position

    def read(self: Self, size: Optional[int] = None) -> memoryview:
        if size is None:
            size = self.remaining

        view = memoryview(self.data)[self.position:self.position + size]

        self.position += size

        return view

    def read_to(self: Self, position: int) -> memoryview:
        view = memoryview(self.data)[self.position:position]

        self.position = position

        return view

    def skip(self: Self, size: int) -> None:
        self.position += size

    def skip_to(self: Self, position: int) -> None:
        self.position = position

    @classmethod
    def empty(cls: type[Self]) -> Self:
        return cls(bytearray())
