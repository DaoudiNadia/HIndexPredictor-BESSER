import enum
from typing import List as List_, Optional as Optional_
from sqlalchemy import (
    create_engine, Column as Column_, ForeignKey as ForeignKey_, Table as Table_, 
    Text as Text_, Boolean as Boolean_, String as String_, Date as Date_, 
    Time as Time_, DateTime as DateTime_, Float as Float_, Integer as Integer_, Enum
)
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped as Mapped_, mapped_column, relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date

class Base(DeclarativeBase):
    pass

# Definitions of Enumerations
class FieldName(enum.Enum):
    PHYSICS = "PHYSICS"
    MEDICINE = "MEDICINE"
    ECONOMICS = "ECONOMICS"
    CHEMISTRY = "CHEMISTRY"
    COMPUTER_SCIENCE = "COMPUTER_SCIENCE"
    BIOLOGY = "BIOLOGY"
    SOCIOLOGY = "SOCIOLOGY"
    MATHEMATICS = "MATHEMATICS"


# Tables definition for many-to-many relationships

# Tables definition
class Researcher(Base):
    __tablename__ = "researcher"
    id: Mapped_[int] = mapped_column(primary_key=True)
    hIndex: Mapped_[int] = mapped_column(Integer_)
    totalCitations: Mapped_[int] = mapped_column(Integer_)
    totalPapers: Mapped_[int] = mapped_column(Integer_)
    careerAge: Mapped_[int] = mapped_column(Integer_)
    citationsPerPaper: Mapped_[float] = mapped_column(Float_)
    researchfield_id: Mapped_[int] = mapped_column(ForeignKey_("researchfield.id"))

class ResearchField(Base):
    __tablename__ = "researchfield"
    id: Mapped_[int] = mapped_column(primary_key=True)
    averageHIndex: Mapped_[float] = mapped_column(Float_)
    name: Mapped_[FieldName] = mapped_column(Enum(FieldName))


#--- Relationships of the researcher table
Researcher.researchfield: Mapped_["ResearchField"] = relationship("ResearchField", back_populates="researcher", foreign_keys=[Researcher.researchfield_id])

#--- Relationships of the researchfield table
ResearchField.researcher: Mapped_[List_["Researcher"]] = relationship("Researcher", back_populates="researchfield", foreign_keys=[Researcher.researchfield_id])

# Database connection
DATABASE_URL = "sqlite:///Class_Diagram.db"  # SQLite connection
engine = create_engine(DATABASE_URL, echo=True)

# Create tables in the database
Base.metadata.create_all(engine, checkfirst=True)