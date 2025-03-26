import copy
import json
import re

from typing import Dict


def map_to_nested_json_key(fn, _dict, key_list, **kwargs):
    try:
        k = key_list[0]
        if not isinstance(_dict[k], (dict, list)) and _dict[k]:
            _dict[k] = fn(_dict[k], **kwargs)
        elif isinstance(_dict[k], list):
            if k == key_list[-1]:
                for i, element in enumerate(_dict[k]):
                    _dict[k][i] = fn(element, **kwargs)
            else:
                for element in _dict[k]:
                    map_to_nested_json_key(fn, element, key_list[1:], **kwargs)
        elif isinstance(_dict[k], dict):
            map_to_nested_json_key(fn, _dict[k], key_list[1:], **kwargs)
    except KeyError:
        pass


def _replace_string(string, replace_dict=None):
    if isinstance(string, str):
        for k, v in replace_dict.items():
            string = re.sub(
                # Match the sequence if led by beginning of word or beginning of line, as well as end, respectively.
                r"(?<=(\b|^))" + re.escape(k) + r"(?=(\b|$))",
                v.replace("\\", "\\\\"),
                string
            )
    return string


class HighlightReplacer:
    def __init__(self, highlight_start_mark: str = "<mark>", highlight_end_mark: str = "</mark>"):
        """
        Applies highlighting to a nested dict, such as elasticsearch profiles. Requires
        initial building of the highlight instructions, which is called by `self.build`.

        :param highlight_start_mark: token indicating the beginning of highlighted string
        :param highlight_end_mark: token indicating the end of a highlighted string
        """

        self.start_mark = highlight_start_mark
        self.end_mark = highlight_end_mark

        self.highlight_map = None

    def build(self, highlight: Dict, exclude_startswith: str = "_"):
        """
        Initializes the `HighlightReplacer` for the subsequent calls.

        :param highlight: Dict provided by elasticsearch, holding instructions which fields to highlight.
        :param exclude_startswith: Allows to exclude fields, main purpose is to exclude "_totallyPrivateKey" type keys.
        :return:
        """
        highlight_map = dict()
        for key, value in highlight.items():
            if not key.startswith(exclude_startswith):
                highlight_map[key] = {
                    self._strip_mark(element): element for element in value
                }
        self.highlight_map = highlight_map

    def _strip_mark(self, string: str):
        return string.replace(self.start_mark, "").replace(self.end_mark, "")

    def __call__(self, _dict: Dict) -> Dict:
        """
        Applies highlighting to the provided nested dictionary.

        :param _dict: dict without highlights
        :return: highlighted dict
        """
        processed_dict = copy.deepcopy(_dict)
        for k in self.highlight_map:
            map_to_nested_json_key(_replace_string, processed_dict, k.split("."), replace_dict=self.highlight_map[k])
        return processed_dict


if __name__ == "__main__":
    with open("../../tests/test_data/highlighting/input_highlighting.json", "r") as file:
        highlight = json.load(file)
    with open("../../tests/test_data/highlighting/input_profile.json", "r") as file:
        profile = json.load(file)

    replacer = HighlightReplacer(highlight)
    print(replacer(profile))
