from .create_superuser_if_not_exist import create_superuser_if_not_exists
from .generate_professions_if_table_is_empty import generate_professions_if_table_is_empty
from .populate_cities_if_table_is_empty import populate_cities_if_table_is_empty


def run_start_tasks():
    create_superuser_if_not_exists.delay()
    generate_professions_if_table_is_empty.delay()
    populate_cities_if_table_is_empty.delay()
