"""
SQLAlchemy ORM Models for Buddy AI PostgreSQL database.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_interaction = Column(DateTime, default=datetime.utcnow)
    interaction_count = Column(Integer, default=0)
    total_interactions = Column(Integer, default=0)

    # Preferences (flattened from MongoDB nested dict)
    humor_level = Column(String, default="medium")
    response_length = Column(String, default="medium")
    formality = Column(String, default="casual")
    language_mix = Column(String, default="hinglish")
    emoji_usage = Column(String, default="moderate")

    communication_style = Column(String, default="casual")
    learned_patterns = Column(JSON, default=list)
    topics_of_interest = Column(JSON, default=list)
    emotional_baseline = Column(String, default="neutral")
    last_updated = Column(DateTime, nullable=True)


class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False, index=True)
    type = Column(String)
    content = Column(Text)
    pattern = Column(Text, nullable=True)
    observation = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    extra_metadata = Column("metadata", JSON, default=dict)


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    scenario = Column(String)
    emotion = Column(String)
    mode = Column(String)
    extra_metadata = Column("metadata", JSON, default=dict)
    type = Column(String, default="interaction_log")


class MemorySummary(Base):
    __tablename__ = "memory_summaries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    traits_identified = Column(JSON, default=list)
    signals = Column(JSON, default=dict)
    type = Column(String, default="trait_update")
