# REPORT_02: Post-Fix Verification

Summary
- Исправлены SQLi, IDOR/BAC, подмена цены, XSS и отсутствие авторизации инструментов ассистента. Добавлены тесты безопасности. Функциональные сценарии сохранены. Все тесты проходят.

Внесённые изменения
- SQL и контекст:
  - rows(query, params) — параметризованные запросы везде.
  - /profile, /search, /assistant/context переписаны на параметры.
- Контроль доступа:
  - /profile: профиль определяется по токену; query id игнорируется; при несовпадении — 403.
  - /orders GET: только заказы владельца.
  - /admin/export: только staff по роли из серверной сессии (игнор X-Role).
- Ценообразование:
  - POST /orders: цена берётся из каталога; client price игнорируется.
- Файлы:
  - /files: клиенты читают только files/<username>/<path>; staff может указывать user; запрет всего вне префикса files/.
- XSS:
  - /reviews/view: html.escape на тексте отзывов.
- Assistant инструменты (/assistant/execute):
  - Проверка токена обязательна.
  - read_file: клиент — только files/<username>/…, staff — любой files/….
  - export_profiles и delete_tree — только staff.

Проверка (до/после)
- Команды:
  - make step6; make test — все тесты проходят.
- Тесты безопасности (practices/practice_06/lab/test_security.py):
  1) /admin/export без токена — 401; клиент с X-Role — 403; staff — 200.
  2) POST /orders с price=1 — возвращает каталоговую цену (lamp=1500/chair=5000).
  3) /files для Alice с user=bob — игнорируется, возвращается чек Alice.
  4) /assistant/execute: клиент не может export_profiles/delete_tree (403); read_file только свой files/<username>/….
  5) /reviews/view экранирует HTML (видно &lt;script&gt;...).
- Функциональные тесты из поставки — зелёные.

Защита от prompt injection
- Контекст ассистента (GET /assistant/context) остаётся неизменным по требованиям задания, но решение модели не является доверенным: сервер авторизует инструменты по сессии и ролям.
- Проверено по методике: вредоносная рекомендация export/delete от модели для клиента отвергается сервером (403); для staff — разрешается.

Совместимость и сохранённая функциональность
- Клиент: логин → свой профиль → покупка по каталогу → добавление отзыва → просмотр своего чека.
- Сотрудник: экспорт профилей и операции, разрешённые staff.

Остаточные риски
- Логи содержат тела/заголовки в учебных целях; в проде требуется маскирование.
- Модель LLM всё ещё может предлагать небезопасные действия, но сервер их не выполнит.

Приложение: полезные проверки
- GET /admin/export:
  - Без токена → 401; клиент + X-Role → 403; staff токен → 200.
- POST /orders {product:"lamp", price:1} → price=1500.
- GET /files?user=bob&path=receipt.txt с токеном Alice → возвращает чек Alice.
- /reviews + "<script>…" → в HTML отрендерится &lt;script&gt;.
- /assistant/execute {decision:{tool:"export_profiles"}} с токеном клиента → 403.
