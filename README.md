# ByBit parsing
Этот проект реализует парсинг сайта новостей (https://announcements.bybit.com/).

## Установка

### Требования
- [git](https://git-scm.com/)
- [docker](https://docs.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)

### Запуск проекта
1. Клонируйте репозиторий:
`git clone https://github.com/bloodeRok/news_parsing.git`.
2. Перейдите в директорию проекта: `cd "path to project"`.
3. Запустите проект с помощью docker-compose: `docker-compose up -d --build`.

### Работа с проектом
После запуска проекта в корне программы будет автоматически создан .csv файл с новостями. Периодически файл обновляется.
