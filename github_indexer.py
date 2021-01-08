import configparser
from typing import Optional

from fregeindexerlib import Indexer, CrawlResult, RabbitMQConnectionParameters, IndexerType, \
    DatabaseConnectionParameters, Language
from github import Github

# using username and password

LANGUAGES = {"C": 1,
             "C++": 2,
             "C#": 3,
             "CSS": 4,
             "Java": 5,
             "JavaScript": 6,
             "PHP": 7,
             "Python": 8,
             "Ruby": 9}


class GitHubIndexer(Indexer):
    BASE_API_URL = 'https://gitlab.com/api/v4/projects'

    def __init__(self, indexer_type: IndexerType, rabbitmq_parameters: RabbitMQConnectionParameters,
                 database_parameters: DatabaseConnectionParameters, rejected_publish_delay: int,
                 config: configparser):
        super().__init__(indexer_type, rabbitmq_parameters, database_parameters, rejected_publish_delay)

        self.github_indexer_parameters = config
        self.g = Github(config['DEFAULT']['GITHUB_PERSONAL_TOKEN'])
        self.iter = self.__get_next_repo()

    def __get_next_repo(self):
        min_stars = self.github_indexer_parameters['DEFAULT']['MIN_STARS']
        min_forks = self.github_indexer_parameters['DEFAULT']['MIN_FORKS']
        last_updated = self.github_indexer_parameters['DEFAULT']['LAST_UPDATED']

        for page in range(1000):
            list_of_repos = self.g.search_repositories(query=f'forks:>={min_forks} stars:>={min_stars}'
                                                             f' is:public pushed:>={last_updated}',
                                                       sort='stars', page=page)
            for repo in list_of_repos:
                languages = {x: False for x in Language}
                for x in repo.get_languages().keys():
                    y = LANGUAGES.get(x, 0)
                    if y:
                        languages[Language(y)] = True

                yield CrawlResult(
                    id=str(repo.id),
                    repo_url=repo.clone_url,
                    git_url=repo.html_url,
                    languages=languages
                )

    def crawl_next_repository(self, prev_repository_id: Optional[str]) -> Optional[CrawlResult]:
        self.log.debug('Start a new crawl')
        return next(self.iter)
