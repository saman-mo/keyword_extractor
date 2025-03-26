from ai_es_utils.queries.interfaces.query_component import QueryComponent, RequestPayload, QueryComponentResponse


class SizeAndOffsetQuery(QueryComponent):
    def __init__(self, **kwargs):
        """
        The component produces a top level entry that defines the number of profiles to return (`size`),
        as well as the `offset`.

        :param kwargs: Warning: UNUSED!
        """
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        offset = payload.filter.offset
        size = payload.filter.size
        return QueryComponentResponse(query={
            "size": size,
            "from": offset
        })
