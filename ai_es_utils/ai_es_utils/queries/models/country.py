import re
from typing import Optional

from pydantic import validator

from ai_es_utils.queries.models.get_basemodel import GetBaseModel

COUNTRY_NAME_REGEX = re.compile(r"^.*[a-zA-Z]{1,}.*$")
COUNTRY_CODE_REGEX = re.compile(r"^[a-zA-Z_]{2,}$")


class Country(GetBaseModel):
    text: Optional[str]
    value: Optional[str]

    @validator("text")
    def validate_text(text):
        if text is None or not text.strip():
            return None

        m = COUNTRY_NAME_REGEX.match(text.strip())
        if not m:
            raise ValueError("country name not matching the expected pattern")
        return text.strip()

    @validator("value")
    def validate_code(value):
        if value is None or not value.strip():
            return None

        m = COUNTRY_CODE_REGEX.match(value.strip())
        if not m:
            raise ValueError("country code not matching the expected pattern")

        return value.strip().upper()
