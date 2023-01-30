docker run -d \
    -p 5433:5432 \
    --name test-db-fastapi \
    --restart always \
    -e POSTGRES_DB=fastapitdb \
    -e POSTGRES_USER=fastapiuser \
    -e POSTGRES_PASSWORD=fastapipassword \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v fastapi-db:/var/lib/postgresql/data \
    ul-postgis:latest

    # -e POSTGRES_MULTIPLE_DATABASES=fastapitdb, tdb \