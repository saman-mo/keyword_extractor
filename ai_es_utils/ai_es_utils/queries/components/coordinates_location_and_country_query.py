from typing import List

from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload
from ai_es_utils.queries.utils import generate_query_string, query_dict


class CoordinatesLocationAndCountryQuery(QueryComponent):
    def __init__(self,
                 boosted_fields: List[str] = None,
                 fuzzy: bool = False,
                 location_field: str = "location",
                 country_field: str = "country",
                 **kwargs):
        """
        This component produces a query for the coordinates index, searching various fields for matching locations
        and countries.

        :param boosted_fields: fields to search locations and countries in.
        :param fuzzy: boolean value controlling the query_string query being fuzzy or not.
        :param location_field: field name in payload.query holding location as str
        :param country_field: field name in payload.query holding country as Country()
        :param kwargs: keyword arguments directly passed to the lowest level query_string query
        """
        self.boosted_fields = boosted_fields
        if not self.boosted_fields:
            self.boosted_fields = [
                "location",
                "location_original",
                "location_cleaned^2.0",
                "location_formatted^3.0",
                "address.city^2.0",
                "address.county^0.5",
                "address.state^0.5",
                "address.country^2.0"
            ]
        self.fuzzy = fuzzy
        self.location_field = location_field
        self.country_field = country_field
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        location = payload.query.get(self.location_field)
        country = payload.query.get(self.country_field)

        if country:
            country = country.get("text")

        if isinstance(location, str):
            return QueryComponentResponse(query=self._build(location, country))
        else:
            return QueryComponentResponse(query={})

    def _build(self, location: str, country: str) -> dict:
        terms = [t for t in [location, country] if t]
        return {
            "query": query_dict(
                "bool",
                must=[
                    query_dict(
                        "query_string",
                        query=generate_query_string(terms, fuzzy=self.fuzzy),
                        fuzziness="AUTO",
                        fields=self.boosted_fields,
                        **self.kwargs
                    )
                ],
                filter=[
                    query_dict("exists", field="geoPoint")
                ]
            ),
            "_source": {
                "include": [
                    "geoPoint",
                    "location"
                ]
            }
        }
