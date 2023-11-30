#!/usr/bin/env bash

# [bash_init]-[BEGIN]
# Exit whenever it encounters an error, also known as a non–zero exit code.
set -o errexit
# Return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status,
#   or zero if all commands in the pipeline exit successfully.
set -o pipefail
# Treat unset variables and parameters other than the special parameters ‘@’ or ‘*’ as an error when performing parameter expansion.
set -o nounset
# Print a trace of commands.
set -o xtrace
# [bash_init]-[END]

# [init]-[BEGIN]
# Apply database migrations.
make migrate

# Create default superuser if not exist
if python manage.py shell -c "from django.contrib.auth import get_user_model; print(get_user_model().objects.exists())" | grep -q "False"; then
    make init-dev-i-create-superuser
fi

## Generate cities and countries
#if python manage.py shell -c "from cities_light.models import City; print(City.objects.exists())" | grep -q "False"; then
#    make init-dev-i-generate-cities
#fi

# Generate professions and services
if python manage.py shell -c "from apps.expert.models import Profession; print(Profession.objects.exists())" | grep -q "False"; then
    make init-dev-i-generate-prof-and-serv
fi

# [init]-[END]

# Run application.
python manage.py runserver 0.0.0.0:8000

