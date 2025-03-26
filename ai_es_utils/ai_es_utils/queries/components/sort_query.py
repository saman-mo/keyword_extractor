from ai_es_utils.queries.interfaces.query_component import QueryComponent, RequestPayload, QueryComponentResponse


class SortQuery(QueryComponent):
    def __init__(self, order: str = "desc", **kwargs):
        """
        The component produces a top-level entry that defines the order of returned results.
        Per default sorting for the _score is always provided.

        :param kwargs: dictionary of arguments passed directly to the internal term query
        """
        self.kwargs = kwargs
        self.order = order

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        sort_key = payload.filter.sort.value

        sort_dict = dict()
        sort_dict[sort_key] = {"order": self.order, **self.kwargs}
        if sort_key != "_score":
            sort_dict["_score"] = {"order": "desc", **self.kwargs}

        return QueryComponentResponse(
            query={
                "sort": [sort_dict]
            }
        )
