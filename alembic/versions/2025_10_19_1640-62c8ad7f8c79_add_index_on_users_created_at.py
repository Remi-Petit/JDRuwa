"""Add index on users.created_at

Revision ID: 62c8ad7f8c79
Revises: 6b516408398c
Create Date: 2025-10-19 16:40:29.259777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62c8ad7f8c79'
down_revision: Union[str, Sequence[str], None] = '6b516408398c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Ajouter un index sur la colonne created_at pour améliorer les performances des requêtes de tri par date
    op.create_index('ix_users_created_at', 'users', ['created_at'])


def downgrade() -> None:
    """Downgrade schema."""
    # Supprimer l'index créé
    op.drop_index('ix_users_created_at', table_name='users')
