import os
import sys

try:
    from PIL import Image
except ImportError:
    print("Pillow is not installed. Installing it now...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image
    except Exception as e:
        print(f"Could not automatically install Pillow: {e}")
        print("Please run: pip install Pillow")
        sys.exit(1)

def compress_image(file_path, max_dimension=1200, quality=85):
    try:
        img = Image.open(file_path)
        original_size = os.path.getsize(file_path)
        
        # Check if resize is needed
        width, height = img.size
        if width > max_dimension or height > max_dimension:
            if width > height:
                new_width = max_dimension
                new_height = int(height * (max_dimension / width))
            else:
                new_height = max_dimension
                new_width = int(width * (max_dimension / height))
            
            # Resampling method fallback for older PIL versions
            resample_method = getattr(Image, "Resampling", None)
            if resample_method:
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            else:
                img = img.resize((new_width, new_height), Image.ANTIALIAS)
            print(f"Resized {os.path.basename(file_path)} from {width}x{height} to {new_width}x{new_height}")
        
        # Save back in original format
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext in ['.jpg', '.jpeg']:
            img.save(file_path, optimize=True, quality=quality)
        elif file_ext == '.png':
            # Optimize PNG. If it's a photo, converting to RGB and saving as JPEG can save even more,
            # but to keep the extension and HTML working we save as optimized PNG.
            img.save(file_path, optimize=True)
        else:
            img.save(file_path, optimize=True)
            
        new_size = os.path.getsize(file_path)
        savings = (original_size - new_size) / original_size * 100
        print(f"Compressed {os.path.basename(file_path)}: {original_size/1024/1024:.2f}MB -> {new_size/1024/1024:.2f}MB ({savings:.1f}% saved)")
    except Exception as e:
        print(f"Error compressing {file_path}: {e}")

def main():
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')
    if not os.path.exists(assets_dir):
        print(f"Assets directory not found at {assets_dir}")
        return
        
    print(f"Scanning directory: {assets_dir}")
    count = 0
    for root, dirs, files in os.walk(assets_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png']:
                full_path = os.path.join(root, file)
                # Skip tiny files like logos or small icons under 50KB
                if os.path.getsize(full_path) > 50 * 1024:
                    compress_image(full_path)
                    count += 1
                    
    print(f"\nDone! Processed {count} images.")

if __name__ == '__main__':
    main()
