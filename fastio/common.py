from .byte_buffer import ByteBuffer
from .reader import Read, Reader, Reading, Result


__all__ = (
    "read_exact",
    "read_lines"
)


def read_exact(total_size: int) -> Reader[memoryview]:
    def read(buffer: ByteBuffer) -> Reading[memoryview]:
        counter = total_size

        while counter > 0:
            remaining = buffer.remaining

            if remaining == 0:
                yield Read()
                continue

            current_size = counter if counter <= remaining else remaining

            value = buffer.read(current_size)

            yield Result(value)

            counter -= current_size

    return read


def read_lines(delimiter: bytes) -> Reader[memoryview]:
    def read(buffer: ByteBuffer) -> Reading[memoryview]:
        while True:
            position = buffer.find(delimiter)

            if position is None:
                yield Read()
                continue

            line = buffer.read_to(position)
            buffer.skip(len(delimiter))

            if line == b"":
                return

            yield Result(line)

    return read
