__all__ = (
    "ByteBuffer",
)


class ByteBuffer:
    def __init__(self, data: bytearray, position: int) -> None:
        self.data = data
        self.position = position
