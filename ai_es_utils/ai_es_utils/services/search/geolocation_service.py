from typing import Callable

from ai_es_utils.queries.components import CoordinatesLocationAndCountryQuery
from ai_es_utils.queries.interfaces import QueryComponent
from ai_es_utils.queries.models import GeoPoint, RequestPayload
from ai_es_utils.services import GeoLocationService, ElasticSearchService
from ai_es_utils.search.result_parsers import ParseGeoPoint


class GeoLocationFromCoordinatesService(GeoLocationService):
    def __init__(self,
                 index: str = "coordinates",
                 query_builder: QueryComponent = None,
                 location_parser: Callable = None,
                 **kwargs
                 ) -> None:
        """
        Service to fetch geopoint coordinates from elastic search. The search logic is defined by the ``query_builder``.

        :param index: defaults to ``coordinates``, an index specifically created to find geopoint information
        :param query_builder: query component building the search logic for the coordinates index
        :param location_parser: Post processor extracting geopoints from ES search results
        :param kwargs: passed to ElasticsearchService instance, such as timeout.
        """
        super().__init__()
        self._get_location = location_parser
        if not self._get_location:
            self._get_location = ParseGeoPoint()
        self.query_builder = query_builder
        if not self.query_builder:
            self.query_builder = CoordinatesLocationAndCountryQuery()
        self.search = ElasticSearchService(index, **kwargs)

    def __call__(self, payload: RequestPayload) -> GeoPoint:
        query = self.query_builder.query(payload).query
        search_results = self.search.execute(query)
        return self._get_location(search_results, payload=payload, query=query)
