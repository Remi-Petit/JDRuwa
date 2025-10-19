import pytest
from app.validations import EmailValidator, PasswordValidator, UserValidator, ValidationError

class TestEmailValidator:
    def test_valid_emails(self):
        valid_emails = [
            "test@example.com",
            "user.name@domain.org",
            "user+tag@example.co.uk",
            "firstname.lastname@company.com",
            "user123@test-domain.com",
        ]
        for email in valid_emails:
            assert EmailValidator.validate(email) is True

    def test_invalid_emails(self):
        invalid_emails = [
            "invalid-email",            # pas de @
            "@example.com",             # pas de partie locale
            "user@",                    # pas de domaine
            "user@.com",                # domaine commence par .
            "user..double@example.com", # double point
            "",                         # vide
            "a@b",                      # trop court
            "user@domain",              # pas d'extension
        ]
        for email in invalid_emails:
            with pytest.raises(ValidationError):
                EmailValidator.validate(email)

class TestPasswordValidator:
    def test_valid_passwords(self):
        valid_passwords = [
            "MonMotDePasse123!",
            "Secure@Password1",
            "MyStr0ng#Pass",
            "Complex!Password2023",
            "Test123+Password",
        ]
        for pwd in valid_passwords:
            assert PasswordValidator.validate(pwd) is True

    def test_invalid_passwords_length_lower_upper_digit_special(self):
        with pytest.raises(ValidationError):
            PasswordValidator.validate("Short1!")          # trop court
        with pytest.raises(ValidationError):
            PasswordValidator.validate("PASSWORD123!")     # pas de minuscule
        with pytest.raises(ValidationError):
            PasswordValidator.validate("password123!")     # pas de majuscule
        with pytest.raises(ValidationError):
            PasswordValidator.validate("Password!")        # pas de chiffre
        with pytest.raises(ValidationError):
            PasswordValidator.validate("Password123")      # pas de caractère spécial

    def test_dangerous_characters_rejected(self):
        # Ces mots de passe doivent être refusés si vous excluez ' " ` ; \ /
        dangerous_passwords = [
            "Password123'",
            'Password123"',
            "Password123`",
            "Password123;",
            "Password123\\",
            "Password123/",
        ]
        for pwd in dangerous_passwords:
            with pytest.raises(ValidationError):
                PasswordValidator.validate(pwd)

    def test_password_strength_score(self):
        weak = PasswordValidator.get_strength_score("abc")
        medium = PasswordValidator.get_strength_score("Password123")
        strong = PasswordValidator.get_strength_score("MonMotDePasse123!")
        assert isinstance(weak, int) and isinstance(medium, int) and isinstance(strong, int)
        assert weak < 30
        assert 40 <= medium < 80
        assert strong >= 80

class TestUserValidator:
    def test_valid_user_creation(self):
        assert UserValidator.validate_user_creation(
            email="test@example.com",
            username="test_user-123",
            password="MonMotDePasse123!"
        ) is True

    def test_username_too_short(self):
        with pytest.raises(ValidationError):
            UserValidator.validate_user_creation(
                email="test@example.com",
                username="ab",
                password="MonMotDePasse123!"
            )

    def test_username_too_long(self):
        with pytest.raises(ValidationError):
            UserValidator.validate_user_creation(
                email="test@example.com",
                username="a" * 51,
                password="MonMotDePasse123!"
            )

    def test_username_invalid_characters(self):
        invalid_usernames = [
            "user name",    # espace
            "user@name",    # @
            "user.name",    # .
            "user#name",    # #
            "user+name",    # +
        ]
        for username in invalid_usernames:
            with pytest.raises(ValidationError):
                UserValidator.validate_user_creation(
                    email="test@example.com",
                    username=username,
                    password="MonMotDePasse123!"
                )