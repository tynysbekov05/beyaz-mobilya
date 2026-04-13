import os
import re
import urllib.parse

def get_images(folder_paths):
    images = []
    base_dir = "/Users/kaisartynysbekov/new-beyaz/Website-Intelligence/site/assets"
    for folder_path in folder_paths:
        full_folder_path = os.path.join(base_dir, folder_path)
        if not os.path.exists(full_folder_path):
            continue
        files = [f for f in os.listdir(full_folder_path) if f.endswith(("webp", "jpg", "png"))]
        files.sort()
        for f in files:
            rel_path = os.path.relpath(os.path.join(full_folder_path, f), base_dir)
            images.append(f"assets/{urllib.parse.quote(rel_path)}")
    return images

def generate_product_html(title, images):
    if not images:
        return ""
    
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

def replace_grid(filepath, new_content):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # We replace everything inside <div class="collection-grid"> ... </div>
    pattern = re.compile(r'(<div class="collection-grid">)(.*?)(</section>)', re.DOTALL)
    
    replacement = r'\1' + new_content + r'\n        </div>\n    \3'
    new_page = pattern.sub(replacement, content)
    
    with open(filepath, 'w') as f:
        f.write(new_page)

# Yatak Odaları
yatak_html = ""
yatak_html += generate_product_html("Lizbon Yatak Odası", get_images(["lizbon-yatak"]))
yatak_html += generate_product_html("Roza Yatak Odası", get_images(["roza-yatak"]))
yatak_html += generate_product_html("Bernido Akkor Yatak Odası", get_images(["bernido-3types/bernido-akkor-yatak"]))
yatak_html += generate_product_html("Bernido Capella Yatak Odası", get_images(["bernido-3types/bernido-capella-yatak"]))
yatak_html += generate_product_html("Bernido Nergis Yatak Odası", get_images(["bernido-3types/berndio-nergis-yatak"]))

replace_grid("/Users/kaisartynysbekov/new-beyaz/Website-Intelligence/site/yatak-odalari.html", yatak_html)

# Yemek Odaları
yemek_html = ""
yemek_html += generate_product_html("Lizbon Yemek Odası", get_images(["lizbon-yemek"]))
yemek_html += generate_product_html("Bernido Akkor Yemek Odası", get_images(["bernido-3types/bernido-akkor-yemek"]))
yemek_html += generate_product_html("Bernido Capella Yemek Odası", get_images(["bernido-3types/bernido-capella-yemek"]))
yemek_html += generate_product_html("Bernido Nergis Yemek Odası", get_images(["bernido-3types/bernido-nergis-yemek"]))

replace_grid("/Users/kaisartynysbekov/new-beyaz/Website-Intelligence/site/yemek-odalari.html", yemek_html)

# Koltuk Takımları
koltuk_html = ""
koltuk_html += generate_product_html("Bernido Akkor Koltuk Takımı", get_images(["bernido-3types/bernido-akkor-koltuk"]))
koltuk_html += generate_product_html("Bernido Capella Koltuk Takımı", get_images(["bernido-3types/bernido-capella-koltuk"]))

replace_grid("/Users/kaisartynysbekov/new-beyaz/Website-Intelligence/site/koltuk-takimlari.html", koltuk_html)

print("HTML generation complete.")
