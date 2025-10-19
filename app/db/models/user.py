from sqlalchemy import Column, Integer, String, DateTime, func, event
from sqlalchemy.ext.hybrid import hybrid_property
from passlib.hash import argon2
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    @hybrid_property
    def password(self):
        """
        La propriété password n'est jamais accessible en lecture pour des raisons de sécurité
        """
        raise AttributeError("Le mot de passe ne peut pas être lu")
    
    @password.setter
    def password(self, password: str):
        """
        Setter qui hash automatiquement le mot de passe avec Argon2
        """
        if password:
            self.hashed_password = argon2.hash(password)
    
    def verify_password(self, password: str) -> bool:
        """
        Vérifie un mot de passe contre son hash Argon2
        """
        return argon2.verify(password, self.hashed_password)
    
    def set_password(self, password: str):
        """
        Méthode pour définir un nouveau mot de passe
        Utilise l'attribut temporaire _new_password pour déclencher le hook
        """
        self._new_password = password


# Hook SQLAlchemy : Hash automatique avant insertion/mise à jour
@event.listens_for(User, 'before_insert')
@event.listens_for(User, 'before_update')
def hash_password_on_save(mapper, connection, target):
    """
    Hook SQLAlchemy qui s'exécute automatiquement avant chaque INSERT/UPDATE
    Si un attribut _new_password existe, il le hash et l'assigne à hashed_password
    """
    # Vérifier s'il y a un nouveau mot de passe à hasher
    if hasattr(target, '_new_password') and target._new_password:
        target.hashed_password = argon2.hash(target._new_password)
        # Nettoyer l'attribut temporaire
        delattr(target, '_new_password')
