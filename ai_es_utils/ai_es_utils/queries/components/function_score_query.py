from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import wrap_bool_query, query_dict


class FunctionScoreQuery(QueryComponent):
    def __init__(
            self,
            field: str = "ml5.profileQuality",
            factor: int = 1,
            missing: int = 4,
            modifier: str = "sqrt",
            bool_type: str = "must",
            **kwargs
    ):
        """
        The component produces a query that adds a function score to the must queries.
        TODO: Investigate what this component does and if we need it.
        The kwargs are passed directly to the inner most (match_all) query.

        :param field: key of field the function score is computed on
        :param factor: TODO: Check Docs
        :param missing: TODO: Check Docs
        :param modifier: TODO: Check Docs
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal match_all query
        """
        self.field = field
        self.factor = factor
        self.missing = missing
        self.modifier = modifier
        self.bool_type = bool_type
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        query = wrap_bool_query(self._build(), bool_type=self.bool_type)
        return QueryComponentResponse(query=query)

    def _build(self):
        return query_dict(
            "function_score",
            boost=1.0,
            functions=[
                query_dict(
                    "field_value_factor",
                    factor=self.factor,
                    field=self.field,
                    missing=self.missing,
                    modifier=self.modifier
                )
            ],
            max_boost=3.4028235e+38,
            query=query_dict("match_all", boost=1, **self.kwargs),
            score_mode="multiply"
        )
