# Публикатор комиксов во Вконтакте

Скрипт предназначен для публикации комиксов с [сайта](https://xkcd.com/) в сообщество соцсети [Вконтакте](https://vk.com).


## Установка

Для установки зависимостей в командной строке введите:

```
pip install -r requirements.txt
```
Также необходимо создать группу во [Вконтакте](https://vk.com), в которую вы будете постить комиксы. Далее создайте приложение по [ссылке](https://dev.vk.com/), в качестве типа приложения следует указать standalone. 
Cледующим шагом нажмите на кнопку “Редактировать” для нового приложения, в адресной строке вы увидите его client_id. 
Также нужно получить `acess_token`, для этого в адресной строке введите следующий адресс `https://oauth.vk.com/authorize?client_id=1&display=page&scope=photos,%20groups,wall,offline&response_type=token&v=5.131`, в котором вам нужно в параметре `client_id` подставить свой, полученный в предыдущем шаге. Далее перейдите по ссылке, в адресной строке появится ваш `acess_token`. 
После вам нужно создать файл `.env`, в котором положите в переменную `VK_ACESS_TOKEN` ваш `acess_token`, выглядит следующим образом:

```
VK_ACESS_TOKEN=533bacf01e1165b57531ad114461ae8736d6506a3
``` 
Получаем `group_id` по [ссылке](https://regvk.com/id/), помещаем его в переменную `VK_GROUP_ID` в файл `.env` аналогичным образом:
```
VK_GROUP_ID=250047464
``` 

## Запуск

Для запуска проргаммы вам необходимо (для пользователей Windows):
```
python main.py
``` 
или (для Linux):
```
python3 main.py
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).