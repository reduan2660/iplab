#!/usr/bin/sh

echo "Waiting for Database to start"
./wait-for-it.sh $DB_HOST:$DB_PORT --timeout=0
echo "Database started"

# if DEPLOYMENT_ENV != "production" then migrate the db
if [ "$DEPLOYMENT_ENV" != "production" ]; then
    echo "Running Migration"
    alembic upgrade head
    echo "Migration run successfully"
fi

# Run the server
echo "Running Server at port $EXPOSE_PORT"
gunicorn app.main:app \
    --log-level debug \
    --workers=${GUNICORN_WORKERS} \
    --worker-class="uvicorn.workers.UvicornWorker" \
    --bind "0.0.0.0:${EXPOSE_PORT}"