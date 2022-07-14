from dataclasses import dataclass
from django.contrib.auth.models import User


@dataclass(frozen=True)
class ListEntity:
    title: str
    owner: User

@dataclass(frozen=True)
class TaskEntity:
    body: str
    task_list: ListEntity
    priority: str
