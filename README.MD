Музыкальный Бот в Телеграме

Этот бот может проигрывать музыку загруженую пользователем через музыкальный архив, можно создавать
отделный сборник песен а также может искать музыку в локальных папках и загружать ее в музыкальный архив


Требования



python 3.8 и выше


Установить



git clone https://github.com/razielSan/mucic_bot.git
cd mucic_bot
pip install -r requirements.txt


Использование



Создайте в директории mucic_bot/app/ файл .env

В файле .env создайте

TOKEN:Токен_Вашего_Телеграм_Бота
SQLITE_BASE:sqlite:///music_play.db
MUSIC_PATH:Путь_До_Ваших_Музыкальных_Файлов

Пример

TOKEN:8061082875:CCCCcmcSoIcr3o5nnCCpM6XUYKEj3gNXlk8

Пример

D:\Media\Music

Для удачого парсинга ваших музыкальных файлов исполнитель должен быть в формате
Название_Исполнителя (Название Страны)
D:\Media\Music\Другое\Тараканы (Москва)

Альбомы исполнителя должны быть в формате 

(Год_Выпуска_Альбома)-Называние альбома
(Год_Выпуска_Альбома) Называние альбома
D:\Media\Music\Другое\Тараканы (Москва)\(1992)-Duty free songs


Запуск программы




В консоли

Перейти в директорию mucic_bot/app

cd mucic_bot/app
app.py

