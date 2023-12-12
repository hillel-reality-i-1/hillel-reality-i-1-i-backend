import os
import json
import environ
from django.conf import settings

from django.core.management import call_command

from apps.expert.models import Profession, Service


env = environ.FileAwareEnv()
env.read_env(settings.BASE_DIR.joinpath(".env"))
ROOT = env.str("ROOT", "/")


def test_generate_prof_and_serv_command(json_file_path):
    json_file_path = os.path.join(
        ROOT,
        'hillel-reality-i-1-i-backend',
        'apps',
        'expert',
        'management',
        'commands',
        'professions_and_services.json'
    )
    os.environ["JSON_FILE_PATH"] = json_file_path

    call_command("generate_prof_and_serv")

    for profession_name, services_list in json.load(open(json_file_path, encoding='utf-8')).items():
        profession = Profession.objects.get(name=profession_name)

        assert profession is not None

        for service_name in services_list:
            service = Service.objects.get(name=service_name)
            assert service is not None

            assert profession in service.professions.all()

    os.environ.pop("JSON_FILE_PATH", None)
