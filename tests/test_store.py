"""TodoStore CRUD 单元测试。"""

import pytest

from todo_agent.store import TodoStore


@pytest.fixture
def store() -> TodoStore:
    """每个测试都拿到一个干净的存储实例。"""
    return TodoStore()


def test_add_assigns_incrementing_ids(store: TodoStore) -> None:
    first = store.add("买牛奶")
    second = store.add("写周报")

    assert first.id == 1
    assert second.id == 2
    assert store.get(1) is first
    assert store.get(2) is second


def test_list_empty(store: TodoStore) -> None:
    assert store.list() == []


def test_list_returns_in_id_order(store: TodoStore) -> None:
    store.add("第三项")
    store.add("第一项")
    store.add("第二项")

    titles = [todo.title for todo in store.list()]
    assert titles == ["第三项", "第一项", "第二项"]


def test_get_returns_none_for_missing_id(store: TodoStore) -> None:
    assert store.get(999) is None


def test_complete_marks_done(store: TodoStore) -> None:
    todo = store.add("写周报")

    result = store.complete(todo.id)

    assert result is todo
    assert todo.done is True


def test_complete_missing_returns_none(store: TodoStore) -> None:
    assert store.complete(999) is None


def test_complete_is_idempotent(store: TodoStore) -> None:
    todo = store.add("写周报")
    store.complete(todo.id)
    store.complete(todo.id)

    assert todo.done is True


def test_delete_returns_true_and_removes(store: TodoStore) -> None:
    todo = store.add("买牛奶")

    assert store.delete(todo.id) is True
    assert store.get(todo.id) is None


def test_delete_missing_returns_false(store: TodoStore) -> None:
    assert store.delete(999) is False
