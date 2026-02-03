# Start

- [x] Init project
- [x] Comtit init

## DB:

- [x] Project model
- [x] Done project model
- [x] Image model

- [x] Run mysql
- [x] Create tables
- [x] Make first migration: config alembic

## Core:

- [x] Create base repository
- [x] Create project repo
- [x] Create image repo

- [x] Create project schemas
- [x] Create image schemas

## FastApi:

- [x] Create depends for repos
- [x] Create depends for database session

## Routers:

- [x] Add params offset and limit for get_all_projects router:
  - [x] Add count of all projects from db to response and response model: { items: [], count: int }
  - [x] Add count and items model to done projects
  - [x] Add done projects router
- [x] Add sort_by(by description or by name, for example)
- [x] Add desc param for reverse the sort
- [x] Get random projects with limit param

- [x] Done projects(get_all with offset and limit)

- [x] Create project(upload files)
- [x] Create all projects

- [x] При удалении преоктов проходиться по его картинкам и удалять последовательно

- [x] Нужно чтобы я передавал depends, передавал туда сортировку и оно отдавало Enum
- [x] Нужно чтобы при загрузке картинок они сжималась
- [x] Переместить папку uploads
- [x] Пофиксить count

### Messages:

- [ ] Ручка для создания сообщений и их отправки в тг бота
- [ ] Tg bot для отправки сообщений досутпным юзера(админы)
- username и chat_id это все для Message в бд.
  Когда оптарвляем сообщения создаем список чатов(usernames и chat_ids),
  которые после отправки сообщений пихаем в бд.

- Список чатов нужно получать из get_updates и из бд.
  Так же если в бд нету того чата который есть в updates, то его нужно туда добавить
  Если updates пустой, то отпрапвляем только тем чатам, которые есть в бд.

Загрузка картинок: планиуреться загружать картинки отдельно от проектов.

- Добавить свойство public: boolean в модели project и done_project
  в контрактах этого свойства не должно быть

  при создании на POST api/v1/projects и POST api/v1/done_projects свойство по умолчанию на false,
  в реквест контракте оно необязательно

  на PUT api/v1/projects и PUT api/v1/done_projects должна быт возмозможность это свойство изменить,
  в реквест контракте оно нужно

  ручки GET api/v1/projects/ramdom, GET api/v1/done_projects/random выводят только то где public = true

  ручки GET /api/v1/projects, GET api/v1/done_projects по умолчанию выводят только public=true,
  но должен быть фильтр позволяющий вывести public=false для админки

## Как решить проблему с ветвлением гит и различными версиямиями бд между ветками:

- Если нужно перейти в другую ветку где все еще старые модели, то нужно делать downgrade на общего предка:
  То есть в старой ветке получить последнюю версию:

```bash
alembic heads
```

Потом перейти в более новую и выполнить:

```bash
alembic downgrade <head_version_id>
```

Далее когда придет время сливать ветки, ты просто сливаешь их как обычно.
Но алембик не повзолит тебе сделать upgrade head, ведь теперь он тоже имеет две цепочки развития.
Нужно делать слияние веток alembic:

```bash
alembic merge -m "merge main and work heads" head1_id head2_id
```

d
