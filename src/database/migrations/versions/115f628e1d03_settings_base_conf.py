"""settings-base-conf

Revision ID: 115f628e1d03
Revises: 364cfff3dd87
Create Date: 2024-11-02 21:20:36.474107

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import Integer, String

# revision identifiers, used by Alembic.
revision: str = '115f628e1d03'
down_revision: Union[str, None] = '364cfff3dd87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define a temporary table structure to use for inserts
settings_table = table(
    'settings',
    column('id', Integer),
    column('dynamic_button_count', Integer),
    column('welcome_message', String)
)


def upgrade() -> None:
    # Use op.bulk_insert to insert initial data without raw SQL
    op.bulk_insert(settings_table, [
        {
            'id': 1,
            'dynamic_button_count': 2,
            'welcome_message': (
                '🤖 {{NAME}} ({{USERNAME}})...connecting to «IT Lobby Irkutsk». '
                'Вошёл, за своё aйти пояснил. Программист, инженер, робототехник, '
                'сис.админ или каким-то образом связан с IT и технологиями, '
                'то расскажи о себе и своей деятельности.'
            )
        }
    ])


def downgrade() -> None:
    # Use op.delete to remove rows from the settings table
    op.execute(
        settings_table.delete().where(settings_table.c.id == 1)
    )
