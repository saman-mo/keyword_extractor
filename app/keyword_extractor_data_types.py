from pydantic import BaseModel
from typing import List

class KeywordExtractorPayload(BaseModel):
    jobAd: str


class KeywordSortPayload(BaseModel):
    jobTitle: List[str]
    location: List[str]
    company: List[str]
    skills: List[str]
    skillParagraph: List[str]