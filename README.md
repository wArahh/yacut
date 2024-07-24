# Сервис укорачивания ссылок YaCut
## Команды развертывания
Клонируйте репозиторий к себе на компьютер при помощи команды:
```
git clone git@github.com:wArahh/yacut.git
```

Создайте, активируйте виртуальное окружение и установите зависимости:
```
cd yacut/
```
```
python -m venv venv
```
```
pip install -r requirements.txt
```
### создайте .env файл по примеру:
```
FLASK_APP=yacut
FLASK_DEBUG=1
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=YOUR_SECRET_KEY
```
### запустите проект командой
```
flask run
```
### документация к api лежит в файле 
```
openapi.yml
```


## Стек
- Python 3.9
- flask 3.0.2
- Prettytable
## Автор
- [Макаренко Никита](https://github.com/wArahh)
