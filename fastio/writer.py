from typing import AsyncGenerator, Callable, Generator, Optional, Union

from .byte_buffer import ByteBuffer


__all__ = (
    "Accept",
    "AsyncWriter",
    "AsyncWriting",
    "Close",
    "Drain",
    "Signal",
    "Writing",
    "Writer",

    "close",
    "push"
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
type AsyncWriting[T] = AsyncGenerator[Signal, Optional[T]]
type Writing[T] = Generator[Signal, Optional[T], None]
type AsyncWriter[T] = Callable[[ByteBuffer], AsyncWriting[T]]
type Writer[T] = Callable[[ByteBuffer], Writing[T]]


def close[T](writing: Writing[T]) -> Writing[T]:
    try:
        signal = writing.throw(Close)
    except StopIteration:
        return

    while not isinstance(signal, Accept):
        yield signal

        try:
            signal = next(writing)
        except StopIteration:
            return


def push[T](writing: Writing[T], value: T) -> Writing[T]:
    try:
        signal = writing.send(value)
    except StopIteration:
        return

    while not isinstance(signal, Accept):
        yield signal

        try:
            signal = next(writing)
        except StopIteration:
            return
