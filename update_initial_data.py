import json
import os
import re

def update_data():
    base_dir = r"C:\Users\Dell Workstation\Downloads\website\SADAK_PORTFOLIO\WEBSITE_FILES\SADAK_PORTFOLIO_WEBSITE_FINAL_V3_MORE_PAGES"
    js_path = os.path.join(base_dir, "portfolio-data.js")
    
    with open(js_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Extract JSON string
    match = re.search(r"const PORTFOLIO_DATA = (\{.*?\});", content, re.DOTALL)
    if not match:
        print("Could not find PORTFOLIO_DATA in JS file.")
        return
        
    data = json.loads(match.group(1))
    
    # Define our updates mapping (key is image path, value is dict of new values)
    updates = {
        # Events
        "images/events/event-01.webp": {"category": "Opening Ceremony", "title": "Parachuting Championship Stage"},
        "images/events/event-02.webp": {"category": "Islamic Event", "title": "Holy Quran Recitation Award Stage"},
        "images/events/event-03.webp": {"category": "Islamic Event", "title": "Quran Recitation Stage - Blue Atmosphere"},
        "images/events/event-04.webp": {"category": "VIP Lounge", "title": "Islamic Conference of Labour Ministers Reception"},
        "images/events/event-05.webp": {"category": "Conference", "title": "ARABAL Annual Conference Stage Set"},
        "images/events/event-06.webp": {"category": "Summit", "title": "6th Global Ministerial Summit on Mental Health"},
        "images/events/event-07.webp": {"category": "Heritage Festival", "title": "Zayed Heritage Festival National Day Show"},
        "images/events/event-08.webp": {"category": "Award Ceremony", "title": "Sheikh Zayed Book Award Ceremony"},
        "images/events/event-09.webp": {"category": "Award Ceremony", "title": "HIPA Photography Award Ceremony"},
        "images/events/event-10.webp": {"category": "Hospitality Lounge", "title": "Catering Event Lounge Concept"},
        "images/events/event-11.webp": {"category": "Corporate Event", "title": "Qatar Airways Celebration Stage"},
        "images/events/event-12.webp": {"category": "Award Stage", "title": "OAG Group of Companies Award Stage"},
        
        # Exhibition
        "images/exhibition/exhibition-001.webp": {"category": "Exhibition Pavilion", "title": "Mubadala Defense Expo Pavilion"},
        "images/exhibition/exhibition-002.webp": {"category": "Exhibition Masterplan", "title": "Mubadala Exhibition Stand 3D Layout"},
        "images/exhibition/exhibition-003.webp": {"category": "Exhibition Booth", "title": "Mwani Qatar Ports Exhibition Stand"},
        "images/exhibition/exhibition-004.webp": {"category": "Exhibition Booth", "title": "Mwani Qatar Ports Exhibition Stand (Alternate Angle)"},
        "images/exhibition/exhibition-005.webp": {"category": "Exhibition Studio", "title": "Ooredoo Exhibition Talk Show Studio"},
        
        # Interior
        "images/architecture/interior/interior-02.webp": {"category": "Majlis", "title": "Arabic Luxury Outdoor Majlis"},
        "images/architecture/interior/interior-03.webp": {"category": "Executive Office", "title": "Luxury Office Lounge"},
        "images/architecture/interior/interior-04.webp": {"category": "Executive Office", "title": "Director's Suite Living Area"},
        "images/architecture/interior/interior-05.webp": {"category": "Banquet Hall", "title": "Grand Luxury Ballroom"},
        
        # Exterior
        "images/architecture/exterior/exterior-07.webp": {"category": "Villa", "title": "Geometric Modern Villa"},
        "images/architecture/exterior/exterior-08.webp": {"category": "Resort", "title": "Tropical Cliffside Resort"},
        "images/architecture/exterior/exterior-11.webp": {"category": "Residential", "title": "Mediterranean Townhouses"},
        "images/architecture/exterior/exterior-12.webp": {"category": "Villa", "title": "Contemporary Stone Villa"},
        "images/architecture/exterior/exterior-13.webp": {"category": "Villa Compound", "title": "Modern Luxury Townhouses"},
        "images/architecture/exterior/exterior-14.webp": {"category": "Residential", "title": "Modern Apartments Exterior"},
        "images/architecture/exterior/exterior-15.webp": {"category": "Luxury Tower", "title": "Skyline Daylight View"}
    }
    
    # Apply updates
    for section_name, items in data.items():
        for item in items:
            img_path = item["image"]
            if img_path in updates:
                item.update(updates[img_path])
                print(f"Updated {img_path} -> {item['category']} | {item['title']}")
                
    # Write back to JS
    js_content = f"// Centralized Portfolio Database\n// This file is loaded by the website and can be edited using admin.html\n\nconst PORTFOLIO_DATA = {json.dumps(data, indent=2)};\n"
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
        
    print("portfolio-data.js updated successfully with audited captions!")

if __name__ == "__main__":
    update_data()
