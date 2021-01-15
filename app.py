import os
import sys
from typing import Optional

from fregeindexerlib import RabbitMQConnectionParameters, DatabaseConnectionParameters, IndexerType

from github_indexer import GitHubIndexer
from github_indexer_parameters import GitHubIndexerParameters


def get_env_var_string(name: str, default: Optional[str] = None) -> str:
    try:
        return os.environ[name]
    except KeyError:
        if default is None:
            print(f"{name} environment var must be provided!")
            sys.exit(1)
        else:
            return default


def get_env_var_int_or_none(name: str) -> Optional[int]:
    try:
        return int(os.environ[name])
    except KeyError:
        return None


def get_env_var_int(name: str, default: Optional[int] = None) -> int:
    return int(get_env_var_string(name, str(default) if default is not None else None))


if __name__ == '__main__':
    rabbit = RabbitMQConnectionParameters(host=get_env_var_string('RMQ_HOST'),
                                          port=get_env_var_int('RMQ_PORT', default=5672))

    database = DatabaseConnectionParameters(host=get_env_var_string('DB_HOST'),
                                            port=get_env_var_int('DB_PORT', default=5432),
                                            database=get_env_var_string('DB_DATABASE'),
                                            username=get_env_var_string('DB_USERNAME'),
                                            password=get_env_var_string('DB_PASSWORD'))

    github = GitHubIndexerParameters(github_personal_token=get_env_var_string('GITHUB_PERSONAL_TOKEN'),
                                     min_stars=get_env_var_int_or_none('MIN_STARS'),
                                     min_forks=get_env_var_int_or_none('MIN_FORKS'),
                                     last_updated=get_env_var_string('LAST_UPDATED'))

    app = GitHubIndexer(indexer_type=IndexerType.GITHUB,
                        rabbitmq_parameters=rabbit, database_parameters=database,
                        rejected_publish_delay=get_env_var_int('RMQ_REJECTED_PUBLISH_DELAY', 10),
                        github_indexer_parameters=github)

    app.run()
