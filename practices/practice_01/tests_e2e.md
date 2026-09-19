# E2E-проверки

| Сценарий пользователя | Предусловия | Действие | Наблюдаемый результат | Evidence |
|---|---|---|---|---|
| Позитивный | Доступен /api/reviews | POST { diff: "..." } | 200 OK и ReviewResponse { comment } | см. prompt_P1_02.md#output (summary/checks) |
| Негативный | Нет поля diff | POST {} | 500 Internal Server Error (KeyError) | см. prompt_P1_02.md#output checks (Risk 1): KeyError подтверждает отсутствие валидации поля diff |
| Граничный | Превышение лимита | POST с большим diff | Рост латентности или сбой (напр., таймаут/500) | см. prompt_P1_02.md#output checks (Risk 2): отсутствие ограничений на размер/таймауты |

## Как использовали AI

- Строка в [`prompts.md`](prompts.md):
- Что проверили и исправили сами:
