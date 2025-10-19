import { gql } from '@apollo/client';

// Type Input pour l'inscription
export const REGISTER_INPUT = gql`
  input RegisterInput {
    firstName: String!
    lastName: String!
    email: String!
    password: String!
  }
`;

// Fragments réutilisables
export const USER_FRAGMENT = gql`
  fragment UserInfo on User {
    id
    email
    firstName
    lastName
    createdAt
    updatedAt
  }
`;

export const AUTH_RESPONSE_FRAGMENT = gql`
  fragment AuthResponse on AuthPayload {
    token
    user {
      ...UserInfo
    }
  }
  ${USER_FRAGMENT}
`;