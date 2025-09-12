import os
from PIL import Image, ImageDraw, ImageFont
import random

def create_professional_image(width, height, category, title, filename):
    colors = {
        'portrait': [(45, 52, 54), (99, 110, 114), (178, 190, 195)],
        'mariage': [(255, 234, 167), (250, 177, 160), (255, 118, 117)],
        'nature': [(46, 125, 50), (76, 175, 80), (129, 199, 132)],
        'architecture': [(55, 71, 79), (96, 125, 139), (144, 164, 174)],
        'mode': [(156, 39, 176), (233, 30, 99), (255, 64, 129)],
        'evenement': [(63, 81, 181), (92, 107, 192), (121, 134, 203)]
    }
    
    img = Image.new('RGB', (width, height), colors[category][0])
    draw = ImageDraw.Draw(img)
    
    for i in range(height):
        ratio = i / height
        r = int(colors[category][0][0] * (1 - ratio) + colors[category][1][0] * ratio)
        g = int(colors[category][0][1] * (1 - ratio) + colors[category][1][1] * ratio)
        b = int(colors[category][0][2] * (1 - ratio) + colors[category][1][2] * ratio)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    for _ in range(random.randint(3, 8)):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(x1, min(x1 + 200, width))
        y2 = random.randint(y1, min(y1 + 200, height))
        
        color = colors[category][2] + (random.randint(30, 80),)
        draw.ellipse([x1, y1, x2, y2], fill=color)
    
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 100))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    
    try:
        font_large = ImageFont.truetype("arial.ttf", 48)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), category.upper(), font=font_large)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 30
    
    draw.text((x + 2, y + 2), category.upper(), font=font_large, fill=(0, 0, 0, 180))
    draw.text((x, y), category.upper(), font=font_large, fill=(255, 255, 255))
    
    subtitle_bbox = draw.textbbox((0, 0), "PRiMA PHOTO", font=font_small)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    sx = (width - subtitle_width) // 2
    sy = y + text_height + 20
    
    draw.text((sx + 1, sy + 1), "PRiMA PHOTO", font=font_small, fill=(0, 0, 0, 120))
    draw.text((sx, sy), "PRiMA PHOTO", font=font_small, fill=(255, 255, 255, 200))
    
    return img

def generate_all_images():
    os.makedirs('static/images/gallery', exist_ok=True)
    os.makedirs('static/images/services', exist_ok=True)
    
    gallery_images = [
        ('portrait-1.jpg', 'portrait', 'Portrait Corporate'),
        ('portrait-2.jpg', 'portrait', 'Portrait Studio'),
        ('portrait-3.jpg', 'portrait', 'Portrait Femme'),
        ('portrait-4.jpg', 'portrait', 'Portrait Homme'),
        ('mariage-1.jpg', 'mariage', 'Ceremonie'),
        ('mariage-2.jpg', 'mariage', 'Premier Regard'),
        ('mariage-3.jpg', 'mariage', 'Echange Voeux'),
        ('mariage-4.jpg', 'mariage', 'Danse'),
        ('nature-1.jpg', 'nature', 'Montagne'),
        ('nature-2.jpg', 'nature', 'Foret'),
        ('nature-3.jpg', 'nature', 'Coucher Soleil'),
        ('nature-4.jpg', 'nature', 'Reflets'),
        ('architecture-1.jpg', 'architecture', 'Gratte-Ciel'),
        ('architecture-2.jpg', 'architecture', 'Details'),
        ('architecture-3.jpg', 'architecture', 'Perspective'),
        ('architecture-4.jpg', 'architecture', 'Ombres'),
        ('mode-1.jpg', 'mode', 'Editorial'),
        ('mode-2.jpg', 'mode', 'Street Style'),
        ('mode-3.jpg', 'mode', 'Haute Couture'),
        ('mode-4.jpg', 'mode', 'Lifestyle'),
        ('evenement-1.jpg', 'evenement', 'Corporate'),
        ('evenement-2.jpg', 'evenement', 'Gala'),
        ('evenement-3.jpg', 'evenement', 'Lancement'),
        ('evenement-4.jpg', 'evenement', 'Networking')
    ]
    
    print("Generation des images de galerie...")
    for filename, category, title in gallery_images:
        img = create_professional_image(800, 600, category, title, filename)
        img.save(f'static/images/gallery/{filename}', 'JPEG', quality=95)
        print(f"  > {filename}")
    
    service_images = [
        ('portrait.jpg', 'portrait', 'Service Portrait'),
        ('mariage.jpg', 'mariage', 'Service Mariage'),
        ('evenement.jpg', 'evenement', 'Service Evenement'),
        ('famille.jpg', 'portrait', 'Service Famille')
    ]
    
    print("\nGeneration des images de services...")
    for filename, category, title in service_images:
        img = create_professional_image(600, 400, category, title, filename)
        img.save(f'static/images/services/{filename}', 'JPEG', quality=95)
        print(f"  > {filename}")
    
    print("\nGeneration des images speciales...")
    
    hero_img = create_professional_image(1920, 1080, 'portrait', 'PRiMA PHOTO', 'hero-bg.jpg')
    hero_img.save('static/images/hero-bg.jpg', 'JPEG', quality=95)
    print("  > hero-bg.jpg")
    
    services_img = create_professional_image(1920, 800, 'architecture', 'SERVICES', 'services-bg.jpg')
    services_img.save('static/images/services-bg.jpg', 'JPEG', quality=95)
    print("  > services-bg.jpg")
    
    about_img = create_professional_image(600, 800, 'portrait', 'PHOTOGRAPHE', 'about-photo.jpg')
    about_img.save('static/images/about-photo.jpg', 'JPEG', quality=95)
    print("  > about-photo.jpg")
    
    hero_portrait = create_professional_image(600, 800, 'portrait', 'PRIMA', 'hero-photo.jpg')
    hero_portrait.save('static/images/hero-photo.jpg', 'JPEG', quality=95)
    print("  > hero-photo.jpg")
    
    print("\n> Toutes les images ont ete generees avec succes !")

if __name__ == "__main__":
    generate_all_images()