# Frege GitHub Indexer

## Docker environment variables

* `RMQ_HOST` - RabbitMQ host
* `RMQ_PORT` - RabbitMQ port (*optional - default 5672*)


* `DB_HOST` - PostgreSQL server host
* `DB_PORT` - PostgreSQL server host (*optional - default 5432*)
* `DB_DATABASE` - Database name
* `DB_USERNAME` - Database username
* `DB_PASSWORD` - Database password


* `GITHUB_PERSONAL_TOKEN` - GitLab personal access token
* `MIN_STARS` - Minimal number of stars that repository should have (*optional*)
* `MIN_FORKS` - Minimal number of forks that repository should have (*optional*)
* `RMQ_REJECTED_PUBLISH_DELAY` - Time in seconds to wait until next attempt to publish while rejected
* `LAST_UPDATED` - Last time repo was updated, e.g. 2020-03-06 


