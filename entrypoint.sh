#!/bin/bash
set -e

case "$1" in
        api)
            echo "starting allocation service api"
	        gunicorn -c ./config/gunicorn_config.py --log-config config/logging.conf "allocation.entrypoints.api:create_app()"
            ;;
        upgrade)
            sleep 5
            export FLASK_APP="allocation.entrypoints.api:create_app()"
            alembic upgrade head
            ;;
        worker)
            echo "starting consumer"
            python -u -m allocation.entrypoints.consumer
            ;;
        *)
            $@
esac
