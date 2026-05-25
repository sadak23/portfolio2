import os
import re
import json

def parse_and_generate():
    base_dir = r"C:\Users\Dell Workstation\Downloads\website\SADAK_PORTFOLIO\WEBSITE_FILES\SADAK_PORTFOLIO_WEBSITE_FINAL_V3_MORE_PAGES"
    html_files = {
        "index.html": "index",
        "exterior.html": "exterior",
        "interior.html": "interior",
        "events.html": "events",
        "exhibition.html": "exhibition"
    }
    
    # We want to find patterns like:
    # <article class="project-card [sizeClass] reveal"><img src="images/[path]" alt="..." />...<small>Category</small><h3>Title</h3></article>
    card_regex = re.compile(
        r'<article\s+class="project-card\s*([^"]*?)\s*reveal".*?>\s*<img\s+src="([^"]+)"[^>]*>.*?'
        r'<small>([^<]+)</small>.*?<h3>([^<]+)</h3>',
        re.DOTALL
    )
    
    # Let's first read index.html to find out which images are featured
    featured_images = set()
    index_path = os.path.join(base_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        matches = card_regex.findall(content)
        for size_class, img_path, cat, title in matches:
            img_path_clean = img_path.replace("\\", "/").replace(".png", ".webp").strip()
            featured_images.add(img_path_clean)
            
    print(f"Found {len(featured_images)} featured images on index page.")
    
    # Now parse the gallery files
    sections = {
        "exterior": [],
        "interior": [],
        "events": [],
        "exhibition": []
    }
    
    gallery_files = ["exterior.html", "interior.html", "events.html", "exhibition.html"]
    for g_file in gallery_files:
        section_name = g_file.split(".")[0] # exterior, interior, events, exhibition
        file_path = os.path.join(base_dir, g_file)
        if not os.path.exists(file_path):
            print(f"Gallery file not found: {g_file}")
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        matches = card_regex.findall(content)
        print(f"Parsed {len(matches)} cards in {g_file}")
        
        for size_class, img_path, cat, title in matches:
            img_path_clean = img_path.replace("\\", "/").replace(".png", ".webp").strip()
            
            # Clean up size class (remove reveal, keep large/wide)
            size_clean = ""
            if "large" in size_class:
                size_clean = "large"
            elif "wide" in size_class:
                size_clean = "wide"
                
            is_featured = img_path_clean in featured_images
            
            sections[section_name].append({
                "image": img_path_clean,
                "category": cat.strip(),
                "title": title.strip(),
                "sizeClass": size_clean,
                "featured": is_featured
            })
            
    # Write to portfolio-data.js
    js_content = f"// Centralized Portfolio Database\n// This file is loaded by the website and can be edited using admin.html\n\nconst PORTFOLIO_DATA = {json.dumps(sections, indent=2)};\n"
    
    js_path = os.path.join(base_dir, "portfolio-data.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print(f"Saved portfolio-data.js to {js_path}")

if __name__ == "__main__":
    parse_and_generate()
