"""Initial schema: create users, memories, interactions, memory_summaries

Revision ID: 001
Revises:
Create Date: 2026-04-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("last_interaction", sa.DateTime(), nullable=True),
        sa.Column("interaction_count", sa.Integer(), nullable=True, default=0),
        sa.Column("total_interactions", sa.Integer(), nullable=True, default=0),
        sa.Column("humor_level", sa.String(), nullable=True, default="medium"),
        sa.Column("response_length", sa.String(), nullable=True, default="medium"),
        sa.Column("formality", sa.String(), nullable=True, default="casual"),
        sa.Column("language_mix", sa.String(), nullable=True, default="hinglish"),
        sa.Column("emoji_usage", sa.String(), nullable=True, default="moderate"),
        sa.Column("communication_style", sa.String(), nullable=True,
                  default="casual"),
        sa.Column("learned_patterns", sa.JSON(), nullable=True),
        sa.Column("topics_of_interest", sa.JSON(), nullable=True),
        sa.Column("emotional_baseline", sa.String(), nullable=True, default="neutral"),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_users_user_id", "users", ["user_id"])

    op.create_table(
        "memories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("pattern", sa.Text(), nullable=True),
        sa.Column("observation", sa.Text(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_memories_user_id", "memories", ["user_id"])

    op.create_table(
        "interactions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("scenario", sa.String(), nullable=True),
        sa.Column("emotion", sa.String(), nullable=True),
        sa.Column("mode", sa.String(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("type", sa.String(), nullable=True, default="interaction_log"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_interactions_user_id", "interactions", ["user_id"])

    op.create_table(
        "memory_summaries",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("traits_identified", sa.JSON(), nullable=True),
        sa.Column("signals", sa.JSON(), nullable=True),
        sa.Column("type", sa.String(), nullable=True, default="trait_update"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_memory_summaries_user_id", "memory_summaries", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_memory_summaries_user_id", table_name="memory_summaries")
    op.drop_table("memory_summaries")
    op.drop_index("ix_interactions_user_id", table_name="interactions")
    op.drop_table("interactions")
    op.drop_index("ix_memories_user_id", table_name="memories")
    op.drop_table("memories")
    op.drop_index("ix_users_user_id", table_name="users")
    op.drop_table("users")
