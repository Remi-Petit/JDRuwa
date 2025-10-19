"""
Guide d'utilisation des hooks SQLAlchemy pour le hashage automatique des mots de passe

Votre modèle User dispose maintenant de plusieurs mécanismes pour gérer les mots de passe :
"""

# ============================================================================
# APPROCHES DISPONIBLES DANS VOTRE MODÈLE USER
# ============================================================================

from app.db.models.user import User

def examples():
    """Exemples d'utilisation des différentes approches"""
    
    # ============================================================================
    # 1. APPROCHE AVEC PROPRIÉTÉ SETTER (RECOMMANDÉE)
    # ============================================================================
    print("1. Approche avec propriété setter :")
    user = User(email="user@example.com", username="testuser")
    
    # Le hashage se fait automatiquement via le setter
    user.password = "MonMotDePasse123!"
    
    print(f"   - Mot de passe hashé automatiquement")
    print(f"   - Hash commence par: {user.hashed_password[:20]}...")
    
    # ============================================================================
    # 2. APPROCHE AVEC MÉTHODE SET_PASSWORD
    # ============================================================================
    print("\n2. Approche avec méthode set_password :")
    user2 = User(email="user2@example.com", username="testuser2")
    
    # Utilise l'attribut temporaire _new_password pour le hook
    user2.set_password("AutreMotDePasse456!")
    
    print(f"   - Méthode set_password() définie")
    print(f"   - Attribut temporaire _new_password créé")
    print(f"   - Le hash sera appliqué lors de la sauvegarde en DB")
    
    # ============================================================================
    # 3. VÉRIFICATION DES MOTS DE PASSE
    # ============================================================================
    print("\n3. Vérification des mots de passe :")
    
    # Correct
    if user.verify_password("MonMotDePasse123!"):
        print("   - Mot de passe correct : VALIDE")
    
    # Incorrect  
    if not user.verify_password("MauvaisMotDePasse"):
        print("   - Mot de passe incorrect : REJETÉ")
    
    # ============================================================================
    # 4. SÉCURITÉ - LECTURE INTERDITE
    # ============================================================================
    print("\n4. Sécurité - propriété password protégée :")
    try:
        password_value = user.password
        print("   - ERREUR : password accessible en lecture")
    except AttributeError:
        print("   - OK : propriété password protégée contre la lecture")

if __name__ == "__main__":
    examples()
    
    print("\n" + "="*70)
    print("UTILISATION DANS VOTRE CODE:")
    print("="*70)
    
    print("""
# Dans UserRepository.create() :
user = User(email=email, username=username)
user.password = password  # <- Hashage automatique !
db.add(user)
await db.commit()

# Dans auth_resolvers.py :
user = await UserRepository.get_by_email(db, email)
if user and user.verify_password(password):  # <- Méthode du modèle !
    return create_access_token(str(user.id))

# Plus besoin de hashage manuel dans les services !
    """)
    
    print("="*70)
    print("AVANTAGES DE CETTE APPROCHE:")
    print("="*70)
    print("""
✓ Hashage automatique et transparent
✓ Sécurité renforcée (password non lisible)  
✓ Code plus propre (moins de logique dans les services)
✓ Hooks SQLAlchemy pour une gestion cohérente
✓ Méthodes de vérification intégrées au modèle
✓ Approche orientée objet et encapsulation
    """)