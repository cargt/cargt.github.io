"""Uncompressed size of the xz stream at the end of a .deb, from its last bytes (footer + index)."""
import struct


def varint(buf, pos):
    val, shift = 0, 0
    while True:
        b = buf[pos]; pos += 1
        val |= (b & 0x7f) << shift
        if not b & 0x80:
            return val, pos
        shift += 7


def xz_uncompressed(tail):
    """tail: the last bytes of the .deb. Returns (uncompressed_size, needed_bytes) or (None, needed_bytes)."""
    t = tail
    if t.endswith(b'\n'):          # ar pads odd-sized members with a newline
        t = t[:-1]
    while t.endswith(b'\0\0\0\0'):  # xz stream padding
        t = t[:-4]
    if len(t) < 12 or t[-2:] != b'YZ':
        return None, 0
    backward = (struct.unpack('<I', t[-8:-4])[0] + 1) * 4
    need = backward + 12 + (len(tail) - len(t))
    if len(t) < backward + 12:
        return None, need
    idx = t[-12 - backward:-12]
    if idx[0] != 0:
        return None, need
    n, pos = varint(idx, 1)
    total = 0
    for _ in range(n):
        _, pos = varint(idx, pos)
        u, pos = varint(idx, pos)
        total += u
    return total, need
