from datetime import datetime, timezone
from sqlalchemy import JSON, Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class IncidentRecord(Base):

    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True, 
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable = False,
    )

    description: Mapped[str] = mapped_column(
        Text, 
        nullable=False, 
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    suggested_priority: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
    )

    investigation_steps: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    human_review_required: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    reviewed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    reviewed_by: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    review_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )