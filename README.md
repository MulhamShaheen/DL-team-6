# Проект по детекции и классификации знаков дорожного движения

## Содержание

- [Описание работы сервиса](#summary)
- [Архитектура сервиса](#architecture)
- [Deploy](#deploy)
- [Пример работы сервиса](#demo)
- [FAQ](#faq)
- [Команда проекта](#project-team)
- [Ссылки](#links)


### Summary
Цель: создание сервиса для детекции классификации знаков дорожного движения.

Данные: В качестве датасета была использована сокращенныя версия датасета российских знаков дорожного движения https://graphics.cs.msu.ru/projects/traffic-sign-recognition.html. В датасете 6 основных классов знаков дорожного движения (на основе классификации в ГОСТ Р 52289-2019):
1. С синей каймой
2. Синий прямоугольник
3. Опасность
4. Главная дорога
5. Предписывающие
6. Запрещающие 

Поскольку в исходном датасете содержится более 100 тысяч изображений, было принято решение сократить его размер до 10 867 изображений (порядка 1800 изображений каждого класса).

Используемая модель и эксперименты: в качестве сравниваемых моделей были выбраны модели архитектуры YOLOv5s и YOLOv8s. В ходе сравнения было определено, что качество работы модели v8 выше (подробные результаты можно найти в разделе эксперименты). Кроме того, было определено, что наилучшее качество работы достигается при размере изображения 1280.
Лучшая модель была интегрирована в сервис.

Дальнейшая работа: В ходе дальнейшей работы можно:
1. Улучшить сервис, сделав его более привлекательным для пользователей.
2. Кроме детекции и классификации на 6 групп с помощью исходных моделей, можно добавить классификаторы для классификации сэмплов классов на подклассы (так как, очевидно, важен не только тип знака, но и конкретное его значение). Для классификации можно воспользоваться, например, классификатором на основе архитектуры ResNet.
### Architecture
![pipeline(4)](https://github.com/MulhamShaheen/DL-team-6/assets/74207896/cd15bd7e-6ae6-4ad9-b10f-182b859c58e5)
Схема с архитектурой сервиса

### Deploy

Система состоит из трех серисов:

- Django - веб-приложение, которое позволяет пользователю вводить ссылку на видео на ютубе, и получить видео с bounding box
- RabbitMQ - как брокер задач для организации очередей сообщений между интересом и приложением
- Fast API - АПИ инференса модели дитекции, через его отправляются результаты работы модели 

Using Docker compose, the system can be started using the following steps:
- Клонируйте данный репозиторий
- Запустите docker на своем компьютере
- docker-compose build
- docker-compose up -d

### Demo

Гифка с результатом работы модели

![shorts_MjnhWCEmpbg](https://github.com/MulhamShaheen/DL-team-6/assets/74207896/7c9e51e4-66c6-4aad-91ad-8ebae462c499)

#### Демонстрации работы API в postman

![api.gif](images%2Fapi.gif)

#### Главный экран веб-приложения

![img.png](images/img.png)

### FAQ

Здесь будут ответы на какие-нибудь вопросы, если такие возникнут

### Project team

Сюда инфу о нас по ролям + линкедин

### Links

Сюда добавим ссылки на датасеты, когда приведем их в порядок
