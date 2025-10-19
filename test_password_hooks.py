"""
Test des hooks SQLAlchemy pour le hashage automatique des mots de passe
"""

async def test_automatic_password_hashing():
    """
    Test que les hooks SQLAlchemy hashent automatiquement les mots de passe
    """
    from app.db.models.user import User
    from passlib.hash import argon2
    
    # Test 1: Propriété password avec setter
    print("Test 1: Propriété password avec setter")
    user = User(email="test@example.com", username="testuser")
    
    # Assigner le mot de passe via la propriété
    user.password = "MonMotDePasse123!"
    
    # Vérifier que le mot de passe a été hashé
    assert user.hashed_password is not None
    assert user.hashed_password != "MonMotDePasse123!"
    assert argon2.verify("MonMotDePasse123!", user.hashed_password)
    print("✓ Setter automatique fonctionne")
    
    # Test 2: Méthode verify_password
    print("\nTest 2: Méthode verify_password du modèle")
    assert user.verify_password("MonMotDePasse123!")
    assert not user.verify_password("mauvais-mot-de-passe")
    print("✓ Vérification de mot de passe fonctionne")
    
    # Test 3: Propriété password non accessible en lecture
    print("\nTest 3: Sécurité - password non accessible en lecture")
    try:
        _ = user.password
        assert False, "La propriété password ne devrait pas être accessible en lecture"
    except AttributeError:
        print("✓ Propriété password protégée en lecture")
    
    print("\n🎉 Tous les tests passent !")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_automatic_password_hashing())