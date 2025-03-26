from typing import List

from typing import List

from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models.payload import RequestPayload
from ai_es_utils.queries.utils import query_dict


class SourceExclusionQuery(QueryComponent):
    def __init__(self, source_exclusion_list: List[str]):
        self.source_exclusion_list = source_exclusion_list

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        if self.source_exclusion_list:
            return QueryComponentResponse(
                query=query_dict("_source", excludes=self.source_exclusion_list)
            )