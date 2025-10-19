'use client';
import { useAuth } from '../../lib/auth-context';
import { Container, Typography, Paper, Box, Button } from '@mui/material';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/');
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom color="primary">
          Dashboard JDRuwa
        </Typography>
        
        <Typography variant="h6" gutterBottom>
          Bienvenue, {user?.firstName || 'Utilisateur'} !
        </Typography>

        <Box sx={{ mt: 3 }}>
          <Typography variant="body1">
            <strong>Email:</strong> {user?.email}
          </Typography>
          <Typography variant="body1">
            <strong>Nom:</strong> {user?.firstName} {user?.lastName}
          </Typography>
        </Box>

        <Box sx={{ mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            Fonctionnalités à venir :
          </Typography>
          <ul>
            <li>Gestion des campagnes JDR</li>
            <li>Création de personnages</li>
            <li>Recherche de groupes</li>
            <li>Calendrier des sessions</li>
          </ul>
        </Box>

        <Box sx={{ mt: 4 }}>
          <Button variant="outlined" color="secondary" onClick={handleLogout}>
            Se déconnecter
          </Button>
        </Box>
      </Paper>
    </Container>
  );
}