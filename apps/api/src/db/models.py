from sqlalchemy import (
    Column, String, Text, DateTime, Float, Integer, ForeignKey, Enum as SQLEnum,
    Index, JSON, Boolean, BigInteger
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import uuid
import enum
from pgvector.sqlalchemy import Vector


Base = declarative_base()


class UserRole(str, enum.Enum):
    FOUNDER = "FOUNDER"
    CTO = "CTO"
    MARKETER = "MARKETER"
    CREATOR = "CREATOR"
    INFLUENCER = "INFLUENCER"


class Plan(str, enum.Enum):
    FREE = "FREE"
    PRO = "PRO"
    TEAM = "TEAM"
    ENTERPRISE = "ENTERPRISE"


class AnalysisType(str, enum.Enum):
    DEEP_DIVE = "DEEP_DIVE"
    COMPETITOR_COMPARISON = "COMPETITOR_COMPARISON"
    MARKET_LANDSCAPE = "MARKET_LANDSCAPE"
    CAMPAIGN_TRACKING = "CAMPAIGN_TRACKING"


class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class MemoryType(str, enum.Enum):
    FACT = "FACT"
    INSIGHT = "INSIGHT"
    OPINION = "OPINION"
    METRIC = "METRIC"
    NEWS = "NEWS"
    REVIEW = "REVIEW"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255))
    role = Column(SQLEnum(UserRole), default=UserRole.FOUNDER)
    plan = Column(SQLEnum(Plan), default=Plan.FREE)
    clerk_id = Column(String(255), unique=True, index=True)
    analyses_count = Column(Integer, default=0)
    brands_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    brands = relationship("Brand", back_populates="user", cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")
    comparisons = relationship("Comparison", back_populates="user", cascade="all, delete-orphan")


class Brand(Base):
    __tablename__ = "brands"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    domain = Column(String(255), index=True)
    industry = Column(String(100))
    description = Column(Text)
    competitors = Column(ARRAY(String), default=[])
    focus_keywords = Column(ARRAY(String), default=[])
    profile_embedding = Column(Vector(1536))
    auto_discovered = Column(Boolean, default=False)
    last_analyzed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="brands")
    analyses = relationship("Analysis", back_populates="brand", cascade="all, delete-orphan")
    memories = relationship("BrandMemory", back_populates="brand", cascade="all, delete-orphan")
    primary_comparisons = relationship("Comparison", foreign_keys="Comparison.primary_brand_id", back_populates="primary_brand")
    competitor_comparisons = relationship("Comparison", foreign_keys="Comparison.competitor_brand_ids", back_populates="competitor_brands")

    __table_args__ = (
        Index("ix_brands_user_name", "user_id", "name"),
        Index("ix_brands_domain", "domain"),
    )


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey("brands.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(SQLEnum(AnalysisType), nullable=False)
    status = Column(SQLEnum(JobStatus), default=JobStatus.PENDING, index=True)
    input_config = Column(JSONB, nullable=False)  # {query, competitors[], date_range, focus_areas, depth}
    result = Column(JSONB)  # Full structured report
    job_id = Column(String(100), index=True)  # BullMQ job ID
    error = Column(Text)
    progress = Column(Integer, default=0)
    current_stage = Column(String(50))
    stage_progress = Column(JSONB, default={})
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    brand = relationship("Brand", back_populates="analyses")
    user = relationship("User", back_populates="analyses")

    __table_args__ = (
        Index("ix_analyses_user_status", "user_id", "status"),
        Index("ix_analyses_brand_created", "brand_id", "created_at"),
    )


class BrandMemory(Base):
    __tablename__ = "brand_memories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey("brands.id", ondelete="CASCADE"), nullable=False, index=True)
    type = Column(SQLEnum(MemoryType), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1536))
    confidence = Column(Float, default=1.0)
    source_url = Column(String(500))
    source_title = Column(String(500))
    tags = Column(ARRAY(String), default=[])
    extracted_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    expires_at = Column(DateTime(timezone=True), index=True)

    brand = relationship("Brand", back_populates="memories")

    __table_args__ = (
        Index("ix_brand_memories_brand_type", "brand_id", "type"),
        Index("ix_brand_memories_expires", "expires_at"),
        Index("ix_brand_memories_embedding", "embedding", postgresql_using="hnsw"),
    )


class Comparison(Base):
    __tablename__ = "comparisons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    primary_brand_id = Column(UUID(as_uuid=True), ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    competitor_brand_ids = Column(ARRAY(UUID(as_uuid=True)), default=[])
    metrics = Column(JSONB, default={})  # Side-by-side computed metrics
    insights = Column(JSONB, default={})  # AI-generated comparative insights
    analysis_ids = Column(ARRAY(UUID(as_uuid=True)), default=[])  # Linked analyses
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="comparisons")
    primary_brand = relationship("Brand", foreign_keys=[primary_brand_id], back_populates="primary_comparisons")
    competitor_brands = relationship("Brand", foreign_keys=[competitor_brand_ids], back_populates="competitor_comparisons")


class EmailDigest(Base):
    __tablename__ = "email_digests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    brand_ids = Column(ARRAY(UUID(as_uuid=True)), default=[])
    frequency = Column(String(20), default="weekly")  # weekly, monthly
    last_sent_at = Column(DateTime(timezone=True))
    next_send_at = Column(DateTime(timezone=True), index=True)
    is_active = Column(Boolean, default=True)
    config = Column(JSONB, default={})  # Customization options
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())