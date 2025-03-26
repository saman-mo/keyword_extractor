from typing import Dict, Optional, List

from pydantic import BaseModel

from ai_es_utils.queries.models.geopoint import GeoPoint
from ai_es_utils.queries.models.payload import RequestPayload


class Expansion(BaseModel):
    skills: List[Dict] = None
    jobs: List[Dict] = None
    geoPoint: GeoPoint = None
    genders: List[str] = None
    blacklist: List[str] = None


class ExpandedQuery(BaseModel):
    payload: RequestPayload
    expansion: Optional[Expansion] = None
    curation: Optional[Expansion] = None
