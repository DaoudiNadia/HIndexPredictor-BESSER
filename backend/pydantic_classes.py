from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

class FieldName(Enum):
    PHYSICS = "PHYSICS"
    MEDICINE = "MEDICINE"
    ECONOMICS = "ECONOMICS"
    CHEMISTRY = "CHEMISTRY"
    COMPUTER_SCIENCE = "COMPUTER_SCIENCE"
    BIOLOGY = "BIOLOGY"
    SOCIOLOGY = "SOCIOLOGY"
    MATHEMATICS = "MATHEMATICS"

############################################
# Classes are defined here
############################################
class ResearcherCreate(BaseModel):
    totalPapers: int
    careerAge: int
    hIndex: int
    citationsPerPaper: float
    totalCitations: int
    researchfield: int  # N:1 Relationship (mandatory)


class ResearchFieldCreate(BaseModel):
    averageHIndex: float
    name: FieldName
    researcher: Optional[List[int]] = None  # 1:N Relationship


