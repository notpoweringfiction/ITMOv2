import json
import os
from typing import List, Set


# Хранилище: порядок добавления важен для UX; поддерживаем уникальность.
_state: List[str] = []
_index: Set[str] = set()


def _db_path() -> str:
    # Можно указать путь через переменную окружения; по умолчанию — рядом с модулем
    return os.environ.get("SUBSCRIBERS_DB", os.path.join(os.path.dirname(__file__), "subscribers.json"))


def load_state() -> None:
    _state.clear()
    _index.clear()
    path = _db_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                for x in data:
                    s = str(x)
                    if s not in _index:
                        _state.append(s)
                        _index.add(s)
        except Exception:
            # Повреждённый файл игнорируем как пустой
            _state.clear()
            _index.clear()


def save_state() -> None:
    path = _db_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(list(_state), f, ensure_ascii=False, indent=2)


def clear_state() -> None:
    _state.clear()
    _index.clear()
    path = _db_path()
    if os.path.exists(path):
        os.remove(path)


def add_subscriber(name: str) -> dict:
    if not isinstance(name, str) or not name.strip():
        raise ValueError("empty name")
    clean = name.strip()
    if clean not in _index:
        _state.append(clean)
        _index.add(clean)
    return {"subscribed": True}


def list_subscribers(prefix: str = "") -> List[str]:
    # Порядок — как добавлялись
    items = list(_state)
    if prefix:
        p = prefix.lower()
        items = [x for x in items if x.lower().startswith(p)]
    return items


def export_subscribers(prefix: str, path: str) -> None:
    if not isinstance(path, str) or not path:
        raise ValueError("invalid output path")
    items = list_subscribers(prefix)
    with open(path, "w", encoding="utf-8") as f:
        for name in items:
            f.write(name + "\n")
