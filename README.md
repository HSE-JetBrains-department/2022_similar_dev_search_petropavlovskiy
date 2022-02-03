# Курс "Code as Data"
**Петропавловский Андрей**  
## Содержание учебной дисциплины
- Работа с `git'ом`
- Работа с `git hosting'ами`.
- Работа с `GitHub API`.
- Классификация языков программирования.
- Работа с AST представленияем программ.
- Работа с библиотеками для работы с `AST`.
- Работа с различными проектами: `GitBase`,  `jgit-spark-connector`
- Описание пайплайна для работы с исходным кодом.
```diff
## @@Этапы работы с проектом@@
```
- Работа с <span style="color:blue">GitHub API</span>
    - Изучение документации
    - Изучение различных способов получения информации о пользователях и их репозиториях
    - Изучение информации о получении информации из самих репозиториев
- Получение данных о пользователях github
    - Разделение пользователей
        - Получение информации о ЯП, на которых пишет разработчик
        - Получение самого написаного кода 
        - Разделение по задачам, для которого был написан код (какие фреймворки использует разработчик)
- Работа с утилитами, дающими возможность получение информации о пользователях [[`enry`](https://github.com/go-enry/go-enry), [`tree-sitter`](https://github.com/tree-sitter/tree-sitter)]
    - Получение ЯП, на которых пишет разработчик
        - Сколько всего было написано ращработчиком на том или ином ЯП
    - Получение имен переменных, которые чаще всего дает разработчик  
- Написание готового проекта
    - Компановка модулей проекта:
        - Классы, работающие с API
        - Классы работающие с утилитами
    - Создание минимального интерфейса
- Покрытие его тестами, создание автоматизации и тд.
    
