Feature: Логика управления подписчиками
  Как модуль логики
  Я хочу добавлять имена, фильтровать по префиксу (case-insensitive) и экспортировать видимый список
  Чтобы предоставлять консистентный API UI-слою

  Background:
    Given новое пустое состояние

  Scenario: Добавление корректного имени
    When я вызываю add_subscriber(" Ann ")
    Then результат равен {"subscribed": true}
    And состояние содержит множество:
      | name |
      | Ann  |

  Scenario: Пустое или пробельное имя
    When я вызываю add_subscriber("   ")
    Then выбрасывается ValueError с сообщением "empty name"

  Scenario: Идемпотентность добавления
    Given состояние содержит множество:
      | name |
      | Ann  |
    When я вызываю add_subscriber("Ann")
    Then размер множества равен 1

  Scenario: Фильтрация по префиксу без учета регистра
    Given состояние содержит множество:
      | name |
      | Ann  |
      | alice|
      | Bob  |
    When я вызываю list_subscribers(prefix="A")
    Then получаю список в порядке:
      | name |
      | Ann  |
      | alice|

  Scenario: Экспорт видимого списка
    Given состояние содержит множество:
      | name |
      | Ann  |
      | Bob  |
      | Alice|
    When я вызываю export_subscribers(prefix="a", path="out.txt")
    Then файл "out.txt" содержит строки в порядке:
      | line |
      | Ann  |
      | Alice|

  Scenario: Ошибка экспорта без пути
    Given состояние содержит множество:
      | name |
      | Ann  |
    When я вызываю export_subscribers(prefix="", path="")
    Then выбрасывается ValueError с сообщением "invalid output path"
