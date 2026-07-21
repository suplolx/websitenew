#!/usr/bin/env python3
import os
import sys
import math
import argparse
import urllib.request
from PIL import Image, ImageDraw, ImageFont

# Default Settings
FONT_URLS = [
    "https://raw.githubusercontent.com/Outfitio/Outfit-Fonts/master/fonts/ttf/Outfit-Bold.ttf",
    "https://raw.githubusercontent.com/google/fonts/main/ofl/outfit/Outfit%5Bwght%5D.ttf",
    "https://github.com/anthropics/skills/raw/main/skills/canvas-design/canvas-fonts/Outfit-Bold.ttf",
    "https://github.com/hoangvu12/kaguya-app/raw/master/assets/fonts/Outfit-Bold.ttf"
]
DEFAULT_FONT_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "Outfit-Bold.ttf")

def download_font(target_path):
    """Try to download the Outfit font from multiple sources if not present."""
    if os.path.exists(target_path):
        return True
    
    print(f"Downloading beautiful Outfit font from open-source mirrors...")
    for url in FONT_URLS:
        try:
            # Request with a standard User-Agent to avoid blocker filters
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                with open(target_path, 'wb') as out_file:
                    out_file.write(response.read())
            print(f"Font successfully saved to {target_path} (source: {url})")
            return True
        except Exception as e:
            # Try next url
            continue
            
    print("Warning: Could not download Outfit font from any mirror.")
    return False

