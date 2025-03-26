import json
from abc import ABC, abstractmethod
from typing import Callable, Dict

from elasticsearch import Elasticsearch

from ai_es_utils.queries.models import GeoPoint, RequestPayload


class ElasticSearchService(ABC):
    def __init__(self, index: str, **kwargs):
        """
        Abstract interface for elasticsearch wrapper to execute searches.

        :param index: elasticsearch index to search in
        :param kwargs: keyword arguments passed to the Elasticsearch instance
        """
        self._search = Elasticsearch(**kwargs)
        self._index = index

    def execute(self, query: Dict) -> Dict:
        return self._search.search(body=query, index=self._index)


class GeoLocationService(ABC):
    """
    Abstract interface for a geolocation search, i.e. fetching geo coordinates for the location inferred
    from the request payload.
    """

    @abstractmethod
    def __call__(self, payload: RequestPayload) -> GeoPoint:
        ...
