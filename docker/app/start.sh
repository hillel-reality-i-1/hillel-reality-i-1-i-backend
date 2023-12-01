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

# [init]-[END]

export RABBITMQ_URL="amqp://${RABBITMQ_USER}:${RABBITMQ_PASSWORD}@rabbitmq:5672/"

rabbitmq_ready() {
python <<END
import sys

import pika

try:
    connection = pika.BlockingConnection(
        pika.URLParameters('${RABBITMQ_URL}')
    )
except pika.exceptions.AMQPConnectionError:
    sys.exit(-1)
sys.exit(0)

END
}

until rabbitmq_ready; do
  echo >&2 'RabbitMQ is unavailable (sleeping)...'
  sleep 1
done

echo >&2 'RabbitMQ is up - continuing...'

python manage.py shell -c "from apps.base.tasks import run_start_tasks; run_start_tasks()"

# Run application.
python manage.py runserver 0.0.0.0:8000

