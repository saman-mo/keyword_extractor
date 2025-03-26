from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import wrap_bool_query, query_dict


class BlockingListQuery(QueryComponent):
    def __init__(self, blocklist_field: str = "blocklist", bool_type: str = "must_not", **kwargs):
        """
        This component allows to filter documents/profiles from the search results by providing a list of ids to ignore.

        :param blocklist_field:  field name in payload.query holding blocking list as list of str
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: keyword arguments directly passed to the lowest level ids query
        """
        self.blocklist_field = blocklist_field
        self.bool_type = bool_type
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        blocking_list = payload.query.get(self.blocklist_field)
        if blocking_list:
            query = wrap_bool_query(self._build_query(blocking_list), bool_type=self.bool_type)
            return QueryComponentResponse(query=query)
        return QueryComponentResponse(query=dict())

    def _build_query(self, blocking_list):
        return query_dict("ids", values=blocking_list, **self.kwargs)
