from typing import Dict, Any


def query_dict(base_key: str, **kwargs) -> Dict[str, Any]:
    """
    Generates query dictionary similar to the deprecated `elasticsearch_dsl.Q` and helps a with readability of the
    nested dict structures produced for elasticsearch queries.

    e.g.:
    ``_dict = query_dict("ids", values=["asdf", "asdf2"])``
    results int:
    ```
    {
        "ids": {
            "values": ["asdf", "asdf2"]
        }
    }
    ```

    :param base_key: top level key string
    :param kwargs: dictionary used next level under base_key
    :return: nested dictionary
    """
    return {base_key: dict(**kwargs)}
