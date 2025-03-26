from enum import Enum
from typing import Optional

from pydantic import BaseModel, conint, validator


class Sorting(str, Enum):
    relevance = "relevance"
    mobility = "mobility"
    change_probability = "changeProbability"
    reputation = "reputation",
    profile_quality = "profileQuality"
    expertise = "expertise"
    score = "_score"


class Filter(BaseModel):
    sort: Optional[Sorting] = Sorting.relevance
    offset: Optional[conint(ge=0, le=10000)] = 0
    size: Optional[conint(ge=5, le=1000)] = 30

    @validator("sort", always=True)
    def rename_relevance(cls, v):
        if v == Sorting.relevance:
            v = Sorting.score
        return v
