from ai_es_utils.queries.interfaces.query_component import QueryComponent, RequestPayload, QueryComponentResponse
from ai_es_utils.queries.utils import query_dict


class MinimumShouldMatchQuery(QueryComponent):
    def __init__(self, name: str,
                 minimum_should_match: int = 1,
                 bool_type: str = "must",
                 **kwargs):
        """
        The component adds the key `minimum_should_match` to query group named `name`.
        The `bool_key` controls which outer bool query the sub-query should be written to.

        :param name: string for named query
        :param minimum_should_match: number of matching queries expected
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal term query
        """
        self.kwargs = kwargs
        self.bool_type = bool_type
        self.minimum_should_match = minimum_should_match
        self.name = name

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        return QueryComponentResponse(query={
            "query": {
                "bool": {
                    self.bool_type: [
                        query_dict(
                            "bool",
                            minimum_should_match=self.minimum_should_match,
                            _name=self.name
                        )
                    ]
                }
            }
        })
