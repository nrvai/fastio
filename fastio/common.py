from typing import AsyncIterable, Callable, Iterable, Optional, Self

from .byte_buffer import ByteBuffer, BytesLike
from .reader import Read, Reader, Reading, Result
from .writer import (
    Accept,
    AsyncWriter,
    AsyncWriting,
    Close,
    Drain,
    Writer,
    Writing,

    close,
    push
)


__all__ = (
    "ArrayByteBuffer",

    "read_bytes",
    "read_lines",
    "write_bytes",
    "write_lines"
)


class ArrayByteBuffer:
    def __init__(
        self: Self,
        data: bytearray,
        read_position: int,
        write_position: int
    ) -> None:
        self.data = data
        self.read_position = read_position
        self.write_position = write_position

    @property
    def readable(self: Self) -> int:
        return self.write_position - self.read_position

    @property
    def size(self: Self) -> int:
        return len(self.data)

    @property
    def writable(self: Self) -> int:
        return self.size - self.write_position

    def find(self: Self, value: bytes) -> Optional[int]:
        start = self.read_position
        stop = self.write_position

        position = self.data.find(value, start, stop)

        if position == -1:
            return None

        return position - self.read_position

    def read(self: Self, size: Optional[int] = None) -> memoryview:
        if size is None:
            size = self.readable

        view = memoryview(self.data)[
            self.read_position:self.read_position + size
        ]

        self.read_position += size

        return view

    def resize(self: Self, size: int) -> None:
        if self.read_position > size:
            self.read_position = 0

        if self.write_position > size:
            self.write_position = size

        self.data.resize(size)

    def skip(self: Self, size: int) -> None:
        self.read_position += size

    def write(self: Self, data: BytesLike) -> None:
        self.data[self.write_position:self.write_position + len(data)] = data

        self.write_position += len(data)

    @classmethod
    def allocate(cls: type[Self], size: int) -> Self:
        return cls(bytearray(b"\x00" * size), 0, 0)

    @classmethod
    def empty(cls: type[Self]) -> Self:
        return cls(bytearray(), 0, 0)

    @classmethod
    def of(cls: type[Self], data: BytesLike) -> Self:
        return cls(bytearray(data), 0, len(data))


def read_bytes(total_size: int) -> Reader[memoryview]:
    def read(buffer: ByteBuffer) -> Reading[memoryview]:
        counter = total_size

        while counter > 0:
            readable = buffer.readable

            if readable == 0:
                yield Read()
                continue

            current_size = counter if counter <= readable else readable

            value = buffer.read(current_size)

            yield Result(value)

            counter -= current_size

    return read


def read_lines(delimiter: bytes) -> Reader[memoryview]:
    def read(buffer: ByteBuffer) -> Reading[memoryview]:
        while True:
            size = buffer.find(delimiter)

            if size is None:
                yield Read()
                continue

            line = buffer.read(size)
            buffer.skip(len(delimiter))

            if line == b"":
                return

            yield Result(line)

    return read


def write_bytes(buffer: ByteBuffer) -> Writing[BytesLike]:
    while True:
        try:
            data = yield Accept()

            assert data is not None
        except Close:
            return

        view = memoryview(data)

        while view:
            if buffer.writable == 0:
                yield Drain(len(view))
                continue

            size = min(buffer.writable, len(view))
            buffer.write(view[:size])
            view = view[size:]


def write_lines(delimiter: bytes) -> Writer[BytesLike]:
    def write(buffer: ByteBuffer) -> Writing[BytesLike]:
        writing = write_bytes(buffer)
        next(writing)

        while True:
            try:
                data = yield Accept()

                yield from push(writing, data)
                yield from push(writing, delimiter) # pyright: ignore [reportReturnType]
            except Close:
                yield from push(writing, delimiter) # pyright: ignore [reportReturnType]
                yield from close(writing)

                return

    return write


def write_iterable[T](items: Iterable[T]) -> Callable[[Writer[T]], Writer[T]]:
    def wrap(writer: Writer[T]) -> Writer[T]:
        def write(buffer: ByteBuffer) -> Writing[T]:
            writing = writer(buffer)
            next(writing)

            for item in items:
                yield from push(writing, item)

            yield from close(writing)

        return write

    return wrap


def write_async_iterable[T](
    items: AsyncIterable[T]
) -> Callable[[Writer[T]], AsyncWriter[T]]:
    def wrap(writer: Writer[T]) -> AsyncWriter[T]:
        async def write(buffer: ByteBuffer) -> AsyncWriting[T]:
            writing = writer(buffer)
            next(writing)

            async for item in items:
                for signal in push(writing, item):
                    yield signal

            for signal in close(writing):
                yield signal

        return write

    return wrap
