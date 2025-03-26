from typing import List, Tuple, Optional


class ParseBoostedFieldError(Exception):
    """
    Is raised if parsing boosted fields fails.
    """
    pass


def parse_boosted_fields(list_of_fields: List[str], split_str: str = "^") -> Tuple[list, list]:
    """
    Parse list of search fields with boost notation, such as `jobTitle^2.0` indicating that the
    search should consider the field `jobTitle` and boost the corresponding query by factor 2.0.
    If no boost value is assigned, the boost is set to `None`.

    :param list_of_fields: list of boosted fields, e.g. `["jobTitle^2.0", "previousJobTitles"]`
    :param split_str: string that indicates the split between field name and boost value
    :return: list of fields, list of boost values
    """

    fields = []
    boosts = []
    for field in list_of_fields:
        _split = field.split(split_str)

        if len(_split) > 2:
            raise ParseBoostedFieldError(f"Invalid field to parse: {field}")

        fields.append(_split[0])
        try:
            try:
                boost_float = float(_split[1])
            except ValueError:
                raise ParseBoostedFieldError(f"Invalid boost value: {_split[1]}")

            boosts.append(boost_float)
        except IndexError:
            boosts.append(1.0)

    return fields, boosts


def format_boosted_field(field: str, boost: Optional[float]) -> str:
    boosted_field = field
    if boost:
        boosted_field += f"^{boost}"
    return boosted_field


def apply_boost_factor(boosted_field_list: List[str], boost_factor: float):
    fields, boosts = parse_boosted_fields(boosted_field_list)
    return [format_boosted_field(field, boost*boost_factor) for field, boost in zip(fields, boosts)]
