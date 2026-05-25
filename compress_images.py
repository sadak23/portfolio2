import os
from PIL import Image

def compress_images():
    base_dir = r"C:\Users\Dell Workstation\Downloads\website\SADAK_PORTFOLIO\WEBSITE_FILES\SADAK_PORTFOLIO_WEBSITE_FINAL_V3_MORE_PAGES"
    image_dirs = [
        os.path.join(base_dir, "images", "architecture", "exterior"),
        os.path.join(base_dir, "images", "architecture", "interior"),
        os.path.join(base_dir, "images", "events"),
        os.path.join(base_dir, "images", "exhibition")
    ]
    
    total_original_size = 0
    total_compressed_size = 0
    converted_count = 0
    
    for img_dir in image_dirs:
        if not os.path.exists(img_dir):
            print(f"Directory not found: {img_dir}")
            continue
        
        print(f"\nProcessing directory: {img_dir}")
        for file_name in os.listdir(img_dir):
            if file_name.lower().endswith('.png'):
                png_path = os.path.join(img_dir, file_name)
                webp_name = os.path.splitext(file_name)[0] + '.webp'
                webp_path = os.path.join(img_dir, webp_name)
                
                orig_size = os.path.getsize(png_path)
                total_original_size += orig_size
                
                try:
                    with Image.open(png_path) as img:
                        # Convert RGBA to RGB if saving to a format that doesn't support transparency,
                        # but WebP supports transparency, so we can save it directly.
                        img.save(webp_path, 'WEBP', quality=82, method=6)
                    
                    comp_size = os.path.getsize(webp_path)
                    total_compressed_size += comp_size
                    converted_count += 1
                    
                    # Remove the original PNG
                    os.remove(png_path)
                    
                    ratio = (comp_size / orig_size) * 100
                    print(f"Compressed {file_name} -> {webp_name} ({orig_size/1024/1024:.2f}MB -> {comp_size/1024/1024:.2f}MB, {ratio:.1f}%)")
                except Exception as e:
                    print(f"Error compressing {file_name}: {e}")
                    
    print("\n--- COMPRESSION SUMMARY ---")
    print(f"Total files converted: {converted_count}")
    print(f"Original total size: {total_original_size/1024/1024:.2f} MB")
    print(f"Compressed total size: {total_compressed_size/1024/1024:.2f} MB")
    if total_original_size > 0:
        reduction = (1 - total_compressed_size/total_original_size) * 100
        print(f"Space Saved: {reduction:.2f}%")

if __name__ == "__main__":
    compress_images()
