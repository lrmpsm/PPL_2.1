from collections.abc import Iterable
from dataclasses import dataclass
from faker import Faker


from src.models.task import Task
from src.sources.repository import register_source

fake = Faker('ru')

@dataclass
class GeneratorSource:
    '''
    Генерирует count задач с id вида <generator:n> и с случайным строковым payload.
    Для случайного payload используется faker.
    '''
    name: str = "generator"
    count: int = 5

    def fetch(self) -> Iterable[Task]:
        for i in range(1, self.count + 1):
            task_id = f"{self.name}:{i}"
            task_payload = fake.sentence(nb_words=3).rstrip('.')
            yield Task(
                id=task_id,
                payload=task_payload
            )


@register_source("generator")
def create_generator_source(count: int = 5) -> GeneratorSource:
    return GeneratorSource(count=count)
