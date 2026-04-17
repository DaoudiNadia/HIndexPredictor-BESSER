from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

class FieldName(Enum):
    CHEMISTRY = "CHEMISTRY"
    ECONOMICS = "ECONOMICS"
    BIOLOGY = "BIOLOGY"
    COMPUTER_SCIENCE = "COMPUTER_SCIENCE"
    SOCIOLOGY = "SOCIOLOGY"
    MATHEMATICS = "MATHEMATICS"
    PHYSICS = "PHYSICS"
    MEDICINE = "MEDICINE"

############################################
# Classes are defined here
############################################
class ResearcherCreate(BaseModel):
    totalPapers: int
    careerAge: int
    citationsPerPaper: float
    hIndex: int
    totalCitations: int
    researchfield: int  # N:1 Relationship (mandatory)


class ResearchFieldCreate(BaseModel):
    averageHIndex: float
    name: FieldName
    researcher: Optional[List[int]] = None  # 1:N Relationship


