"""TodoAgent 循环逻辑的单元测试（使用 mock client，不调用真实 LLM）。"""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from todo_agent.agent import TodoAgent
from todo_agent.store import TodoStore


@pytest.fixture
def store() -> TodoStore:
    """每个测试都拿到一个干净的存储实例。"""
    return TodoStore()


def make_tool_call(name: str, arguments: str, call_id: str) -> SimpleNamespace:
    """构造一个 tool_call 对象。"""
    return SimpleNamespace(
        id=call_id,
        function=SimpleNamespace(name=name, arguments=arguments),
    )


def make_response(content=None, tool_calls=None) -> SimpleNamespace:
    """构造一个 openai 风格的响应对象。"""
    message = SimpleNamespace(content=content, tool_calls=tool_calls)
    return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def make_agent(store: TodoStore, responses: list) -> TodoAgent:
    """构造一个按顺序返回给定响应的 agent。"""
    client = MagicMock()
    client.chat.completions.create.side_effect = responses
    return TodoAgent(store, client, model="deepseek-v4-flash")


def test_returns_text_without_tool_calls(store: TodoStore) -> None:
    resp = make_response(content="你好，有什么可以帮你？")
    agent = make_agent(store, [resp])

    result = agent.run("你好")

    assert result == "你好，有什么可以帮你？"
    assert store.list() == []


def test_executes_tool_then_returns_final_answer(store: TodoStore) -> None:
    first = make_response(
        tool_calls=[
            make_tool_call("add_todo", '{"title": "买牛奶"}', call_id="call_1")
        ]
    )
    second = make_response(content="已帮你添加待办：买牛奶")
    agent = make_agent(store, [first, second])

    result = agent.run("帮我添加买牛奶")

    assert "买牛奶" in result
    assert len(store.list()) == 1
    assert store.list()[0].title == "买牛奶"


def test_multiple_rounds_of_tool_calls(store: TodoStore) -> None:
    first = make_response(
        tool_calls=[make_tool_call("list_todos", "{}", call_id="call_1")]
    )
    second = make_response(
        tool_calls=[make_tool_call("delete_todo", '{"todo_id": 1}', call_id="call_2")]
    )
    third = make_response(content="已完成")
    agent = make_agent(store, [first, second, third])

    store.add("买牛奶")

    result = agent.run("删除我的待办")

    assert result == "已完成"
    assert store.list() == []


def test_multiple_tool_calls_in_one_response(store: TodoStore) -> None:
    first = make_response(
        tool_calls=[
            make_tool_call("add_todo", '{"title": "A"}', call_id="call_1"),
            make_tool_call("add_todo", '{"title": "B"}', call_id="call_2"),
        ]
    )
    second = make_response(content="已添加两条待办")
    agent = make_agent(store, [first, second])

    result = agent.run("添加 A 和 B")

    assert "已添加两条待办" in result
    assert [t.title for t in store.list()] == ["A", "B"]


def test_max_iterations_fallback(store: TodoStore) -> None:
    resp = make_response(
        tool_calls=[make_tool_call("list_todos", "{}", call_id="call_1")]
    )
    agent = make_agent(store, [resp] * 10)

    result = agent.run("随便")

    assert "抱歉" in result


def test_messages_include_tool_result_with_correct_id(store: TodoStore) -> None:
    first = make_response(
        tool_calls=[
            make_tool_call("add_todo", '{"title": "买牛奶"}', call_id="call_abc")
        ]
    )
    second = make_response(content="完成")
    client = MagicMock()
    client.chat.completions.create.side_effect = [first, second]
    agent = TodoAgent(store, client, model="deepseek-v4-flash")

    agent.run("添加买牛奶")

    # 第二次调用时的 messages 应包含 role=tool 且 tool_call_id 正确
    second_call_messages = client.chat.completions.create.call_args_list[1].kwargs["messages"]
    tool_messages = [
        m for m in second_call_messages
        if isinstance(m, dict) and m.get("role") == "tool"
    ]
    assert len(tool_messages) == 1
    assert tool_messages[0]["tool_call_id"] == "call_abc"
    assert "买牛奶" in tool_messages[0]["content"]
