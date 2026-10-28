Feature: CLI управления подписчиками
  Как пользователь CLI
  Я хочу подписывать имена, просматривать список с фильтром и экспортировать видимое
  Чтобы быстро работать со списком без ручной фильтрации

  Background:
    Given пустое хранилище подписчиков

  Scenario: Подписка успешна
    When я выполняю команду "subscribe Ann"
    Then вывод содержит "subscribed: true"
    And состояние содержит имена:
      | name |
      | Ann  |

  Scenario: Пустое имя — ошибка
    When я выполняю команду "subscribe  \t  "
    Then код возврата не 0
    And stderr содержит "empty name"

  Scenario: Список без фильтра
    Given в хранилище есть имена:
      | name |
      | Ann  |
      | Bob  |
    When я выполняю команду "list"
    Then вывод содержит строки в порядке:
      | line |
      | Ann  |
      | Bob  |

  Scenario: Фильтрация по префиксу, регистр не важен
    Given в хранилище есть имена:
      | name |
      | Ann  |
      | alice|
      | Bob  |
    When я выполняю команду "list --prefix a"
    Then вывод содержит строки в порядке:
      | line |
      | Ann  |
      | alice|

  Scenario: Экспорт видимого списка
    Given в хранилище есть имена:
      | name |
      | Ann  |
      | Bob  |
      | Alice|
    When я выполняю команду "export --prefix a --out out.txt"
    Then файл "out.txt" содержит строки в порядке:
      | line |
      | Ann  |
      | Alice|
