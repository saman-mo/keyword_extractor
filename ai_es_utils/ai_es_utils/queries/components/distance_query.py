from ai_es_utils.queries.interfaces import QueryComponent, QueryComponentResponse
from ai_es_utils.queries.models import RequestPayload, GeoPoint
from ai_es_utils.queries.utils import wrap_bool_query, query_dict
from ai_es_utils.services import GeoLocationService


class DistanceQuery(QueryComponent):
    def __init__(
            self,
            geolocation_service: GeoLocationService,
            location_field: str = "location",
            distance_field: str = "distance",
            location_response_field: str = "location",
            bool_type: str = "filter",
            **kwargs
    ):
        """
        The component produces a query <describe what it does>.
        The kwargs are passed directly to the inner <whatever you use> query.

        :param geolocation_service: service to query geo coordinates from location information of type GeoLocationService
        :param location_field: field name in payload.query holding location string
        :param distance_field: field name in payload.query holding distance as int
        :param location_response_field: field name for the response data injection
        :param bool_type: type of outer boolean query (filter, must, must_not, should)
        :param kwargs: dictionary of arguments passed directly to the internal term query
        """
        self.geolocation_service = geolocation_service
        self.location_field = location_field
        self.distance_field = distance_field
        self.location_response_field = location_response_field
        self.bool_type = bool_type
        self.kwargs = kwargs

    def query(self, payload: RequestPayload, bearer_token: str = None) -> QueryComponentResponse:
        location = payload.query.get(self.location_field)
        if isinstance(location, str):
            distance = payload.query.get(self.distance_field)
            geo_point = self.geolocation_service(payload)
            if geo_point is not None and distance is not None:
                query = wrap_bool_query(self._build(geo_point, distance), bool_type=self.bool_type)
                return QueryComponentResponse(
                    query=query,
                    response_data={self.location_response_field: geo_point.dict()}
                )
            else:
                return QueryComponentResponse(query={})
        else:
            return QueryComponentResponse(query={})

    def _build(self, geo_point: GeoPoint, distance: int) -> dict:
        return query_dict(
            "geo_distance",
            distance=distance*1000,
            distance_type="arc",
            geoPoint=[geo_point.long, geo_point.lat],
            **self.kwargs
        )