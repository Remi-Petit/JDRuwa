import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { AppRouterCacheProvider } from '@mui/material-nextjs/v15-appRouter';
import theme from './theme';
import { ApolloWrapper } from './apollo-wrapper';
import { AuthProvider } from '../lib/auth-context';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "JDRuwa",
  description: "Application JDRuwa - Gestion et découverte de jeux de rôle",
};

export default function RootLayout({ children }) {
  return (
    <html lang="fr">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <ApolloWrapper>
          <AppRouterCacheProvider>
            <ThemeProvider theme={theme}>
              <CssBaseline />
              <AuthProvider>
                {children}
              </AuthProvider>
            </ThemeProvider>
          </AppRouterCacheProvider>
        </ApolloWrapper>
      </body>
    </html>
  );
}
