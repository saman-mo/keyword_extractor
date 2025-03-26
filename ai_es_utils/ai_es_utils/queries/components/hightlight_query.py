from typing import List

from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import query_dict


class HighlightQuery(QueryComponent):
    def __init__(
            self,
            highlight_fields: List[str] = None,
            post_tags: str = "</mark>",
            pre_tags: str = "<mark>",
            require_field_match: bool = False,
            **kwargs
    ):
        """
        The component produces a top-level entry producing instructions to highlight the search results.

        :param highlight_fields: list of fields to include for highlights
        :param: post_tags: closing string for highlighted parts
        :param pre_tags: opening string for highlighted parts
        :param require_field_match: forwarded elasticsearch option. If true highlights field only if they matched.
        :param kwargs: dictionary of arguments passed directly to the internal term query
        """
        self.kwargs = kwargs

        self.highlight_fields = highlight_fields
        if not self.highlight_fields:
            self.highlight_fields = ["company",
                                     "email",
                                     "jobTitle",
                                     "jobs.jobTitle",
                                     "jobs.notes",
                                     "location",
                                     "previousCompanies",
                                     "previousJobTitles",
                                     "skills"]

        self.post_tags = post_tags
        self.pre_tags = pre_tags
        self.require_field_match = require_field_match

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        return QueryComponentResponse(
            query=query_dict(
                "highlight",
                fields={field: {} for field in self.highlight_fields},
                post_tags=self.post_tags,
                pre_tags=self.pre_tags,
                require_field_match=self.require_field_match,
                **self.kwargs
            )
        )
