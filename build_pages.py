import os
import json
import re
import urllib.parse

def get_images(folder_paths):
    images = []
    base_dir = "/Users/kaisartynysbekov/new-beyaz/Website-Intelligence/site/assets"
    for folder_path in folder_paths:
        full_folder_path = os.path.join(base_dir, folder_path)
        if not os.path.exists(full_folder_path):
            continue
        files = [f for f in os.listdir(full_folder_path) if f.endswith(("webp", "jpg", "png", "jpeg"))]
        files.sort()
        for f in files:
            rel_path = os.path.relpath(os.path.join(full_folder_path, f), base_dir)
            images.append(f"assets/{urllib.parse.quote(rel_path)}")
    return images

def generate_product_html(item):
    title = item.get("title", "")
    folder = item.get("folder", "")
    images = get_images([folder])
    
    if not images:
        # Provide a fallback placeholder if no images are found
        images = ["assets/placeholder.webp"]

    html = f"""
            <!-- Product: {title} -->
            <div class="col-item gsap-fade-up">
                <div class="p-card-carousel">"""
    
    for i, img in enumerate(images):
        active_class = " active" if i == 0 else ""
        html += f"""
                    <img src="{img}" class="p-card-slide{active_class}" alt="{title}">"""
    
    display_arrows = "" if len(images) > 1 else " style=\"display:none;\""
    html += f"""
                    <button class="p-card-arrow prev"{display_arrows}>‹</button>
                    <button class="p-card-arrow next"{display_arrows}>›</button>
                </div>
                <div class="p-card-info">
                    <h3>{title}</h3>
                    <ul class="p-card-features">
                        <li>Premium Malzeme Kalitesi</li>
                        <li>Modern ve Şık Tasarım</li>
                        <li>Özel Koleksiyon Serisi</li>
                    </ul>
                    <a href="https://wa.me/905424785431?text=Merhaba,%20{urllib.parse.quote(title)}%20hakkında%20fiyat%20ve%20bilgi%20almak%20istiyorum." target="_blank" class="btn-whatsapp-outline">Hızlı Fiyat Al</a>
                </div>
            </div>"""
    return html

def generate_campaign_html(item):
    title = item.get("title", "")
    desc = item.get("description", "")
    features = item.get("features", [])
    image = item.get("image", "")
    wa_text = item.get("whatsapp_text", "Merhaba, kampanyalar hakkında bilgi almak istiyorum.")
    
    html = f"""
            <!-- Campaign: {title} -->
            <div class="col-item gsap-fade-up" style="max-width: 800px; margin: 0 auto 2rem auto; display: block; border: 2px solid var(--primary); border-radius: 12px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">
                <div style="position: relative;">
                    <img src="{image}" style="width: 100%; height: auto; display: block;" alt="{title}" onerror="this.src='assets/yatak-oda.png'">
                    <div style="position: absolute; top: 1rem; right: 1rem; background: var(--primary); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold; font-size: 0.9rem;">Aktif Fırsat</div>
                </div>
                <div class="p-card-info" style="padding: 2rem;">
                    <h3 style="font-size: 1.8rem; margin-bottom: 1rem;">{title}</h3>
                    <p style="color: #666; margin-bottom: 1.5rem; line-height: 1.6;">{desc}</p>
                    <ul class="p-card-features" style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-bottom: 2rem;">"""
    for feat in features:
        html += f"""
                        <li style="border:none; padding: 0.5rem 0; font-weight: 500;">✓ {feat}</li>"""
    
    html += f"""
                    </ul>
                    <a href="https://wa.me/905424785431?text={urllib.parse.quote(wa_text)}" target="_blank" class="btn-primary" style="display: block; text-align: center; width: 100%;">Kampanyadan Yararlan</a>
                </div>
            </div>"""
    return html

def replace_grid(filepath, new_content):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # We replace everything inside <div class="collection-grid"> ... </div>
    pattern = re.compile(r'(<div class="collection-grid">)(.*?)(</div>\s*</section>)', re.DOTALL)
    
    # Ensure the replacement preserves the grid container
    replacement = r'\1\n' + new_content + r'\n        \3'
    new_page = pattern.sub(replacement, content)
    
    with open(filepath, 'w') as f:
        f.write(new_page)

def main():
    base_dir = "/Users/kaisartynysbekov/new-beyaz/Website-Intelligence/site"
    data_file = os.path.join(base_dir, "data.json")
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 1. Yatak Odaları
    yatak_html = ""
    for item in data.get("yatak-odalari", []):
        yatak_html += generate_product_html(item)
    replace_grid(os.path.join(base_dir, "yatak-odalari.html"), yatak_html)
    
    # 2. Yemek Odaları
    yemek_html = ""
    for item in data.get("yemek-odalari", []):
        yemek_html += generate_product_html(item)
    replace_grid(os.path.join(base_dir, "yemek-odalari.html"), yemek_html)
    
    # 3. Koltuk Takımları
    koltuk_html = ""
    for item in data.get("koltuk-takimlari", []):
        koltuk_html += generate_product_html(item)
    replace_grid(os.path.join(base_dir, "koltuk-takimlari.html"), koltuk_html)
    
    # 4. Kampanyalar
    kampanyalar_html = ""
    for item in data.get("kampanyalar", []):
        kampanyalar_html += generate_campaign_html(item)
    
    # Notice: for campaigns we might just want to center them, so we can override grid styles slightly
    kampanyalar_html = f"""
        <div style="display: flex; flex-direction: column; gap: 2rem; width: 100%;">
            {kampanyalar_html}
        </div>
    """
    replace_grid(os.path.join(base_dir, "kampanyalar.html"), kampanyalar_html)
    
    print("HTML generation complete using data.json.")

if __name__ == "__main__":
    main()
