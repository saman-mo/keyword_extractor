from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload, GeoPoint
from ai_es_utils.queries.utils import wrap_bool_query, query_dict
from ai_es_utils.services import GeoLocationService


class DistanceFromGeoPointQuery(QueryComponent):
    def __init__(
            self,
            coordinates_field: str = "geoPoint",
            distance_field: str = "distance",
            bool_type: str = "filter",
            **kwargs
    ):
        self.coordinates_field = coordinates_field
        self.distance_field = distance_field
        self.bool_type = bool_type
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        geo_point = payload.query.get(self.coordinates_field)
        distance = payload.query.get(self.distance_field)
        if geo_point is not None and distance is not None:
            query = wrap_bool_query(self._build(geo_point, distance), bool_type=self.bool_type)
            return QueryComponentResponse(
                query=query
            )
        else:
            return QueryComponentResponse(query={})

    def _build(self, geo_point: GeoPoint, distance: int) -> dict:
        return query_dict(
            "geo_distance",
            distance=distance * 1000,
            distance_type="arc",
            geoPoint=[geo_point.long, geo_point.lat],
            **self.kwargs
        )
