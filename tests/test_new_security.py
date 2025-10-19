"""
Tests d'intégration pour les nouvelles fonctionnalités de sécurité
"""

# Exemples de mutations GraphQL à tester

MUTATIONS_EXAMPLES = """
# ✅ Mutation valide - devrait fonctionner
mutation CreateValidUser {
  create_user(
    email: "user@example.com"
    username: "testuser123"
    password: "MonMotDePasse123!"
  ) {
    id
    email
    username
    created_at
  }
}

# ❌ Email invalide - devrait échouer
mutation CreateInvalidEmail {
  create_user(
    email: "email-invalide"
    username: "testuser"
    password: "MonMotDePasse123!"
  ) {
    id
    email
    username
  }
}

# ❌ Mot de passe faible - devrait échouer
mutation CreateWeakPassword {
  create_user(
    email: "user2@example.com"
    username: "testuser2"
    password: "123"
  ) {
    id
    email
    username
  }
}

# ❌ Username avec caractères interdits - devrait échouer
mutation CreateInvalidUsername {
  create_user(
    email: "user3@example.com"
    username: "test user@"
    password: "MonMotDePasse123!"
  ) {
    id
    email
    username
  }
}

# ✅ Login - devrait fonctionner après création d'utilisateur
mutation LoginUser {
  login(
    email: "user@example.com"
    password: "MonMotDePasse123!"
  )
}

# ✅ Requête me - devrait fonctionner avec token JWT
query GetCurrentUser {
  me {
    id
    email
    username
    created_at
  }
}
"""

print("Exemples de mutations GraphQL pour tester les nouvelles validations :")
print("=" * 70)
print(MUTATIONS_EXAMPLES)

print("\nÉtapes pour tester :")
print("1. Exécuter la migration : poetry run python migrate_username.py")
print("2. Démarrer le serveur : poetry run uvicorn main:app --host 0.0.0.0 --port 8200 --reload")
print("3. Aller sur http://localhost:8200/graphql")
print("4. Tester les mutations ci-dessus")