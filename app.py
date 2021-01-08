import configparser

from fregeindexerlib import RabbitMQConnectionParameters, DatabaseConnectionParameters, IndexerType

from github_indexer import GitHubIndexer

config = configparser.ConfigParser()
config.read('config.ini')

if __name__ == '__main__':
    rabbit = RabbitMQConnectionParameters(host=config['DEFAULT']['RMQ_HOST'],
                                          port=int(config['DEFAULT']['RMQ_PORT']))

    database = DatabaseConnectionParameters(host=(config['DEFAULT']['DB_HOST']),
                                            port=int(config['DEFAULT']['DB_PORT']),
                                            database=(config['DEFAULT']['DB_DATABASE']),
                                            username=(config['DEFAULT']['DB_USERNAME']),
                                            password=(config['DEFAULT']['DB_PASSWORD']))

    app = GitHubIndexer(indexer_type=IndexerType.GITHUB,
                        rabbitmq_parameters=rabbit, database_parameters=database,
                        rejected_publish_delay=int(config['DEFAULT']['RMQ_REJECTED_PUBLISH_DELAY']),
                        config=config)

    app.run()
