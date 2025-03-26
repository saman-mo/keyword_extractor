import re
from typing import Optional, List, Dict

import pydantic
from pydantic import BaseModel, validator, constr

from ai_es_utils.queries.models.country import Country
from ai_es_utils.queries.models.get_basemodel import GetBaseModel

JOB_TITLE_PATTERN = re.compile(r'\b(\w|-\s){2,}\b', flags=re.IGNORECASE)


class SemanticExpansion(BaseModel):
    jobs: Optional[List[Dict]]
    skills: Optional[List[Dict]]


class Query(GetBaseModel, extra=pydantic.Extra.allow):
    pass


class ValidatedSearchQuery(Query):
    changeProbability: Optional[int]
    consultantsOnly: Optional[bool]
    country: Optional[Country] = Country()
    location: Optional[str]
    distance: Optional[int] = 25  # distance in km
    entrepreneursOnly: Optional[bool]
    excludePortals: Optional[List[str]]
    executiveOnly: Optional[bool]
    freelancerOnly: Optional[bool]
    hasEmail: Optional[bool]
    hasPhone: Optional[bool]
    includePortals: Optional[List[str]]
    industryCode: Optional[str]
    isMale: Optional[bool]
    jobTitle: Optional[constr(to_lower=True)]
    languages: Optional[List[str]]
    mobility: Optional[int]
    previouslyAt: Optional[List[str]]
    previouslyAtExclude: Optional[List[str]]
    recruiterOnly: Optional[bool]
    relevance: Optional[int]
    scientistsOnly: Optional[bool]
    semanticExpansion: Optional[SemanticExpansion]
    skills: Optional[List[str]]
    studentsOnly: Optional[bool]
    worksAt: Optional[List[str]]
    worksAtExclude: Optional[List[str]]
    yearsWorkingMax: Optional[int]
    yearsWorkingMin: Optional[int]
    blocklist: Optional[List[str]]

    @validator('jobTitle')
    def job_title_must_be_non_empty(cls, job_title):
        if JOB_TITLE_PATTERN.search(job_title) is None:
            raise ValueError('must contain a minimum number of alphabetical symbols')
        return job_title

    @validator('worksAt')
    def validate_non_empty_string(cls, works_at):
        if works_at is not None:
            for company in works_at:
                if len(company.strip(' ')) < 2:
                    raise ValueError('worksAt must contain company name with at minimum 2 alphabetical symbols')
        return works_at

    @validator('includePortals')
    def validate_include_portals(cls, include_portals, values):
        if include_portals:
            exclude_portals = values.get('excludePortals')
            if exclude_portals:
                raise ValueError("includePortals and excludePortals are mutual exclusive")
        return include_portals

    @validator('excludePortals')
    def validate_exclude_portals(cls, exclude_portals, values):
        if exclude_portals:
            include_portals = values.get('includePortals')
            if include_portals:
                raise ValueError("includePortals and excludePortals are mutual exclusive")
        return exclude_portals

    @validator('worksAt')
    def validate_works_at(cls, works_at, values):
        if works_at:
            works_at_exclude = values.get('worksAtExclude')
            if works_at_exclude:
                raise ValueError("worksAt and worksAtExclude are mutual exclusive")
        return works_at

    @validator('worksAtExclude')
    def validate_works_at_exclude(cls, works_at_exclude, values):
        if works_at_exclude:
            works_at = values.get('worksAt')
            if works_at:
                raise ValueError("worksAt and worksAtExclude are mutual exclusive")
        return works_at_exclude

    @validator('previouslyAt')
    def validate_previously_at(cls, previously_at, values):
        if previously_at:
            include_portals = values.get('previouslyAtExclude')
            if include_portals:
                raise ValueError("previouslyAt and previouslyAtExclude are mutual exclusive")
        return previously_at

    @validator('previouslyAtExclude')
    def validate_previously_at_exclude(cls, previously_at_exclude, values):
        if previously_at_exclude:
            previously_at = values.get('previouslyAt')
            if previously_at:
                raise ValueError("previouslyAt and previouslyAtExclude are mutual exclusive")
        return previously_at_exclude

    @validator("distance")
    def validate_distance(cls, distance, values):
        if values.get("location") is None:
            return distance  # If no location is provided, distance does not need to be validated.

        if distance is None:
            raise ValueError("Distance can't be null or None. Please provide a value >= 0.")
        elif distance <= 0:
            raise ValueError(f"distance = {distance} can not be zero or less")

        return distance
