import logging

import numpy as np

from typing import Dict, List, Any, Optional

from ai_es_utils.queries.models import GeoPoint


def extract_geo_coordinates_as_array(doc: Dict[str, Any]) -> Optional[List[float]]:
    try:
        gp = doc["_source"]["geoPoint"]
        return [gp["lat"], gp["lon"]]
    except KeyError:
        return None


def _check_geo_point_statistics(data: List[dict], **extra_data) -> None:
    geo_points = [extract_geo_coordinates_as_array(doc) for doc in data]
    mean = np.mean(geo_points, axis=0)
    std = np.std(geo_points, axis=0)

    if np.any(np.abs(std) > 5.0):
        logging.warning(
            "WARNING: GeoLocationService - High variance results detected in geo location service!",
            extra=dict(data=data, **extra_data)
        )

    if np.all(np.abs(std) < 0.1):
        return None  # Everything fine, super focused results.

    highly_varied_count = 0
    for gp in geo_points:
        is_highly_varied = np.any(np.abs(gp - mean) > std)
        if is_highly_varied:
            highly_varied_count += 1
        else:
            break

    if highly_varied_count > 0:
        logging.warning(
            f"WARNING: GeoLocationService - Best documents are beyond variance of all results!",
            extra=dict(data=data, **extra_data)
        )


class ParseGeoPoint:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def __call__(self, search_result: Dict[str, Any], **params) -> Optional[GeoPoint]:
        matched_geo_locations = search_result['hits']['hits']
        if matched_geo_locations:
            if self.verbose:
                _check_geo_point_statistics(matched_geo_locations, **params)
            d = matched_geo_locations[0]["_source"]["geoPoint"]
            return GeoPoint(lat=d['lat'], long=d['lon'])
        else:
            return None
