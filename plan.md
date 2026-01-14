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
  - [ ] Add done projects router
- [x] Add sort_by(by description or by name, for example)
- [x] Add desc param for reverse the sort
- [x] Get random projects with limit param

- [x] Done projects(get_all with offset and limit)

- [x] Create project(upload files)
- [x] Create all projects

Загрузка картинок: планиуреться загружать картинки отдельно от проектов.
