import re
from typing import List

class ValidationError(Exception):
    """Exception levée lorsqu'une validation échoue"""
    pass

class EmailValidator:
    """Validateur d'email avec regex robuste"""
    
    @staticmethod
    def validate(email: str) -> bool:
        """
        Valide un email selon le standard RFC 5322 (version simplifiée)
        """
        if not email or len(email) < 5:
            raise ValidationError("L'email doit contenir au moins 5 caractères")
        
        # Regex pour validation d'email (version robuste mais simplifiée)
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            raise ValidationError("Format d'email invalide")
        
        # Vérifications supplémentaires
        if email.count('@') != 1:
            raise ValidationError("L'email doit contenir exactement un @")
        
        local_part, domain = email.split('@')
        
        # Vérification de la partie locale (avant @)
        if len(local_part) > 64:
            raise ValidationError("La partie locale de l'email est trop longue (max 64 caractères)")
        
        # Vérification du domaine
        if len(domain) > 253:
            raise ValidationError("Le domaine de l'email est trop long (max 253 caractères)")
        
        return True

class PasswordValidator:
    """Validateur de mot de passe avec règles de sécurité renforcées"""
    
    MIN_LENGTH = 8
    
    @staticmethod
    def validate(password: str) -> bool:
        """
        Valide un mot de passe selon les critères de sécurité :
        - Au moins 8 caractères
        - Au moins 1 minuscule
        - Au moins 1 majuscule  
        - Au moins 1 chiffre
        - Au moins 1 caractère spécial
        """
        errors = []
        
        # Vérification de la longueur
        if len(password) < PasswordValidator.MIN_LENGTH:
            errors.append(f"Le mot de passe doit contenir au moins {PasswordValidator.MIN_LENGTH} caractères")
        
        # Vérification des minuscules
        if not re.search(r'[a-z]', password):
            errors.append("Le mot de passe doit contenir au moins une lettre minuscule")
        
        # Vérification des majuscules
        if not re.search(r'[A-Z]', password):
            errors.append("Le mot de passe doit contenir au moins une lettre majuscule")
        
        # Vérification des chiffres
        if not re.search(r'\d', password):
            errors.append("Le mot de passe doit contenir au moins un chiffre")
        
        # Vérification des caractères spéciaux
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Le mot de passe doit contenir au moins un caractère spécial (!@#$%^&*(),.?\":{}|<>)")
        
        # Si des erreurs existent, les lever
        if errors:
            raise ValidationError(" ; ".join(errors))
        
        return True
    
    @staticmethod
    def get_strength_score(password: str) -> int:
        """
        Retourne un score de robustesse du mot de passe (0-100)
        """
        score = 0
        
        # Longueur
        if len(password) >= 8:
            score += 25
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10
        
        # Complexité
        if re.search(r'[a-z]', password):
            score += 15
        if re.search(r'[A-Z]', password):
            score += 15
        if re.search(r'\d', password):
            score += 15
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 20
        
        return min(score, 100)

class UserValidator:
    """Validateur global pour les données utilisateur"""
    
    @staticmethod
    def validate_user_creation(email: str, username: str, password: str) -> bool:
        """
        Valide toutes les données nécessaires à la création d'un utilisateur
        """
        # Validation de l'email
        EmailValidator.validate(email)
        
        # Validation du nom d'utilisateur
        if not username or len(username.strip()) < 3:
            raise ValidationError("Le nom d'utilisateur doit contenir au moins 3 caractères")
        
        if len(username) > 50:
            raise ValidationError("Le nom d'utilisateur ne peut pas dépasser 50 caractères")
        
        # Caractères autorisés pour le nom d'utilisateur (lettres, chiffres, underscore, tiret)
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise ValidationError("Le nom d'utilisateur ne peut contenir que des lettres, chiffres, underscore et tirets")
        
        # Validation du mot de passe
        PasswordValidator.validate(password)
        
        return True