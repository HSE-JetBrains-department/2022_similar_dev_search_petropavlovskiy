# [Курс "Code as Data"](https://gist.github.com/EgorBu/e4e6cf7e2c907e29ee9730..)
```css
Петропавловский Андрей
```
## Этапы работы с проектом
- VCS
    - Изучение основ `git`
    - Изучение того, как получить коммиты и ланные из них
        - Информацию о пользователе
        - Информацию о коде
            - Блобы
            - Хеши
            - Диффы
- GitHub API
    - Изучение документации
    - Изучение различных способов получения информации о пользователях и их репозиториях
    - Изучение информации о получении информации из самих репозиториев
- Получение данных о пользователях github
    - Использование знаний из предыдущих блоков про `VSC` и `GitHub API`
    - Разделение пользователей
        - Получение информации о ЯП, на которых пишет разработчик
        - Получение самого написаного кода
        - Разделение по задачам, для которого был написан код (какие фреймворки использует разработчик)
- Использование [[`enry`](https://github.com/go-enry/go-enry), [`tree-sitter`](https://github.com/tree-sitter/tree-sitter)] для получения информации о пользователях
    - Получение ЯП, на которых пишет разработчик
    - Сколько всего было написано разработчиком на том или ином ЯП
    - Получение имен переменных, которые чаще всего дает разработчик
- Написание готового проекта
    - Компановка модулей проекта:
        - Классы, работающие с API
        - Классы работающие с утилитами
        - Создание минимального интерфейса
- Покрытие его тестами, создание автоматизации и тд.

# How application works
[![Watch the video](https://disk.yandex.ru/i/GoNYPrkyIahCSQ)](https://disk.yandex.ru/i/5iav7zEzyZxA_Q)
