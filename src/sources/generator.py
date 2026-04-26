from collections.abc import Iterable
from dataclasses import dataclass
from faker import Faker

from src.models.descriptors import Priority
from src.models.task import Task
from src.models.task_status import TaskStatus
from src.sources.repository import register_source

fake = Faker('ru')

@dataclass
class GeneratorSource:
    '''
    Генерирует count задач с id вида <generator:n>.
    '''
    name: str = "generator"
    count: int = 5

    def fetch(self) -> Iterable[Task]:
        for i in range(1, self.count + 1):
            priority_obj = Priority()
            yield Task(
                id=f"{self.name}:{i}",
                description=fake.sentence(nb_words=4).rstrip('.'),
                priority=fake.random_int(
                    priority_obj.min_value,
                    priority_obj.max_value,
                ),
                status=fake.random_element(elements=list(TaskStatus))
            )


@register_source("generator")
def create_generator_source(count: int = 5) -> GeneratorSource:
    return GeneratorSource(count=count)
