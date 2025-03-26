from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload, Country
from ai_es_utils.queries.utils import wrap_bool_query, apply_boost_factor, query_dict


class CountryQuery(QueryComponent):
    def __init__(self,
                 country_names: dict = None,
                 name: str = "country",
                 country_field: str = "country",
                 bool_type: str = "filter",
                 boost_factor: float = 1.0,
                 **kwargs):
        """
        The component produces a query that filters for profiles corresponding to the
        provided countries. To this end, we consider various translations of the country
        name, which are provided by the `country_names` dict, whose keys are the country
        codes.
        The kwargs are passed directly to the inner <whatever you use> query.

        :param country_names: mapping from short-hand to country names (e.g. de -> Deutschland)
        :param name: name of the named query
        :param country_field: field name in payload.query holding country as Country()
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal query_string query
        """
        self.kwargs = kwargs
        self.country_names = country_names
        self.country_field = country_field
        self.name = name
        self.bool_type = bool_type
        self.boost_factor = boost_factor

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        country = payload.query.get(self.country_field, Country())
        if isinstance(country, dict):
            country = Country(**country)
        if isinstance(country.value, str) or isinstance(country.text, str):
            query = wrap_bool_query(self._build(country), bool_type=self.bool_type)
            return QueryComponentResponse(query=query)
        else:
            return QueryComponentResponse(query={})

    def _build(self, country: Country) -> dict:
        country_queries = []

        if country.value:
            country_queries.append(
                self._build_query_string_query(
                    self._build_country_codes_query(country),
                    apply_boost_factor(["address.countryCode^1.0"], self.boost_factor)
                )
            )

        country_queries.append(
            self._build_query_string_query(
                self._build_country_names_query(country),
                apply_boost_factor(["location^1.0"], self.boost_factor)
            )
        )

        return query_dict(
            "bool",
            should=country_queries,
            _name=self.name
        )

    @staticmethod
    def _remove_quotes(word):  # TODO: Should be moved to Country model validation
        w = word.strip('"')
        return f' "{w.replace("/", "//")}" '

    def _build_query_string_query(self, query, fields):
        return query_dict(
            "query_string",
            query=query,
            fields=fields,
            type="best_fields",
            default_operator="or",
            **self.kwargs
        )

    def _build_country_names_query(self, country: Country) -> str:
        country_names = []
        if country.value:
            country_names = self._get_country_names_from_value(country.value)

        _query = None
        if len(country_names) > 1:
            _query = " OR ".join(country_names)
        else:
            _query = self._remove_quotes(country.text)
        return _query

    def _get_country_names_from_value(self, country_value: str):
        country_names = self.country_names.get(country_value.upper(), {})
        # convert to list
        country_names = list(country_names.values())
        # remove quotes
        return [self._remove_quotes(name) for name in country_names]

    @staticmethod
    def _build_country_codes_query(country: Country) -> str:
        return " OR ".join([country.value, country.value.lower()])
