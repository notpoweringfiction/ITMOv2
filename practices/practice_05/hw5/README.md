ДЗ 5 · Две команды — одна фича

Фича: управление подписчиками с фильтром и экспортом

- UI: CLI с командами `subscribe`, `list`, `export`.
- Логика: хранение подписчиков, фильтрация по префиксу (регистр игнорируется), экспорт видимого списка в файл.
- SDD-фреймворк: BDD/Gherkin (две спеки — UI и логика).

Как запустить проверки

1. Локальные unit и e2e тесты:

   ```
   make -C practices/practice_05/hw5 test
   ```

2. Ручной прогон CLI (пример):

   ```
   export SUBSCRIBERS_DB=/tmp/hw5_subs.json
   python practices/practice_05/hw5/cli.py subscribe Ann
   python practices/practice_05/hw5/cli.py subscribe Bob
   python practices/practice_05/hw5/cli.py list --prefix a
   python practices/practice_05/hw5/cli.py export --prefix b --out /tmp/out.txt
   ```

Структура

- specs/ui.feature — сценарии UI (CLI)
- specs/logic.feature — сценарии логики
- service_ext.py — функции логики и хранилище
- cli.py — интерфейс командной строки
- tests/ — unit и e2e проверки
- REFLECTION.md — сравнение Gherkin и OpenSpec и выводы
