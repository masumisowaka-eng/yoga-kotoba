#!/usr/bin/env python3
import struct, zlib, math

def write_png(filename, size):
    img = []
    for y in range(size):
        row = []
        for x in range(size):
            t = y / size
            r = int(212 * (1-t) + 200 * t)
            g = int(232 * (1-t) + 220 * t)
            b = int(212 * (1-t) + 200 * t)
            cx, cy = size/2, size/2
            dist = math.sqrt((x-cx)**2 + (y-cy)**2)
            radius = size * 0.45
            if dist > radius + 2:
                r, g, b = 212, 232, 212
            elif dist > radius:
                a = (dist - radius) / 2
                r = int(r*(1-a) + 212*a)
                g = int(g*(1-a) + 232*a)
                b = int(b*(1-a) + 212*a)
            row.extend([r, g, b])
        img.append(bytes([0] + row))

    def chunk(t, d):
        c = t + d
        return struct.pack('>I', len(d)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)

    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0))
    idat = chunk(b'IDAT', zlib.compress(b''.join(img), 9))
    iend = chunk(b'IEND', b'')
    with open(filename, 'wb') as f:
        f.write(sig + ihdr + idat + iend)
    print(f'Created {filename}')

write_png('icon-192.png', 192)
write_png('icon-512.png', 512)
