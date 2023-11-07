#!/usr/bin/env bash

# shellcheck disable=SC2124
cmd="$@"

# [bash_init]-[BEGIN]
# Exit whenever it encounters an error, also known as a non–zero exit code.
set -o errexit
# Return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status,
#   or zero if all commands in the pipeline exit successfully.
set -o pipefail
# Treat unset variables and parameters other than the special parameters ‘@’ or ‘*’ as an error when performing parameter expansion.
set -o nounset
# [bash_init]-[END]

# [wait_postgres]-[BEGIN]
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

postgres_ready() {
  python <<END
import sys

import psycopg

try:
    psycopg.connect(
        '${DATABASE_URL}'
    )
except psycopg.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}

until postgres_ready; do
  echo >&2 'PostgreSQL is unavailable (sleeping)...'
  sleep 1
done

echo >&2 'PostgreSQL is up - continuing...'
# [wait_postgres]-[END]

# shellcheck disable=SC2086
exec $cmd
