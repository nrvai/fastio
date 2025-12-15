import random

from textwrap import dedent

import pytest

from fastio.byte_buffer import ByteBuffer
from fastio.common import read_lines
from fastio.reader import Read, Result


def partition(items, size):
    parts = []
    index = 0

    while True:
        part = items[index:index + size]

        if len(part) != 0:
            parts.append(part)
        
        if len(part) < size:
            break

        index += size

    return parts


@pytest.mark.parametrize(
    "text",
    [
        """
        HTTP/1.1 201 Created
        Content-Type: application/json
        Location: http://example.com/users/123

        """
    ]
)
def test_line_reader(text):
    data = dedent(text[1:]).encode()

    parts = iter(partition(data, 8))
    buffer = ByteBuffer.empty()
    reader = read_lines(b"\n")
    lines = []

    for signal in reader(buffer):
        match signal:
            case Read():
                buffer.extend(next(parts))
            case Result(line):
                lines.append(bytes(line))
                line.release()

    result = b"\n".join(lines) + b"\n\n"

    assert result == data
