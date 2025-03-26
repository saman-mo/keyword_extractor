import pytest

from ai_es_utils.search.result_parsers.parse_geo_point import ParseGeoPoint
from ai_es_utils.queries.models import GeoPoint

from tests.utils import load_json_from_test_root

SAMPLE_SEARCH_RESULT = load_json_from_test_root("test_data/search_result/coordinates_search_result.json")


def test_parse_geo_point_from_results():
    geo_point_parser = ParseGeoPoint()
    geo_point = geo_point_parser(SAMPLE_SEARCH_RESULT)
    assert geo_point == GeoPoint(long=13.3922, lat=52.532)
