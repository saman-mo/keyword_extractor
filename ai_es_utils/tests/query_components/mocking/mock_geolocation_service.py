from ai_es_utils.services.search.geolocation_service import GeoLocationService, GeoPoint, RequestPayload
from ai_es_utils.queries.models.country import Country


class MockGeoLocationService(GeoLocationService):
    def __init__(self, mock_data: dict):
        self.mock_data = mock_data
        self._default = {list(v.keys())[0]: list(v.values())[0] for k, v in self.mock_data.items()}

    def __call__(self, payload: RequestPayload):
        location = payload.query.get("location")
        country = payload.query.get("country", Country()).text
        country_mock = self.mock_data.get(country, self._default)
        location_mock = country_mock.get(location, None)
        if location_mock:
            return GeoPoint(**location_mock)
        else:
            return None
