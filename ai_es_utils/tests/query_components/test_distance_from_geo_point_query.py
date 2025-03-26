import pytest

from ai_es_utils.queries.components import DistanceFromGeoPointQuery
from ai_es_utils.queries.models.payload import RequestPayload, Query
from tests.utils import load_base_query
from ai_es_utils.queries.models import GeoPoint

target_query_body = load_base_query("distance_from_geo_point_query.json")
distance_query = DistanceFromGeoPointQuery()


@pytest.mark.parametrize(
    "geo_point, distance, _target_query_body", [
        (GeoPoint(long=13.404954, lat=52.52000659999999), 33, target_query_body),
        (None, 33, {}),
        (GeoPoint(long=13.404954, lat=52.52000659999999), None, {})
    ]
)
def test_base_query(geo_point, distance, _target_query_body):
    payload = RequestPayload()

    query_kwargs = {
        "geoPoint": geo_point,
        "distance": distance
    }
    query_kwargs = {k: v for k, v in query_kwargs.items() if v is not None}

    if query_kwargs:
        payload = RequestPayload(
            query=Query(**query_kwargs)
        )

    assert distance_query.query(payload).query == _target_query_body
