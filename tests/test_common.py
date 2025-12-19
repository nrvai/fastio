import random

from textwrap import dedent

import pytest

from fastio.common import ArrayByteBuffer, read_lines, write_lines
from fastio.reader import Read, Result
from fastio.writer import Accept, Drain


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
    buffer = ArrayByteBuffer.empty()
    reader = read_lines(b"\n")
    lines = []

    for signal in reader(buffer):
        match signal:
            case Read():
                buffer.write(next(parts))
            case Result(line):
                lines.append(bytes(line))
                line.release()

    result = b"\n".join(lines) + b"\n\n"

    assert result == data


@pytest.mark.parametrize(
    "text",
    [
        """
        RTSP/1.0 200 OK
        CSeq: 1
        Public: DESCRIBE, SETUP, TEARDOWN, PLAY, PAUSE

        """
    ]
)
def test_line_writer(text):
    size = 8
    buffer = ArrayByteBuffer.allocate(size)

    data = dedent(text[1:]).encode()
    lines = iter(data.split(b"\n")[:-2])
    writer = write_lines(b"\n")
    writing = writer(buffer)
    signal = next(writing)

    while True:
        match signal:
            case Accept():
                try:
                    signal = writing.send(next(lines))
                except StopIteration:
                    signal = writing.throw(StopIteration)
            case Drain():
                size *= 2

                buffer.resize(size)
                signal = next(writing)

    result = buffer.read()

    assert result == data
