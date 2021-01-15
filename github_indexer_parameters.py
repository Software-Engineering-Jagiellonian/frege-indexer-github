from dataclasses import dataclass
from typing import Optional


@dataclass
class GitHubIndexerParameters:
    github_personal_token: str
    min_stars: Optional[int] = None
    min_forks: Optional[int] = None
    last_updated: Optional[str] = None