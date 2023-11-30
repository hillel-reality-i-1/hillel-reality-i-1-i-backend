import os
import json

from django.core.management import call_command

from apps.expert.models import Profession, Service


def test_generate_prof_and_serv_command(json_file_path):
    os.environ["JSON_FILE_PATH"] = json_file_path

    call_command("generate_prof_and_serv")

    for profession_name, services_list in json.load(open(json_file_path)).items():
        profession = Profession.objects.get(name=profession_name)

        assert profession is not None

        for service_name in services_list:
            service = Service.objects.get(name=service_name)
            assert service is not None

            assert profession in service.professions.all()

    os.environ.pop("JSON_FILE_PATH", None)
