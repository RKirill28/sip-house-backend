# Cleand architecture

## Domain

Здесь лежат модели(типа DTO), которые еще и соблюдают правила бизнеса:

- Типа price не может ыбыть меньше или больше x
- Можно использовать Pydantic модели или dataclass, все сразу лучше не надо
- Не знает про БД, не про инфраструктуру

```py
# entities.py
from pydantic import BaseModel, ConfigDict, Field

class User(BaseModel):
    model_config = ConfigDict(from_attributes=True) # Магия для маппинга

    id: int
    balance: float = Field(ge=0) # Валидация: баланс не может быть < 0

    def can_afford(self, amount: float) -> bool:
        return self.balance >= amount
```

## Infrastructure (DB, other tools)

- Тут лежит база данных, репозитории
- Тут же другие сервисы, например TelegramService, который не знает ничего про БД или другие сервисы, изолирован
- В репозиториях происходит маппинг в моедли из уровня Domain

```py
# models.py
class UserORM(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    balance = Column(Float)

# repository.py
class UserRepository:
    def __init__(self, session): self.session = session

    async def get_by_id(self, uid: int) -> domain.User:
        db_user = await self.session.get(UserORM, uid)
        return domain.User.model_validate(db_user) if db_user else None
```

## Use cases

Сценарии, орекстрация всем, соеденяет логику.

## Главный файл, которйы все зпускает и инициализирует

main.py
