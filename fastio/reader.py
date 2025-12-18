from typing import Callable, Generator, Optional, Self, Union

from .byte_buffer import ByteBuffer


__all__ = (
    "Read",
    "Reader",
    "Reading",
    "Result",
    "Signal"
)


class Read:
    __match_args__ = ("size",)

    def __init__(self: Self, size: Optional[int] = None) -> None:
        self.size = size


class Result[T]:
    __match_args__ = ("value",)

    def __init__(self: Self, value: T) -> None:
        self.value = value


type Signal[T] = Union[Read, Result[T]]
type Reading[T] = Generator[Signal[T]]
type Reader[T] = Callable[[ByteBuffer], Reading[T]]
