import dataclasses


@dataclasses.dataclass
class Worker:
    email: str
    password: str
    usage_count: int
    is_work: bool


@dataclasses.dataclass
class Task:
    link: str
    finished: bool
    worker: Worker
    worker_in_group: bool