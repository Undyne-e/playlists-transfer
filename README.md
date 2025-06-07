Работа сервиса направлена на быстрый и удобный перенос любого плейлиста между популярными музыкальными стримингами (Яндекс музыка, Youtube music, Spotify)

![image](https://github.com/user-attachments/assets/e9c823fb-2c85-4a6e-b393-207a1127ce2d)

# Как запустить веб-сервис?
В первую очередь надо будет настроить .env файлы

## Настройка .env для backend

1. cd backend --> создайте новый файл .env --> скопируйте туда содержимое .env.example

2. запишите для #database и #pgadmin в .env свои данные

3. теперь, запустив Docker Desktop, вы можете, находясь в директории /backend, создать БД - пропишите "docker compose up -d"     (для остановки - "docker compose down")

4. На данный момент в сервис внедрена работа с апи Яндекс музыки (Yandex Oauth); Youtube музыки (Youtube Data API v3); Spotify (Oauth), для их работы нужно получить client_secrets (см. далее)

5. ДЛЯ ЯНДЕКС МУЗЫКИ:
    - переходим на https://oauth.yandex.ru/; нажимаем "создать приложение"
    - называем его и указываем Веб-сервисы
    - предоставляем ко всему доступ
    - в Redirect URI указываем http://localhost:5173/yandexcallback
    - в Хосте - http://localhost:5173
    - подтверждаем и сохраняем --> получаем CLIENT_ID и CLIENT_SECRET --> вставляем их в .env

6. ДЛЯ YOUTUBE МУЗЫКИ:
    - переходим на https://cloud.google.com/appengine/docs/standard/nodejs/building-app/creating-project; листаем чуть вниз и нажимаем "Go to project selector"
    - далее create project и называем его как-нибудь
    - APIs & Services --> Credentials --> Create credentials --> API key --> получаем ключ (его никуда вставлять не надо)
    - APIs & Services --> Credentials --> Create credentials --> OAuth client ID --> CONFIGURE CONSENT SCREEN --> GET STARTED
    - Заполняем все нужные данные; в графе Audience выбираем External
    - после этого нажимаем CREATE OAUTH CLIENT --> Application type - выбираем Web Application
    - в Authorized JavaScript origins указываем - http://localhost:5173
    - в Authorized redirect URIs указываем - http://localhost:5173/googlecallback
    - нажимаем CREATE 
    - в открывшемся списке видим нашего клиента --> справа скачиваем JSON с нужными данными
    - в окошке скачивания можем сразу скопировать CLIENT_ID и CLIENT_SECRET / либо же копируем из скачанного JSON файла --> вставляем данные в .env
    - скачанный JSON надо просто переименовать в client_secret.json и вставить его в эту же директорию /backend 
    - во вкладке Audience в графе Test users укажите свою gmail почту
    - возвращаемся во вкладку APIs & Services --> Library --> листаем чуть ниже и выбираем YouTube Data API v3 --> жмем ENABLE

7. ДЛЯ SPOTIFY:
    - переходим на https://developer.spotify.com/documentation/web-api/concepts/apps
    - если нет аккаунта - создаем, и следуем простой инструкции по созданию spotify web app
    - в поле APIs used достаточно указать только - Web API
    - в настройках нашего приложения в поле Redirect URIs указываем - http://localhost:5173/spotifycallback
    - теперь можем увидеть свои Client ID и Client secret для Spotify, которые копируем в .env в нужные графы


## Настройка .env для frontend

1. cd ../frontend --> создайте новый файл .env --> скопируйте туда содержимое .env.example (уже из директории frontend)

2. укажите соответствующие CLIENT_ID для яндекса, google и spotify которые вы уже получили раннее

3. перейдите по https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d --> авторизуемся при необходимости и предоставляем доступ --> скопируйте в адресной строке access token и вставте его в .env (в графу VITE_YANDEX_TOKEN)


# Запуск сервиса

1. возвращаемся в корень - cd .. --> прописываем "python -m venv .venv" и ".venv\Scripts\activate"

2. cd backend --> pip install -r requirements.txt

3. здесь сразу же запускаем БД (docker compose up -d)

4. запуск backend: "python manage.py makemigrations" --> "python manage.py migrate" --> "python manage.py runserver"

5. запуск frontend: cd ../frontend --> npm install --> npm run dev

6. теперь frontend доступен по адресу - http://localhost:5173/; backend по адресу - http://localhost:8000/


# Как пользоваться сервисом?

1. перейдем на http://localhost:5173/Register и пройдем этап регистрации и логина пользователя (подтвердить почту можно по ссылке, которая появится в терминале)

2. после перехода на главную страничку можем выбрать нужный музыкальный сервис для скачивания плейлиста(ов) (!важно - чтобы перенести плейлист с какого-либо сервиса требуется пройти этап авторизации на этом сервисе, который доступен по этим самым кнопкам выбора сервиса и авторизации (получения токенов))

3. после скачивания нужных плейлистов (когда плейлист скачается, рядом появится галочка) и авторизаций на сервисах, нажимаем на кнопку "Перенести плейлист", можем выбрать нужный плейлист в списке (отображаться будут все скачанные вами плейлисты). Далее выбираем принимающий сервис, нажимаем перенести и ждем

4. на данный момент можно проводить операции через сервисы Youtube music; Yandex music; Spotify без проблем, однако для Youtube Data API v3 существует лимит квот по операциям в день, о них можно почитать тут - https://developers.google.com/youtube/v3/determine_quota_cost?hl=ru.

5. Также в разделе аккаунта можно удалить аккаунт или выйти из системы
