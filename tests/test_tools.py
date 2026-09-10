"""工具层单元测试。"""

import pytest

from todo_agent.store import TodoStore
from todo_agent.tools import TOOLS, execute_tool


@pytest.fixture
def store() -> TodoStore:
    """每个测试都拿到一个干净的存储实例。"""
    return TodoStore()


def test_tools_contains_exactly_four_functions() -> None:
    names = [t["function"]["name"] for t in TOOLS]
    assert names == ["add_todo", "list_todos", "complete_todo", "delete_todo"]


def test_each_tool_has_valid_schema() -> None:
    for tool in TOOLS:
        assert tool["type"] == "function"
        assert isinstance(tool["function"]["name"], str)
        assert tool["function"]["parameters"]["type"] == "object"


def test_add_todo_returns_message_and_persists(store: TodoStore) -> None:
    result = execute_tool("add_todo", {"title": "买牛奶"}, store)

    assert "买牛奶" in result
    todos = store.list()
    assert len(todos) == 1
    assert todos[0].title == "买牛奶"


def test_list_todos_empty(store: TodoStore) -> None:
    assert execute_tool("list_todos", {}, store) == "当前没有待办事项。"


def test_list_todos_with_items(store: TodoStore) -> None:
    store.add("买牛奶")
    store.add("写周报")

    result = execute_tool("list_todos", {}, store)

    assert "买牛奶" in result
    assert "写周报" in result


def test_complete_todo_success(store: TodoStore) -> None:
    todo = store.add("写周报")

    result = execute_tool("complete_todo", {"todo_id": todo.id}, store)

    assert "写周报" in result
    assert todo.done is True


def test_complete_todo_missing(store: TodoStore) -> None:
    result = execute_tool("complete_todo", {"todo_id": 999}, store)

    assert "未找到" in result
    assert "999" in result


def test_delete_todo_success(store: TodoStore) -> None:
    todo = store.add("买牛奶")

    result = execute_tool("delete_todo", {"todo_id": todo.id}, store)

    assert "已删除" in result
    assert store.get(todo.id) is None


def test_delete_todo_missing(store: TodoStore) -> None:
    result = execute_tool("delete_todo", {"todo_id": 999}, store)

    assert "未找到" in result
    assert "999" in result


def test_unknown_tool(store: TodoStore) -> None:
    result = execute_tool("nonexistent_tool", {}, store)

    assert "未知工具" in result
