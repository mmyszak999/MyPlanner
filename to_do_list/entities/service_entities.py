from dataclasses import dataclass


@dataclass(frozen=True)
class ListEntity:
    title: str


@dataclass(frozen=True)
class TaskEntity:
    body: str
    priority: str
