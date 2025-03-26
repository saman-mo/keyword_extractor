from pydantic import BaseModel


class GeoPoint(BaseModel):
    lat: float
    long: float
