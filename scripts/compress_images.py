import hashlib
import json
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


def get_file_hash(file_path):
    """Calculate MD5 hash of a file."""
    hasher = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None


def load_cache(cache_file):
    """Load the compression cache from disk."""
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not read cache ({e}), starting fresh.")
            return {}
    return {}


def save_cache(cache_file, cache):
    """Save the compression cache to disk."""
    try:
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save cache ({e})")


def should_compress(file_path, rel_path, cache):
    """Determine if a file needs compression based on cache and file attributes."""
    if rel_path not in cache:
        return True

    cached = cache[rel_path]
    current_mtime = os.path.getmtime(file_path)
    current_size = os.path.getsize(file_path)

    # Quick check: mtime and size match
    if cached.get("mtime") == current_mtime and cached.get("size") == current_size:
        return False

    # Deep check: if mtime/size changed, check if MD5 hash is still the same
    current_hash = get_file_hash(file_path)
    if cached.get("hash") and cached.get("hash") == current_hash:
        # File content unchanged, update mtime & size in cache
        cached["mtime"] = current_mtime
        cached["size"] = current_size
        return False

    return True


def compress_image(file_path, rel_path, cache, max_dimension=1200, quality=85):
    """Resize and compress an image, then update the cache."""
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
            img.save(file_path, optimize=True)
        else:
            img.save(file_path, optimize=True)

        new_size = os.path.getsize(file_path)
        new_mtime = os.path.getmtime(file_path)
        new_hash = get_file_hash(file_path)

        # Update cache entry
        cache[rel_path] = {
            "mtime": new_mtime,
            "size": new_size,
            "hash": new_hash
        }

        savings = (original_size - new_size) / original_size * 100 if original_size > 0 else 0
        print(f"Compressed {os.path.basename(file_path)}: {original_size/1024/1024:.2f}MB -> {new_size/1024/1024:.2f}MB ({savings:.1f}% saved)")
    except Exception as e:
        print(f"Error compressing {file_path}: {e}")


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(project_root, 'assets')
    cache_dir = os.path.join(project_root, '.cache')
    cache_file = os.path.join(cache_dir, 'image-compress-cache.json')

    if not os.path.exists(assets_dir):
        print(f"Assets directory not found at {assets_dir}")
        return

    cache = load_cache(cache_file)

    print(f"Scanning directory: {assets_dir}")
    processed_count = 0
    skipped_count = 0

    for root, dirs, files in os.walk(assets_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png']:
                full_path = os.path.join(root, file)
                # Skip tiny files like logos or small icons under 50KB
                if os.path.getsize(full_path) <= 50 * 1024:
                    continue

                rel_path = os.path.relpath(full_path, project_root).replace('\\', '/')

                if should_compress(full_path, rel_path, cache):
                    compress_image(full_path, rel_path, cache)
                    processed_count += 1
                else:
                    skipped_count += 1

    # Prune deleted files from cache
    cache = {k: v for k, v in cache.items() if os.path.exists(os.path.join(project_root, k))}
    save_cache(cache_file, cache)

    print(f"\nDone! {processed_count} compressed, {skipped_count} skipped (unchanged).")


if __name__ == '__main__':
    main()
