from typing import Generator, Optional, Protocol, Self, Union

from .byte_buffer import ByteBuffer


__all__ = (
    "Read",
    "Reader",
    "Reading",
    "Result",
    "Signal"
)


class Read:
    def __init__(self: Self, size: Optional[int] = None) -> None:
        self.size = size


class Result[T]:
    def __init__(self: Self, value: T) -> None:
        self.value = value


type Signal[T] = Union[
    Read,
    Result[T]
]


type Reading[T] = Generator[Signal[T]]


class Reader[T](Protocol):
    def read(self: Self, buffer: ByteBuffer) -> Reading[T]:
        ...
