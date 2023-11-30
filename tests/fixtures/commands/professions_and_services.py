import json
import pytest


@pytest.fixture
def json_data():
    return {
        "Profession1": ["Service1", "Service2"],
        "Profession2": ["Service3", "Service4"],
    }


@pytest.fixture
def json_file_path(tmpdir, json_data):
    json_file = tmpdir.join("test_professions_and_services.json")
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(json_data, file)
    return str(json_file)
