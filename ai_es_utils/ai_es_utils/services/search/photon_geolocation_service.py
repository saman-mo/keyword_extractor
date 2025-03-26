import requests
from typing import List, Optional

from requests.adapters import Retry, HTTPAdapter

from ai_es_utils.services import GeoLocationService
from ai_es_utils.queries.models import GeoPoint, RequestPayload


class NoGeoLocationError(Exception):
    pass


class GetLocationFromPhotonAPI(GeoLocationService):
    def __init__(
            self,
            photon_api_endpoint: str = "http://photon.talentwunder.io:2322/api",
            location_field: str = "location",
            **kwargs
            
    ):
        self.photon_api_endpoint = photon_api_endpoint
        self.location_field = location_field

        self.retries = Retry(
            total=5,
            backoff_factor=0.1
        )
        self.request_session = requests.Session()
        self.request_session.mount(
            "http://",
            HTTPAdapter(max_retries=self.retries)
        )
        self.kwargs = kwargs

    def __call__(self, payload: RequestPayload) -> GeoPoint:
        location = payload.query.get(self.location_field)
        if isinstance(location, str):
            return self._get_geo_point(location)
        else:
            return None

    def _get_geo_point(self, location: str) -> GeoPoint:
        params = {**dict(q=location), **self.kwargs}
        response = self.request_session.get(f"{self.photon_api_endpoint}", 
            params=params)
        if not response.status_code == 200:
            raise ConnectionError(f"Fetching geopoint from photon API failed "
                                  f"for location: {location}, with status "
                                  f"code {response.status_code}")
        response_data = response.json()
        result_list = response_data.get("features", None)

        if not result_list:
            raise NoGeoLocationError(f"No matches from photon API for "
                                     f"location {location}")

        best_coordinates = result_list[0].get("geometry", dict())
        best_coordinates = best_coordinates.get("coordinates", None)

        if not best_coordinates:
            raise NoGeoLocationError(f"No valid coordinates detected "
                                     f"in result: {result_list[0]}")
        return GeoPoint(long=best_coordinates[0], lat=best_coordinates[1])

