# Guide d'intégration GraphQL avec Apollo Client

## ✅ Configuration terminée

Votre application Next.js est maintenant configurée pour communiquer avec votre API GraphQL !

## 📁 Structure créée

```
lib/
├── apollo-client.js       # Configuration Apollo Client
├── auth-context.js        # Context d'authentification React
└── graphql/
    ├── auth.js           # Mutations et queries d'authentification
    └── fragments.js      # Fragments GraphQL réutilisables

app/
├── apollo-wrapper.js     # Wrapper Apollo pour Next.js 15
├── layout.js            # Layout mis à jour avec providers
├── login/page.js        # Page de connexion avec Apollo
└── register/page.js     # Page d'inscription avec Apollo
```

## 🔧 Configuration requise

### 1. Variables d'environnement
Configurez l'URL de votre API dans `.env.local` :
```bash
NEXT_PUBLIC_GRAPHQL_URL=http://localhost:4000/graphql
```

### 2. Schéma GraphQL attendu
Vos mutations GraphQL doivent correspondre à :

**Login :**
```graphql
mutation Login($email: String!, $password: String!) {
  login(email: $email, password: $password) {
    token
    user {
      id
      email
      firstName
      lastName
      createdAt
    }
  }
}
```

**Register :**
```graphql
mutation Register($input: RegisterInput!) {
  register(input: $input) {
    token
    user {
      id
      email
      firstName
      lastName
      createdAt
    }
  }
}
```

**Input Type :**
```graphql
input RegisterInput {
  firstName: String!
  lastName: String!
  email: String!
  password: String!
}
```

## 🚀 Fonctionnalités disponibles

### Authentification
- ✅ Connexion avec Apollo Client
- ✅ Inscription avec validation
- ✅ Gestion automatique des tokens JWT
- ✅ Context React pour l'état d'authentification
- ✅ Gestion des erreurs GraphQL
- ✅ Redirection automatique après authentification

### Sécurité
- ✅ Headers d'autorisation automatiques
- ✅ Gestion des erreurs 401 (déconnexion auto)
- ✅ Stockage sécurisé des tokens (localStorage)
- ✅ Validation côté client

## 🔨 Utilisation

### Dans vos composants
```javascript
import { useAuth } from '../lib/auth-context';
import { useMutation, useQuery } from '@apollo/client';

function MyComponent() {
  const { user, logout, isAuthenticated } = useAuth();
  
  // Vos queries et mutations GraphQL ici
}
```

### Ajouter de nouvelles queries/mutations
1. Créez vos queries dans `lib/graphql/`
2. Utilisez `useQuery` ou `useMutation` dans vos composants
3. Les headers d'authentification sont automatiquement ajoutés

## 🛠️ Prochaines étapes suggérées

1. **Page Dashboard** - Créer une page protégée après connexion
2. **Middleware de protection** - Protéger les routes privées
3. **Profil utilisateur** - Gestion du profil avec GraphQL
4. **Refresh tokens** - Gestion du renouvellement des tokens
5. **Tests** - Ajouter des tests pour l'authentification

## 🔍 Debug

### Vérifier la connexion
1. Ouvrez la console du navigateur
2. Les erreurs GraphQL sont loggées automatiquement
3. Apollo Client DevTools disponible en extension Chrome

### Variables d'environnement
Vérifiez que `NEXT_PUBLIC_GRAPHQL_URL` est bien définie et accessible depuis le client.

---

**🎯 Votre app est prête à communiquer avec votre API GraphQL !**