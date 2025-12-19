from typing import Callable, Generator, Optional, Self, Union

from .byte_buffer import ByteBuffer


__all__ = (
    "Accept",
    "Close",
    "Drain",
    "Signal",
    "Writing",
    "Writer"
)


class Accept:
    pass


class Close(BaseException):
    pass


class Drain:
    __match_args__ = ("size",)

    def __init__(self, size: Optional[int] = None) -> None:
        self.size = size


type Signal = Union[Accept, Drain]
type Writing[T] = Generator[Signal, Optional[T], None]
type Writer[T] = Callable[[ByteBuffer], Writing[T]]
