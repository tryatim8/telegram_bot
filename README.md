# Программа телеграм-бота работы с клиентами в сфере бизнес-продаж
___
## Описание
* Мотивация
  * Создавать телеграм-бота это база любого питониста, которую необходимо освоить.
  * Данная программа в процессе обучения на платформе Skillbox является своего рода финальной работой
  * Возможность применить и закрепить знания и навыки, полученные на курсе Основы Python
  * Практический багаж для будущего портфолио, который никогда не лишний.
* Цели и задачи
  * __многопользовательский__ интерфейс телеграм-бота для взаимодействия с клиентом (TelegramAPI)
  * Реляционная база данных для хранения истории команд, отправленных телеграм-боту (peeweeORM + SqliteDatabase)
  * Механизм запроса и вывода результатов поиска товаров (AmazonRestyleAPI)
* Достоинства
  * Многопользовательский интерфейс
  * Сокрытие чувствительных и приватных данных
  * Структурированность слоёв
  * Простота основного кода
  * Преимущественно функциональное и объектно-ориентированное программирование
## Установка
1. Клонируйте репозиторий в среду разработки.
2. Обновите интерпретатор до Python 3.12 или новее.
3. Выполните установку пакетов через терминал среды разработки:
`pip install -r requirements.txt`
4. Выполните подписку на сайте [AmazonRestylerAPI](https://rapidapi.com/ru/restyler/api/amazon23/)
5. Переименуйте файл .env.templates в .env
6. Из вышеуказанного сайта скопируйте в файл .env:
   1. X-RapidAPI-Key в переменную SITE_API
   2. X-RapidAPI-Host в переменную HOST_API
7. Создайте своего телеграм-бота с помощью [BotFather](https://telegram.me/BotFather)
8. Скопируйте __токен__ созданного телеграм-бота в переменную BOT_TOKEN файла .env
## Использование
Способы запуска программы:
- Через терминал среды разработки `python main.py`
- Запуск файла main.py через проводник
- Запуск файла main.py в среде разработки

Теперь ваши клиенты могут пользоваться чат-ботом, пока запущена ваша программа.
## Помощь проекту
Отзывы и предложения пишите на почту tryatim8@mail.ru

Счёт для пожертвований в рублях: "Чей-то банковский счёт"
## Участники

Куратор работы
: Александр Ольховик

Студент курса
: Тимофей Прокофьев