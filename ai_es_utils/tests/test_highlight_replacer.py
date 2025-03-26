import json

import pytest

from ai_es_utils.search.highlight_replacer import HighlightReplacer
from tests.utils import add_pytest_cwd

input_profile = json.load(open(add_pytest_cwd("test_data/highlighting/input_profile.json")))
input_highlighting = json.load(open(add_pytest_cwd("test_data/highlighting/input_highlighting.json")))
expected_profile = json.load(open(add_pytest_cwd("test_data/highlighting/expected_profile_with_highlighting.json")))

highlighter = HighlightReplacer()


def test_highlight_replace_sample_case():
    highlighter.build(input_highlighting)
    _processed_profile = highlighter(input_profile)
    assert _processed_profile == expected_profile


@pytest.mark.parametrize(
    "input_dict, expected_dict, highlight_map", [
        # Ignore substrings
        (
                {"a": ["nananana", "na"]},
                {"a": ["nananana", "<mark>na</mark>"]},
                {"a": ["<mark>na</mark>"]}
        ),
        # 'Self referencing highlight map', i.e. sub-strings contained in the mark token
        (
                {"a": ["mark", "ma", "ar", "rk", "m", "a", "r", "k"]},
                {"a": ["<mark>mark</mark>",
                       "<mark>ma</mark>",
                       "<mark>ar</mark>",
                       "<mark>rk</mark>",
                       "<mark>m</mark>",
                       "<mark>a</mark>",
                       "<mark>r</mark>",
                       "<mark>k</mark>"]},
                {"a": ["<mark>mark</mark>",
                       "<mark>ma</mark>",
                       "<mark>ar</mark>",
                       "<mark>rk</mark>",
                       "<mark>m</mark>",
                       "<mark>a</mark>",
                       "<mark>r</mark>",
                       "<mark>k</mark>"]}
        ),
        # Match phrases in brackets at end of line
        (
                {"a": ["asdf (asdf)", "asdf asdf"]},
                {"a": ["asdf (<mark>asdf</mark>)", "asdf asdf"]},
                {"a": ["asdf (<mark>asdf</mark>)"]}
        ),
        # Match phrases in brackets at beginning of line
        (
                {"a": ["(asdf) asdf", "asdf asdf"]},
                {"a": ["(<mark>asdf</mark>) asdf", "asdf asdf"]},
                {"a": ["(<mark>asdf</mark>) asdf"]}
        ),
        # Very deeeeeeep dictionaries
        (
                {"a": [
                    {"b": {
                        "c": [
                            {"d": ["x", "y", "y", "x"]},
                            {"d": ["z", "z", "x", "y"]}
                        ]}
                    },
                    {"b": {
                        "c": [
                            {"d": ["y", "y", "x", "x"], "x": "x"},
                            {"d": ["z", "x", "z", "x"], "x": "x"}
                        ],
                        "x": "x"}
                    }
                ]
                },
                {"a": [
                    {"b":
                        {
                            "c": [
                                {"d": ["<mark>x</mark>", "y", "y", "<mark>x</mark>"]},
                                {"d": ["z", "z", "<mark>x</mark>", "y"]}
                            ]}
                    },
                    {"b":
                        {
                            "c": [
                                {"d": ["y", "y", "<mark>x</mark>", "<mark>x</mark>"], "x": "x"},
                                {"d": ["z", "<mark>x</mark>", "z", "<mark>x</mark>"], "x": "x"}
                            ],
                            "x": "x"}
                    }
                ]
                },
                {"a.b.c.d": ["<mark>x</mark>"]}
        ),
        # Handle backslashes in the original text TODO!!!
        (
                {"a": ["This\\That something"]},
                {"a": ["This\\That <mark>something</mark>"]},
                {"a": ["This\\That <mark>something</mark>"]}  # The issue seems to be here, the "to replace value"
        ),
        # Empty values in list of dicts
        (
                {"address": [{"text": "valid address"}, {"text": None}]},
                {"address": [{"text": "<mark>valid address</mark>"}, {"text": None}]},
                {"address.text": ["<mark>valid address</mark>"]}
        ),
        (
                {"a": ["na", 2]},
                {"a": ["na",2]},
                {"a": ["<mark>2</mark>"]}
        ),
        (
                {"a": [None, "na"]},
                {"a": [None, "<mark>na</mark>"]},
                {"a": ["<mark>na</mark>"]}
        ),
        (
                {"a": ["na", 2]},
                {"a": ["<mark>na</mark>",2]},
                {"a": ["<mark>na</mark>"]}
        )

    ]
)
def test_specific_cases(input_dict, expected_dict, highlight_map):
    highlighter.build(highlight_map)
    assert highlighter(input_dict) == expected_dict




