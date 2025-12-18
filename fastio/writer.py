from typing import Callable, Generator, Optional

from .byte_buffer import ByteBuffer


class Drain:
    __match_args__ = ("size",)

    def __init__(self, size: Optional[int] = None) -> None:
        self.size = size


type Signal = Drain
type Writing = Generator[Signal]
type Writer[T] = Callable[[T, ByteBuffer], Writing]
