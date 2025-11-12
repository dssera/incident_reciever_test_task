# Incident Handler Bot

Telegram-бот и REST API для быстрого создания и просмотра инцидентов.

---

## Особенности

- Сервис униврсален - прокидываем разные env переменные и получаем несколько аппок для разных типов инцидентов
- Просмотр всех инцидентов командой `/get_<SERVICE_SOURCE>`.

---

## Эндпоинты

- POST /incidents/ - Создание инцидента
- GET /incidents/ - Получние инцидентов с фильтром по статусу
- POST /webhook/{token}/ - Вебхук для Telegram 

---

## Инструкция по запуску

Экономлю ваше время (и свое на докере) и сразу даю ссылку на готового бота + апи на примере CityDrive:)

- Telegram-бот: [@incidenthandlerjk34bot](https://t.me/incidenthandlerjk34bot)  
- Swagger-документация API: [https://c7080b3aaecf.ngrok-free.app/docs](https://c7080b3aaecf.ngrok-free.app/docs)

