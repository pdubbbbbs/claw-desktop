#!/usr/bin/env python3
"""Generate app icons for Claw Command Deck Tauri app."""
from PIL import Image, ImageDraw, ImageFont
import struct, io

def create_icon(size):
    """Create a dark terminal-style icon with >_ prompt."""
    img = Image.new("RGBA", (size, size), (10, 15, 26, 255))
    draw = ImageDraw.Draw(img)
    
    # Border
    border = max(2, size // 32)
    draw.rounded_rectangle(
        [border, border, size - border, size - border],
        radius=size // 8,
        outline=(0, 240, 255, 255),
        width=max(2, size // 64)
    )
    
    # Draw >_ prompt
    font_size = size // 3
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    text = ">_"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) // 2
    y = (size - th) // 2 - size // 16
    draw.text((x, y), text, fill=(0, 240, 255, 255), font=font)
    
    return img

def create_icns(images, path):
    """Create a macOS .icns file from a dict of {size: PIL.Image}."""
    # Simple ICNS using PNG format entries
    icon_types = {
        32: b'icp4',   # 16x16@2x
        64: b'icp5',   # 32x32@2x  
        128: b'ic07',   # 128x128
        256: b'ic08',   # 256x256
        512: b'ic09',   # 512x512
        1024: b'ic10',  # 512x512@2x
    }
    
    entries = []
    for size, img in sorted(images.items()):
        if size in icon_types:
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            png_data = buf.getvalue()
            icon_type = icon_types[size]
            entry_size = len(png_data) + 8
            entries.append(icon_type + struct.pack('>I', entry_size) + png_data)
    
    body = b''.join(entries)
    total = len(body) + 8
    icns_data = b'icns' + struct.pack('>I', total) + body
    
    with open(path, 'wb') as f:
        f.write(icns_data)

def create_ico(images, path):
    """Create a Windows .ico file."""
    sizes = [16, 32, 48, 256]
    ico_images = []
    for s in sizes:
        if s in images:
            ico_images.append(images[s])
        else:
            closest = min(images.keys(), key=lambda x: abs(x - s))
            ico_images.append(images[closest].resize((s, s), Image.LANCZOS))
    ico_images[0].save(path, format='ICO', sizes=[(img.width, img.height) for img in ico_images], append_images=ico_images[1:])

# Generate all sizes
sizes = [16, 32, 64, 128, 256, 512, 1024]
images = {}
for s in sizes:
    images[s] = create_icon(s)

# Save individual PNGs
images[32].save("src-tauri/icons/32x32.png")
images[128].save("src-tauri/icons/128x128.png")
images[256].save("src-tauri/icons/128x128@2x.png")

# Save ICNS and ICO
create_icns(images, "src-tauri/icons/icon.icns")
create_ico(images, "src-tauri/icons/icon.ico")

print("Icons generated successfully.")
