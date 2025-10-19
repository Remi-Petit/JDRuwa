"""
Tests des nouvelles validations de sécurité pour les utilisateurs
"""
import pytest
from app.core.validators import EmailValidator, PasswordValidator, UserValidator, ValidationError

class TestEmailValidator:
    def test_valid_emails(self):
        """Test avec des emails valides"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.org",
            "user+tag@example.co.uk",
            "firstname.lastname@company.com"
        ]
        
        for email in valid_emails:
            assert EmailValidator.validate(email) == True
    
    def test_invalid_emails(self):
        """Test avec des emails invalides"""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "user@",
            "user@.com",
            "user..double.dot@example.com",
            ""
        ]
        
        for email in invalid_emails:
            with pytest.raises(ValidationError):
                EmailValidator.validate(email)

class TestPasswordValidator:
    def test_valid_passwords(self):
        """Test avec des mots de passe valides"""
        valid_passwords = [
            "MonMotDePasse123!",
            "Secure@Password1",
            "MyStr0ng#Pass",
            "Complex!Password2023"
        ]
        
        for password in valid_passwords:
            assert PasswordValidator.validate(password) == True
    
    def test_invalid_passwords(self):
        """Test avec des mots de passe invalides"""
        invalid_cases = [
            ("short", "Le mot de passe doit contenir au moins 8 caractères"),
            ("nouppercase123!", "majuscule"),
            ("NOLOWERCASE123!", "minuscule"),
            ("NoNumbers!", "chiffre"),
            ("NoSpecialChar123", "caractère spécial")
        ]
        
        for password, expected_error in invalid_cases:
            with pytest.raises(ValidationError) as exc_info:
                PasswordValidator.validate(password)
            assert expected_error.lower() in str(exc_info.value).lower()
    
    def test_password_strength_score(self):
        """Test du calcul de force du mot de passe"""
        # Mot de passe faible
        weak_score = PasswordValidator.get_strength_score("abc")
        assert weak_score < 50
        
        # Mot de passe fort
        strong_score = PasswordValidator.get_strength_score("MonMotDePasse123!")
        assert strong_score >= 80

class TestUserValidator:
    def test_valid_user_creation(self):
        """Test avec des données utilisateur valides"""
        assert UserValidator.validate_user_creation(
            email="test@example.com",
            username="testuser",
            password="MonMotDePasse123!"
        ) == True
    
    def test_invalid_username(self):
        """Test avec des noms d'utilisateur invalides"""
        invalid_usernames = [
            ("ab", "au moins 3 caractères"),  # Trop court
            ("user with spaces", "lettres, chiffres, underscore"),  # Espaces
            ("user@domain", "lettres, chiffres, underscore"),  # Caractères interdits
            ("a" * 51, "ne peut pas dépasser 50 caractères")  # Trop long
        ]
        
        for username, expected_error in invalid_usernames:
            with pytest.raises(ValidationError) as exc_info:
                UserValidator.validate_user_creation(
                    email="test@example.com",
                    username=username,
                    password="MonMotDePasse123!"
                )
            assert expected_error.lower() in str(exc_info.value).lower()

if __name__ == "__main__":
    # Tests rapides en mode script
    print("🧪 Test des validateurs...")
    
    try:
        # Test email valide
        EmailValidator.validate("test@example.com")
        print("✅ Email valide : OK")
        
        # Test mot de passe fort
        PasswordValidator.validate("MonMotDePasse123!")
        print("✅ Mot de passe fort : OK")
        
        # Test utilisateur valide
        UserValidator.validate_user_creation("test@example.com", "testuser", "MonMotDePasse123!")
        print("✅ Utilisateur valide : OK")
        
        # Test mot de passe faible
        try:
            PasswordValidator.validate("123")
            print("❌ Erreur : mot de passe faible accepté")
        except ValidationError:
            print("✅ Mot de passe faible rejeté : OK")
        
        print("\n🎉 Tous les tests passent !")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")