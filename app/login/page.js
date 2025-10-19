'use client';
import { useState } from 'react';
import { useMutation } from '@apollo/client';
import { useRouter } from 'next/navigation';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Link,
  Alert,
  InputAdornment,
  IconButton,
} from '@mui/material';
import {
  Email as EmailIcon,
  Lock as LockIcon,
  Visibility,
  VisibilityOff,
  Login as LoginIcon,
} from '@mui/icons-material';
import NextLink from 'next/link';
import { LOGIN_MUTATION } from '../../lib/graphql/auth';
import { useAuth } from '../../lib/auth-context';

export default function LoginPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  
  const router = useRouter();
  const { login } = useAuth();
  
  const [loginMutation, { loading }] = useMutation(LOGIN_MUTATION, {
    onCompleted: (data) => {
      if (data.login) {
        const token = data.login; // data.login est directement le token JWT
        
        // Créer un objet utilisateur temporaire avec les données du formulaire
        // En attendant de récupérer les vraies données depuis l'API
        const userData = {
          id: 'temp-id', // ID temporaire
          email: formData.email,
          firstName: 'Utilisateur', // Valeur par défaut
          lastName: 'Connecté', // Valeur par défaut
        };
        
        login(token, userData);
        router.push('/dashboard');
      }
    },
    onError: (error) => {
      console.error('Login error:', error);
      setError(
        error.graphQLErrors?.[0]?.message || 
        'Email ou mot de passe incorrect'
      );
    },
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.email || !formData.password) {
      setError('Veuillez remplir tous les champs');
      return;
    }

    try {
      await loginMutation({
        variables: {
          email: formData.email,
          password: formData.password,
        },
      });
    } catch (err) {
      console.error('Submit error:', err);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <Container component="main" maxWidth="sm">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          minHeight: '80vh',
        }}
      >
        <Paper
          elevation={3}
          sx={{
            padding: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            width: '100%',
            maxWidth: 400,
          }}
        >
          <Box sx={{ mb: 3, textAlign: 'center' }}>
            <Typography component="h1" variant="h4" gutterBottom color="primary">
              JDRuwa
            </Typography>
            <Typography variant="h6" color="text.secondary">
              Connexion
            </Typography>
          </Box>

          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1, width: '100%' }}>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email"
              name="email"
              autoComplete="email"
              autoFocus
              value={formData.email}
              onChange={handleChange}
              disabled={loading}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <EmailIcon color="action" />
                  </InputAdornment>
                ),
              }}
            />

            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Mot de passe"
              type={showPassword ? 'text' : 'password'}
              id="password"
              autoComplete="current-password"
              value={formData.password}
              onChange={handleChange}
              disabled={loading}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <LockIcon color="action" />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={togglePasswordVisibility}
                      edge="end"
                      disabled={loading}
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2, py: 1.5 }}
              disabled={loading}
              startIcon={<LoginIcon />}
            >
              {loading ? 'Connexion...' : 'Se connecter'}
            </Button>

            <Box sx={{ textAlign: 'center', mt: 2 }}>
              <Link component={NextLink} href="/register" variant="body2">
                Pas encore de compte ? S'inscrire
              </Link>
            </Box>

            <Box sx={{ textAlign: 'center', mt: 1 }}>
              <Link component={NextLink} href="/" variant="body2" color="text.secondary">
                Retour à l'accueil
              </Link>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}