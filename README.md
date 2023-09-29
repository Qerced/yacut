# Сервис коротких ссылок

Проект ассоциирует длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

## Технологический стек

* Flask
* SQLAlchemy
* Jinja

## Установка

Для установики проекта, выполните следующие команды:

```
git clone git@github.com:Qerced/yacut.git
cd Yacut
pip install -r requirements.txt
```

## Запуск

Перед запуском наполните env для корректной работы сервиса:

```
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=your_secret_key
```

Запуск проекта осуществляется с помощью:

```
flask run
```

## Использование

Чтобы добавить короткую ссылку, перейдите на [главную страницу](http://localhost:5000/) и введите URL веб сайта в поле `Длинная ссылка`. Нажмите кнопку `Создать`. Проект сгенерирует случайную короткую ссылку и отобразит её в поле `Ваша новая ссылка готова:`.

## API

Yacut также реализует API со следующими эндпоинтами:

* `/api/id/` POST - принимает параметры в виде `url: string` и `short_link: string`.
* `/api/id/<short_id>/` GET - возвращает `url: string`.

## Пример использования API

Добавление своей короткой ссылки можно реализовать, используя данный пример для запроса:

```
curl -d '{ "url": "https://www.google.com", "short_link": "example" }' -H "Content-Type: application/json" -X POST http://localhost:5000/api/id/
```

Получение URL веб сайта осуществляется по его короткой ссылке:

```
curl http://localhost:5000/api/id/example/
```

## Авторы:
- [Vakauskas Vitas](https://github.com/Qerced)