def parse_hex_color(hex_str):
    """Parse hex color strings like '#ffffff', 'fff', or 'ffffff' into an RGB tuple."""
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join([c*2 for c in hex_str])
    if len(hex_str) != 6:
        raise ValueError(f"Invalid hex color format: {hex_str}")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def interpolate_color(c1, c2, t):
    """Interpolate between two RGB colors c1 and c2 by factor t (0.0 to 1.0)."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def get_font(font_path, font_size):
    """Loads specified font, falls back to common system fonts, then default font."""
    # 1. Try downloaded/specified font path
    if font_path and os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, font_size)
        except Exception:
            pass

    # 2. Try default Outfit font locally
    if os.path.exists(DEFAULT_FONT_NAME):
        try:
            return ImageFont.truetype(DEFAULT_FONT_NAME, font_size)
        except Exception:
            pass

    # 3. Try common Windows/Mac system font locations
    system_fonts = [
        "calibrib.ttf", "arialbd.ttf", "segoeuib.ttf",  # Windows
        "/Library/Fonts/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc",  # macOS
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Linux
    ]
    for font_name in system_fonts:
        try:
            return ImageFont.truetype(font_name, font_size)
        except Exception:
            # If Windows, search C:\Windows\Fonts directly
            if sys.platform == 'win32' and not font_name.startswith('/'):
                win_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts', font_name)
                if os.path.exists(win_path):
                    try:
                        return ImageFont.truetype(win_path, font_size)
                    except Exception:
                        pass
            continue
            
    # 4. Fallback
    print("Warning: Using system default monospace font (may look basic).")
    return ImageFont.load_default()

def create_initials_avatar(
    initials="J",
    resolution=(980, 1200),
    start_color="#84cc16",
    end_color="#16a34a",
    angle=120,
    circle_radius=330,
    text_color="#ffffff",
    bg_color="#ffffff",
    font_size=380,
    text_offset_y=0,
    font_path=DEFAULT_FONT_NAME
):
    w, h = resolution
    
    # 1. Parse colors
    c_start = parse_hex_color(start_color)
    c_end = parse_hex_color(c_start if end_color is None else end_color)
    c_text = parse_hex_color(text_color)
    
    # Check background type
    is_transparent = bg_color.lower() == 'transparent'
    c_bg = (0, 0, 0, 0) if is_transparent else parse_hex_color(bg_color)
    
    # 2. Setup background canvas
    canvas_mode = 'RGBA' if is_transparent else 'RGB'
    canvas = Image.new(canvas_mode, (w, h), c_bg)
    
    # 3. Create Circle Gradient Layer
    # We create a square layer larger than the circle diameter to support rotation cleanly
    D = circle_radius * 2
    # Diagonal size of the square
    size = int(D * 1.5)
    
    # Create horizontal linear gradient
    gradient_1d = Image.new('RGB', (size, 1))
    for x in range(size):
        t = x / (size - 1) if size > 1 else 0
        gradient_1d.putpixel((x, 0), interpolate_color(c_start, c_end, t))
    gradient_2d = gradient_1d.resize((size, size))
    
    # Rotate the gradient
    # PIL rotates counter-clockwise. To align with CSS angle behavior (clockwise from top):
    # - We rotate by (180 - angle) or standard adjustments
    pil_angle = (90 - angle) % 360
    rotated_grad = gradient_2d.rotate(pil_angle, resample=Image.Resampling.BILINEAR)
    
    # Crop the center D x D square
    left = (size - D) // 2
    top = (size - D) // 2
    cropped_grad = rotated_grad.crop((left, top, left + D, top + D))
    
    # Create circle alpha mask
    mask = Image.new('L', (D, D), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, D, D), fill=255)
    
    # Assemble circle layer (RGBA to support transparency overlay)
    circle_layer = Image.new('RGBA', (D, D), (0, 0, 0, 0))
    circle_layer.paste(cropped_grad, (0, 0), mask=mask)
    
    # Paste circle onto canvas center
    cx = w // 2
    cy = h // 2
    canvas.paste(circle_layer, (cx - circle_radius, cy - circle_radius), mask=circle_layer)
    
    # 4. Draw initials text
    # Draw context (must be RGBA to support transparent backgrounds or anti-aliasing)
    draw_canvas = canvas if canvas.mode == 'RGBA' else canvas.convert('RGBA')
    draw = ImageDraw.Draw(draw_canvas)
    
    # Load Font
    font = get_font(font_path, font_size)
    
    # Standard text position
    # Offset by 3% of font size for perfect visual balance (aligning with React canvas offset)
    visual_adjust = text_offset_y + int(font_size * 0.03)
    text_y = cy + visual_adjust
    
    # Draw text exactly centered using anchor='mm' (middle-middle)
    # Note: anchor='mm' requires a TrueType/OpenType font to center correctly.
    try:
        draw.text((cx, text_y), initials.upper(), fill=c_text, font=font, anchor="mm")
    except Exception:
        # Fallback if font doesn't support anchors
        # Estimate text bounding box
        left, top, right, bottom = draw.textbbox((0, 0), initials.upper(), font=font)
        text_w = right - left
        text_h = bottom - top
        draw.text((cx - text_w // 2, cy - text_h // 2 + visual_adjust), initials.upper(), fill=c_text, font=font)
        
    # Convert back to RGB if background is solid (non-transparent) for smaller file sizes
    if not is_transparent:
        canvas = draw_canvas.convert('RGB')
    else:
        canvas = draw_canvas

    return canvas

def main():
    parser = argparse.ArgumentParser(
        description="Elegant Initials Avatar Generator (980x1200 pixel portraits)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-i", "--initials", type=str, default="J", help="Initials text (1-3 chars)")
    parser.add_argument("-o", "--output", type=str, default="avatar.png", help="Output file name")
    parser.add_argument("-r", "--resolution", type=str, default="980x1200", help="Resolution width x height")
    parser.add_argument("--start-color", type=str, default="#84cc16", help="Gradient start color (Hex)")
    parser.add_argument("--end-color", type=str, default="#16a34a", help="Gradient end color (Hex)")
    parser.add_argument("--angle", type=int, default=120, help="Gradient angle in degrees (0-360)")
    parser.add_argument("--radius", type=int, default=330, help="Circle radius in pixels")
    parser.add_argument("--text-color", type=str, default="#ffffff", help="Initials text color (Hex)")
    parser.add_argument("--bg-color", type=str, default="#ffffff", help="Canvas background color (Hex or 'transparent')")
    parser.add_argument("--font-size", type=int, default=380, help="Text font size in pixels")
    parser.add_argument("--offset-y", type=int, default=0, help="Vertical text offset adjustment")
    parser.add_argument("--font", type=str, default=DEFAULT_FONT_NAME, help="Custom TTF font path")
    
    args = parser.parse_args()
    
    # 1. Make sure initials are limited
    initials_str = args.initials[:3]
    
    # 2. Parse resolution
    try:
        res = tuple(map(int, args.resolution.lower().split('x')))
        if len(res) != 2:
            raise ValueError()
    except Exception:
        print("Error: Resolution must be in the format 'WIDTHxHEIGHT', e.g., '980x1200'.")
        sys.exit(1)
        
    # 3. Attempt font download
    download_font(DEFAULT_FONT_NAME)
    
    # 4. Generate avatar
    try:
        avatar = create_initials_avatar(
            initials=initials_str,
            resolution=res,
            start_color=args.start_color,
            end_color=args.end_color,
            angle=args.angle,
            circle_radius=args.radius,
            text_color=args.text_color,
            bg_color=args.bg_color,
            font_size=args.font_size,
            text_offset_y=args.offset_y,
            font_path=args.font
        )
        
        # 5. Save output
        avatar.save(args.output)
        print(f"Success! Elegant avatar generated and saved to: {args.output}")
        print(f"Dimensions: {res[0]}x{res[1]} px | Initials: '{initials_str}'")
    except Exception as e:
        print(f"Error generating avatar: {e}")
        print("Ensure you have Pillow installed: 'pip install Pillow'")
        sys.exit(1)

if __name__ == "__main__":
    main()
