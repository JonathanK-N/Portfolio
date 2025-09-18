#!/usr/bin/env python3
"""
Script de test pour vérifier si l'IA OpenAI fonctionne
"""
import os
from openai import OpenAI

def test_openai():
    api_key = os.environ.get('OPENAI_API_KEY')
    
    print("=== TEST OPENAI ===")
    print(f"Clé API présente: {bool(api_key)}")
    
    if not api_key:
        print("❌ Aucune clé API OpenAI trouvée")
        print("Ajoutez OPENAI_API_KEY dans vos variables d'environnement")
        return False
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Test simple
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": "Réponds juste 'OK' si tu me reçois"
                }
            ],
            max_tokens=5
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ OpenAI répond: {result}")
        print("✅ L'IA est fonctionnelle")
        return True
        
    except Exception as e:
        print(f"❌ Erreur OpenAI: {e}")
        return False

if __name__ == "__main__":
    test_openai()