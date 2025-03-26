import pytest

from ai_es_utils.queries.utils import update_nested_dict, OverrideValueWarning


@pytest.mark.parametrize(
    "insert_dict, source_dict, expected_dict", [
        # Inject new key (arbitrary type)
        ({"new_key": 1},
         {"a": 2},
         {"new_key": 1, "a": 2}),
        # Inject into list
        ({"list": [{"new_entry": True}]},
         {"list": [{"old_entry": False}]},
         {"list": [{"old_entry": False}, {"new_entry": True}]}),
        # Inject into nested dictionary
        ({"dict": {"new_key": True}},
         {"dict": {"a": False}},
         {"dict": {"new_key": True, "a": False}}),
        # Ignore key-value pairs present in both dicts
        ({"dict": {"new_key": True, "shared_key": 1}},
         {"dict": {"a": False, "shared_key": 1}},
         {"dict": {"new_key": True, "a": False, "shared_key": 1}})
    ]
)
def test_insert_value(insert_dict, source_dict, expected_dict):
    _dict = update_nested_dict(insert_dict, source_dict)
    assert _dict == expected_dict


def test_override_value():
    _dict = update_nested_dict(
        {"dict": {"a": "new_value", "b": True}},
        {"dict": {"a": "value"}}
    )
    assert _dict == {"dict": {"a": "new_value", "b": True}}


def test_warning_override_value():
    with pytest.warns(OverrideValueWarning):
        _dict = update_nested_dict(
            {"dict": {"a": "new_value", "b": True}},
            {"dict": {"a": "value"}}
        )
