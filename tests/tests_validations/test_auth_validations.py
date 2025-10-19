import pytest
from app.validations.auth_validations import LoginValidator
from app.validations.user_validations import ValidationError

class TestLoginValidator:
    def test_valid_login(self):
        assert LoginValidator.validate_login_data("user@example.com", "Password123!") is True

    def test_missing_email(self):
        with pytest.raises(ValidationError):
            LoginValidator.validate_login_data("", "Password123!")
        with pytest.raises(ValidationError):
            LoginValidator.validate_login_data("   ", "Password123!")

    def test_missing_password(self):
        with pytest.raises(ValidationError):
            LoginValidator.validate_login_data("user@example.com", "")
        with pytest.raises(ValidationError):
            LoginValidator.validate_login_data("user@example.com", "   ")