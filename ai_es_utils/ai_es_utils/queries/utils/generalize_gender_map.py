def generalize_gender_map(gender_map: dict) -> dict:
    _generalized_gender_map = dict()
    for key, value in gender_map.items():
        _job_list = [data["jobTitle"] for gender, data in value.items()]
        for job in _job_list:
            _generalized_gender_map[job] = value
    return _generalized_gender_map
