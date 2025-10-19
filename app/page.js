'use client';
import Image from "next/image";
import { Container, Typography, Box, Button, Stack, Paper } from '@mui/material';
import { Login as LoginIcon, PersonAdd as PersonAddIcon, SportsEsports as GameIcon } from '@mui/icons-material';
import Link from 'next/link';

export default function Home() {
  return (
    <Container maxWidth="lg">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 4,
          py: 4,
        }}
      >
        {/* Header avec logo */}
        <Paper 
          elevation={2}
          sx={{ 
            p: 4, 
            textAlign: 'center',
            maxWidth: 600,
            width: '100%',
          }}
        >
          <Box sx={{ mb: 3 }}>
            <GameIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
            <Typography variant="h2" component="h1" gutterBottom color="primary">
              JDRuwa
            </Typography>
            <Typography variant="h6" color="text.secondary" sx={{ mb: 3 }}>
              Votre plateforme pour découvrir et gérer vos jeux de rôle
            </Typography>
          </Box>

          {/* Description */}
          <Typography variant="body1" sx={{ mb: 4, lineHeight: 1.6 }}>
            Plongez dans l'univers fascinant des jeux de rôle ! 
            Découvrez de nouveaux mondes, créez vos personnages et 
            vivez des aventures épiques avec votre communauté.
          </Typography>

          {/* Boutons d'action */}
          <Stack 
            direction={{ xs: 'column', sm: 'row' }} 
            spacing={2} 
            justifyContent="center"
            sx={{ mb: 3 }}
          >
            <Button
              component={Link}
              href="/login"
              variant="contained"
              size="large"
              startIcon={<LoginIcon />}
              sx={{ minWidth: 160 }}
            >
              Se connecter
            </Button>
            
            <Button
              component={Link}
              href="/register"
              variant="outlined"
              size="large"
              startIcon={<PersonAddIcon />}
              sx={{ minWidth: 160 }}
            >
              S'inscrire
            </Button>
          </Stack>
        </Paper>

        {/* Fonctionnalités */}
        <Box sx={{ width: '100%', maxWidth: 800 }}>
          <Typography variant="h5" textAlign="center" gutterBottom sx={{ mb: 3 }}>
            Fonctionnalités
          </Typography>
          
          <Stack 
            direction={{ xs: 'column', md: 'row' }} 
            spacing={3}
          >
            <Paper elevation={1} sx={{ p: 3, flex: 1, textAlign: 'center' }}>
              <Typography variant="h6" gutterBottom color="primary">
                🎲 Gestion de campagnes
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Organisez vos sessions, suivez vos personnages et gardez un historique de vos aventures.
              </Typography>
            </Paper>

            <Paper elevation={1} sx={{ p: 3, flex: 1, textAlign: 'center' }}>
              <Typography variant="h6" gutterBottom color="primary">
                👥 Communauté
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Trouvez des joueurs, rejoignez des groupes et partagez vos expériences.
              </Typography>
            </Paper>

            <Paper elevation={1} sx={{ p: 3, flex: 1, textAlign: 'center' }}>
              <Typography variant="h6" gutterBottom color="primary">
                📚 Base de données
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Accédez à une vaste collection de systèmes de jeu et d'univers.
              </Typography>
            </Paper>
          </Stack>
        </Box>
      </Box>
    </Container>
  );
}
