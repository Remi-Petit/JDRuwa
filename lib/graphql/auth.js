import { gql } from '@apollo/client';

// Mutation pour la connexion (retourne directement le token)
export const LOGIN_MUTATION = gql`
  mutation Login($email: String!, $password: String!) {
    login(email: $email, password: $password)
  }
`;

// Mutation pour l'inscription (retourne directement le token)
export const REGISTER_MUTATION = gql`
  mutation Register($input: RegisterInput!) {
    register(input: $input)
  }
`;

// Query pour récupérer le profil utilisateur
export const GET_ME = gql`
  query GetMe {
    me {
      id
      email
      firstName
      lastName
      createdAt
      updatedAt
    }
  }
`;

// Query pour vérifier si l'utilisateur est connecté
export const IS_AUTHENTICATED = gql`
  query IsAuthenticated {
    isAuthenticated
  }
`;