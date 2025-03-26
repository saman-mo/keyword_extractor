from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Any

from ai_es_utils.queries.utils.query_dict import query_dict

@dataclass
class NestedField:
    field: str
    path: str = None


class InvalidNestedField(Exception):
    """
    Exception indicating that the nested field is not valid
    """
    pass


def parse_nested_field(field: str) -> NestedField:
    field_list = field.split(".")
    if len(field_list) == 1:
        return NestedField(field=field)
    elif len(field_list) == 2:
        return NestedField(field=field_list[1], path=field_list[0])
    else:
        raise InvalidNestedField(f"Too many nested elements: {field}")


def wrap_nested_field_query(field: str, query: dict = None) -> Dict[str, Any]:
    nested_field = parse_nested_field(field)
    if nested_field.path:
        return query_dict("nested", path=nested_field.path, query=query)
    else:
        return query


def build_field_path_map(fields: List[str], boosts: List[float]) -> Dict[str, Any]:
    nested_fields = [parse_nested_field(f) for f in fields]
    field_path_map = defaultdict(list)
    for field, boost in zip(nested_fields, boosts):
        if boost:
            field.field = field.field + f"^{boost}"
        if field.path:
            field_path_map[field.path].append(field.field)
        else:
            field_path_map["None"].append(field.field)
    return field_path_map
