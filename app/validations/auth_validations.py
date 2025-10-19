"""Validateurs pour l'authentification"""

from .user_validations import ValidationError

class LoginValidator:
    """Validateur pour les données de connexion"""
    
    @staticmethod
    def validate_login_data(email: str, password: str) -> bool:
        """
        Valide les données de connexion
        """
        if not email or not email.strip():
            raise ValidationError("L'email est requis pour la connexion")
        
        if not password or not password.strip():
            raise ValidationError("Le mot de passe est requis pour la connexion")
        
        return True