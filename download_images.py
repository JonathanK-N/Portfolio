import requests
import os

def download_image(url, filename, folder):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"  > {filename}")
        return True
    except Exception as e:
        print(f"  Erreur {filename}: {e}")
        return False

def download_all_images():
    os.makedirs('static/images/gallery', exist_ok=True)
    os.makedirs('static/images/services', exist_ok=True)
    
    # Images Unsplash haute qualité
    gallery_images = [
        # Portraits
        ('portrait-1.jpg', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop'),
        ('portrait-2.jpg', 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=800&h=600&fit=crop'),
        ('portrait-3.jpg', 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=800&h=600&fit=crop'),
        ('portrait-4.jpg', 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=800&h=600&fit=crop'),
        
        # Mariages
        ('mariage-1.jpg', 'https://images.unsplash.com/photo-1519741497674-611481863552?w=800&h=600&fit=crop'),
        ('mariage-2.jpg', 'https://images.unsplash.com/photo-1606216794074-735e91aa2c92?w=800&h=600&fit=crop'),
        ('mariage-3.jpg', 'https://images.unsplash.com/photo-1583939003579-730e3918a45a?w=800&h=600&fit=crop'),
        ('mariage-4.jpg', 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=800&h=600&fit=crop'),
        
        # Nature
        ('nature-1.jpg', 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop'),
        ('nature-2.jpg', 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=600&fit=crop'),
        ('nature-3.jpg', 'https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?w=800&h=600&fit=crop'),
        ('nature-4.jpg', 'https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=800&h=600&fit=crop'),
        
        # Architecture
        ('architecture-1.jpg', 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=600&fit=crop'),
        ('architecture-2.jpg', 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop'),
        ('architecture-3.jpg', 'https://images.unsplash.com/photo-1518005020951-eccb494ad742?w=800&h=600&fit=crop'),
        ('architecture-4.jpg', 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&h=600&fit=crop'),
        
        # Mode
        ('mode-1.jpg', 'https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=800&h=600&fit=crop'),
        ('mode-2.jpg', 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&h=600&fit=crop'),
        ('mode-3.jpg', 'https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=800&h=600&fit=crop'),
        ('mode-4.jpg', 'https://images.unsplash.com/photo-1581044777550-4cfa60707c03?w=800&h=600&fit=crop'),
        
        # Événements
        ('evenement-1.jpg', 'https://images.unsplash.com/photo-1511578314322-379afb476865?w=800&h=600&fit=crop'),
        ('evenement-2.jpg', 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800&h=600&fit=crop'),
        ('evenement-3.jpg', 'https://images.unsplash.com/photo-1505373877841-8d25f7d46678?w=800&h=600&fit=crop'),
        ('evenement-4.jpg', 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&h=600&fit=crop')
    ]
    
    print("Telechargement des images de galerie...")
    for filename, url in gallery_images:
        download_image(url, filename, 'static/images/gallery')
    
    service_images = [
        ('portrait.jpg', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=400&fit=crop'),
        ('mariage.jpg', 'https://images.unsplash.com/photo-1519741497674-611481863552?w=600&h=400&fit=crop'),
        ('evenement.jpg', 'https://images.unsplash.com/photo-1511578314322-379afb476865?w=600&h=400&fit=crop'),
        ('famille.jpg', 'https://images.unsplash.com/photo-1511895426328-dc8714191300?w=600&h=400&fit=crop')
    ]
    
    print("\nTelechargement des images de services...")
    for filename, url in service_images:
        download_image(url, filename, 'static/images/services')
    
    special_images = [
        ('hero-bg.jpg', 'https://images.unsplash.com/photo-1452587925148-ce544e77e70d?w=1920&h=1080&fit=crop'),
        ('services-bg.jpg', 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1920&h=800&fit=crop'),
        ('about-photo.jpg', 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=600&h=800&fit=crop'),
        ('hero-photo.jpg', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=600&h=800&fit=crop')
    ]
    
    print("\nTelechargement des images speciales...")
    for filename, url in special_images:
        download_image(url, filename, 'static/images')
    
    print("\n> Toutes les vraies images ont ete telechargees !")

if __name__ == "__main__":
    download_all_images()