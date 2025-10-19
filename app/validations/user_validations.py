import re

class ValidationError(Exception):
    """Exception levée lorsqu'une validation échoue"""
    pass


class EmailValidator:
    """Validateur d'email avec règles explicites"""

    @staticmethod
    def validate(email: str) -> bool:
        """
        Valide un email selon des règles usuelles:
        - exact. 1 '@'
        - parties locale et domaine non vides
        - pas de '..' dans local ou domaine
        - domaine ne commence/termine pas par '.'
        - domaine avec au moins un point (TLD)
        - labels de domaine: [A-Za-z0-9-], 1..63, pas commencer/finir par '-'
        - TLD: seulement lettres, longueur >= 2
        - local-part: [A-Za-z0-9._%+-], 1..64, ne commence/termine pas par '.'
        - longueurs max: local <= 64, domain <= 253
        """
        if not isinstance(email, str) or not email:
            raise ValidationError("Email requis")

        # 1 seul '@'
        if email.count("@") != 1:
            raise ValidationError("Format d'email invalide")

        local_part, domain = email.split("@", 1)

        # Parties non vides
        if not local_part or not domain:
            raise ValidationError("Format d'email invalide")

        # Pas de double point
        if ".." in local_part or ".." in domain:
            raise ValidationError("Format d'email invalide")

        # Domaine ne commence/termine pas par '.'
        if domain.startswith(".") or domain.endswith("."):
            raise ValidationError("Format d'email invalide")

        # Domaine doit contenir un point (TLD)
        labels = domain.split(".")
        if len(labels) < 2:
            raise ValidationError("Format d'email invalide")

        # Chaque label du domaine
        label_re = re.compile(r"^[A-Za-z0-9-]{1,63}$")
        for label in labels:
            if not label or not label_re.match(label):
                raise ValidationError("Format d'email invalide")
            if label.startswith("-") or label.endswith("-"):
                raise ValidationError("Format d'email invalide")

        # TLD: lettres uniquement, au moins 2
        if not re.fullmatch(r"[A-Za-z]{2,}", labels[-1]):
            raise ValidationError("Format d'email invalide")

        # Local-part: caractères autorisés, et ne commence/termine pas par '.'
        if not re.fullmatch(r"[A-Za-z0-9._%+-]{1,64}", local_part):
            raise ValidationError("Format d'email invalide")
        if local_part.startswith(".") or local_part.endswith("."):
            raise ValidationError("Format d'email invalide")

        # Longueurs
        if len(local_part) > 64 or len(domain) > 253:
            raise ValidationError("Format d'email invalide")

        return True


class PasswordValidator:
    """Validateur de mot de passe avec règles de sécurité renforcées"""

    MIN_LENGTH = 8

    @staticmethod
    def validate(password: str) -> bool:
        """
        Valide un mot de passe selon les critères:
        - Au moins 8 caractères
        - Au moins 1 minuscule
        - Au moins 1 majuscule
        - Au moins 1 chiffre
        - Au moins 1 caractère spécial (liste sûre)
        - Refuse explicitement ' " ` ; \ /
        """
        if not isinstance(password, str):
            raise ValidationError("Mot de passe invalide")

        errors = []

        # Longueur
        if len(password) < PasswordValidator.MIN_LENGTH:
            errors.append(f"Le mot de passe doit contenir au moins {PasswordValidator.MIN_LENGTH} caractères")

        # Minuscules
        if not re.search(r"[a-z]", password):
            errors.append("Le mot de passe doit contenir au moins une lettre minuscule")

        # Majuscules
        if not re.search(r"[A-Z]", password):
            errors.append("Le mot de passe doit contenir au moins une lettre majuscule")

        # Chiffres
        if not re.search(r"\d", password):
            errors.append("Le mot de passe doit contenir au moins un chiffre")

        # Caractères spéciaux sûrs (pas de quotes/backticks/;\/)
        safe_special_chars = r"[!@#$%^&*(),.?:{}|<>=+_]"
        if not re.search(safe_special_chars, password):
            errors.append("Le mot de passe doit contenir au moins un caractère spécial (!@#$%^&*(),.?:{}|<>=+_)")

        # Caractères dangereux interdits
        dangerous_chars = r"[\'\"`;\\/]"
        if re.search(dangerous_chars, password):
            errors.append("Le mot de passe ne peut pas contenir les caractères suivants : ' \" ` ; \\ /")

        if errors:
            raise ValidationError(" ; ".join(errors))

        return True

    @staticmethod
    def get_strength_score(password: str) -> int:
        """
        Retourne un score de robustesse du mot de passe (0-100)
        """
        if not isinstance(password, str):
            return 0

        score = 0

        # Longueur
        if len(password) >= 8:
            score += 25
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10

        # Complexité
        if re.search(r"[a-z]", password):
            score += 15
        if re.search(r"[A-Z]", password):
            score += 15
        if re.search(r"\d", password):
            score += 15
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            score += 20

        return min(score, 100)


class UserValidator:
    """Validateur global pour les données utilisateur"""

    @staticmethod
    def validate_user_creation(email: str, username: str, password: str) -> bool:
        """
        Valide toutes les données nécessaires à la création d'un utilisateur
        """
        # Email
        EmailValidator.validate(email)

        # Username
        if not isinstance(username, str) or not username.strip():
            raise ValidationError("Le nom d'utilisateur est requis")

        if len(username.strip()) < 3:
            raise ValidationError("Le nom d'utilisateur doit contenir au moins 3 caractères")

        if len(username) > 50:
            raise ValidationError("Le nom d'utilisateur ne peut pas dépasser 50 caractères")

        # Caractères autorisés: lettres, chiffres, underscore, tiret
        if not re.fullmatch(r"[A-Za-z0-9_-]+", username):
            raise ValidationError("Le nom d'utilisateur ne peut contenir que des lettres, chiffres, underscore et tirets")

        # Mot de passe
        PasswordValidator.validate(password)

        return True