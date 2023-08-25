# Yacut

Yacut - это учебный проект, который позволяет создавать короткие ссылки для любых веб сайтов.

## Технологический стек

* Flask
* SQLAlchemy
* Jinja

## Установка

Чтобы установить проект, выполните следующие команды:

```
git clone git@github.com:Qerced/yacut.git
cd Yacut
pip install -r requirements.txt
```

## Запуск

Чтобы запустить проект, выполните следующую команду:

```
flask run
```

Для заполнения env, руководствуйтесь следующим примером:

```
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=your_secret_key
```

## Использование

Чтобы добавить короткую ссылку, перейдите на страницу `/` и введите URL веб сайта в поле `Длинная ссылка`. Нажмите кнопку `Создать`. Проект сгенерирует случайную короткую ссылку и отобразит её в поле `Ваша новая ссылка готова:`.

## API

Yacut также реализует API со следующими эндпоинтами:

* `/api/id/` POST - принимает параметры в виде `url`: string и `short_link`: string.
* `/api/id/<short_id>/` GET - возвращает `url`: string.

## Пример использования API

Чтобы добавить короткую ссылку с помощью API, выполните следующий запрос:

```
curl -d '{ "url": "https://www.google.com", "short_link": "example" }' -H "Content-Type: application/json" -X POST http://localhost:5000/api/id/
```

Чтобы получить URL веб сайта по его короткой ссылке с помощью API, выполните следующий запрос:

```
curl http://localhost:5000/api/id/example/
```

## Авторы:
- [Vakauskas Vitas](https://github.com/Qerced)
