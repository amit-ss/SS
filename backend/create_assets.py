import zlib
import struct
from pathlib import Path

def create_png(width, height, color_rgba, filepath):
    # PNG signature
    png = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk
    ihdr_data = struct.pack('!IIBBBBB', width, height, 8, 6, 0, 0, 0)
    ihdr_crc = zlib.crc32(b'IHDR' + ihdr_data)
    png += struct.pack('!I', len(ihdr_data)) + b'IHDR' + ihdr_data + struct.pack('!I', ihdr_crc)
    
    # IDAT chunk
    raw_data = bytearray()
    r, g, b, a = color_rgba
    for _ in range(height):
        raw_data.append(0) # filter type 0
        for _ in range(width):
            raw_data.extend([r, g, b, a])
            
    compressed = zlib.compress(raw_data)
    idat_crc = zlib.crc32(b'IDAT' + compressed)
    png += struct.pack('!I', len(compressed)) + b'IDAT' + compressed + struct.pack('!I', idat_crc)
    
    # IEND chunk
    iend_crc = zlib.crc32(b'IEND')
    png += struct.pack('!I', 0) + b'IEND' + struct.pack('!I', iend_crc)
    
    with open(filepath, 'wb') as f:
        f.write(png)

assets_dir = Path(r"E:\SS\mobile\assets")
assets_dir.mkdir(parents=True, exist_ok=True)

# LPU Navy Blue: #1E3A8A -> 30, 58, 138, 255
create_png(192, 192, (30, 58, 138, 255), assets_dir / "icon.png")
create_png(192, 192, (37, 99, 235, 255), assets_dir / "adaptive-icon.png")
create_png(400, 800, (30, 58, 138, 255), assets_dir / "splash.png")
create_png(48, 48, (30, 58, 138, 255), assets_dir / "favicon.png")
print("Assets generated successfully!")
