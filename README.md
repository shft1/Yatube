### API Описание

В проекте описано API для социальной сети Yatube, через API можно получать и записывать информацию о посте, оставлять и получать комментарии, подписываться на пользователей, получать список собственных подписок, получать группу, в которой находится пост. Ауентификация происходит на основе JWT-токена.


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone ...
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Примеры запросов


# Создание поста:

<img width="1264" alt="image" src="https://github.com/shft1/api_final_yatube/assets/143039459/1efc197a-7ce1-4907-94ff-198e7dccae6e">



# Создание комментария:

<img width="1272" alt="image" src="https://github.com/shft1/api_final_yatube/assets/143039459/338cd2cc-3737-40b9-8538-38742e27a2e7">



# Получение списка групп:


<img width="1263" alt="image" src="https://github.com/shft1/api_final_yatube/assets/143039459/2bf1892e-e37b-4e8b-adc3-576999bc50bc">
