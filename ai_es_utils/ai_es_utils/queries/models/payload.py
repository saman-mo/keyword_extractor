from typing import Optional

from pydantic import BaseModel

from ai_es_utils.queries.models.filter import Filter
from ai_es_utils.queries.models.query import Query, ValidatedSearchQuery


class RequestPayload(BaseModel):
    query: Optional[Query] = Query()
    filter: Optional[Filter] = Filter()


class ValidatedPayload(RequestPayload):
    query: Optional[ValidatedSearchQuery] = ValidatedSearchQuery()

    def get_job_title(self):
        return self.query.jobTitle

    def get_location(self):
        return self.query.location

    def get_country_name(self):
        return self.query.country.text

    def get_country_code(self):
        return self.query.country.value

    def get_industry_code(self):
        return self.query.industryCode

    def get_works_at(self):
        return self.query.worksAt

    def get_works_at_exclude(self):
        return self.query.worksAtExclude

    def get_previously_at(self):
        return self.query.previouslyAt

    def get_previously_at_exclude(self):
        return self.query.previouslyAtExclude

    def get_semantic_jobs(self):
        if self.query.semanticExpansion and self.query.semanticExpansion.jobs is not None:
            return self.query.semanticExpansion.jobs
        else:
            return None

    def get_semantic_skills(self):
        if self.query.semanticExpansion and self.query.semanticExpansion.skills is not None:
            return self.query.semanticExpansion.skills
        else:
            return None
