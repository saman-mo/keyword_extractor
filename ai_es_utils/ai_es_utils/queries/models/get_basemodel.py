from typing import Optional, Any

import pydantic


class GetBaseModel(pydantic.BaseModel):
    def get(self, field_name: str, default=None) -> Optional[Any]:
        try:
            return self.__getattribute__(field_name)
        except AttributeError:
            return default
