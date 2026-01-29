from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    # Fully Qualified Name is the primary key
    fqn = Column(String(255), primary_key=True, index=True)

    # Example: MySQL, PostgreSQL, MSSQL
    source_type = Column(String(50), nullable=False)

    # Parsed parts (for search)
    connection = Column(String(100), nullable=False)
    database = Column(String(100), nullable=False)
    schema = Column(String(100), nullable=False)
    table = Column(String(100), nullable=False)

    columns = relationship(
        "DatasetColumn",
        back_populates="dataset",
        cascade="all, delete-orphan",
    )

    upstream = relationship(
        "Lineage",
        foreign_keys="Lineage.downstream_fqn",
        back_populates="downstream",
    )

    downstream = relationship(
        "Lineage",
        foreign_keys="Lineage.upstream_fqn",
        back_populates="upstream",
    )


class DatasetColumn(Base):
    __tablename__ = "dataset_columns"

    id = Column(Integer, primary_key=True, index=True)
    dataset_fqn = Column(
        String(255),
        ForeignKey("datasets.fqn", ondelete="CASCADE"),
        nullable=False,
    )

    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)

    dataset = relationship("Dataset", back_populates="columns")

    __table_args__ = (
        UniqueConstraint("dataset_fqn", "name", name="uq_dataset_column"),
    )


class Lineage(Base):
    __tablename__ = "lineage"

    upstream_fqn = Column(
        String(255),
        ForeignKey("datasets.fqn", ondelete="CASCADE"),
        primary_key=True,
    )

    downstream_fqn = Column(
        String(255),
        ForeignKey("datasets.fqn", ondelete="CASCADE"),
        primary_key=True,
    )

    upstream = relationship(
        "Dataset",
        foreign_keys=[upstream_fqn],
        back_populates="downstream",
    )

    downstream = relationship(
        "Dataset",
        foreign_keys=[downstream_fqn],
        back_populates="upstream",
    )
