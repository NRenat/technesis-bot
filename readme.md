# Technesis bot
Телеграм бот, который получает файл-таблицу .xlsx, .ods, .xls со столбцами title, url, xpath.

Бот проходит по всем предложенным ссылкам и собирает цены товаров, расположенных по xpath.

Результаты выводит пользователю и сохраняет в БД.

## Запуск бота:
* Создать и заполнить файл .env в соответствии с .env.example
* Установить зависимости
```bash
pip install -r requirements.txt
```
* Применить миграции
```bash
alembic upgrade head
```
* Запустить бота 
 
Для windows:
```bash
python bot/bot.py
```
Для linux/macos
```bash
python3 bot/bot.py
```

## Технологии
* aiogram
* sqlalchemy
* pydantic
* alembic
* httpx
* pandas
