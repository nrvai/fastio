from typing import Optional, Protocol, Self, Union


__all__ = (
    "ByteBuffer",
    "BytesLike"
)


type BytesLike = Union[bytearray, bytes, memoryview]


class ByteBuffer(Protocol):
    @property
    def readable(self: Self) -> int:
        ...

    @property
    def size(self: Self) -> int:
        ...

    @property
    def writable(self: Self) -> int:
        ...

    def find(self: Self, value: bytes) -> Optional[int]:
        ...

    def read(self: Self, size: Optional[int] = None) -> memoryview:
        ...

    def skip(self: Self, size: int) -> None:
        ...

    def write(self: Self, data: BytesLike) -> None:
        ...
