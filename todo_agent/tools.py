"""Tool 层：把 TodoStore 的 CRUD 方法包装成可供 LLM 调用的工具。

本模块只负责两件事：
1. 定义工具 Schema（TOOLS），告诉 LLM 有哪些工具、各自收什么参数。
2. 实现工具分发（execute_tool），把 LLM 返回的工具名 + 参数映射到
   TodoStore 的方法，并把结果序列化成字符串。

本模块不依赖任何 LLM SDK，也不发起网络请求。
"""

from .store import TodoStore

TOOLS: list[dict] = [
    {
        "type": "function",
        "function": {
            "name": "add_todo",
            "description": "新增一条待办事项",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "待办内容"}
                },
                "required": ["title"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_todos",
            "description": "列出所有待办事项",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "complete_todo",
            "description": "将指定待办事项标记为完成",
            "parameters": {
                "type": "object",
                "properties": {
                    "todo_id": {"type": "integer", "description": "待办事项的 id"}
                },
                "required": ["todo_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_todo",
            "description": "删除指定待办事项",
            "parameters": {
                "type": "object",
                "properties": {
                    "todo_id": {"type": "integer", "description": "待办事项的 id"}
                },
                "required": ["todo_id"],
            },
        },
    },
]


def execute_tool(name: str, arguments: dict, store: TodoStore) -> str:
    """执行指定工具，返回序列化后的字符串结果。

    Args:
        name: 工具名，对应 TOOLS 中的 function.name。
        arguments: 已解析好的参数（dict），由调用方负责 JSON 反序列化。
        store: TodoStore 实例，工具操作的对象。

    Returns:
        自然语言字符串，用于回传给 LLM。
    """
    if name == "add_todo":
        todo = store.add(arguments["title"])
        return f"已添加待办 #{todo.id}：{todo.title}"

    if name == "list_todos":
        todos = store.list()
        if not todos:
            return "当前没有待办事项。"
        lines = [
            f"#{t.id} [{'x' if t.done else ' '}] {t.title}" for t in todos
        ]
        return "当前待办：\n" + "\n".join(lines)

    if name == "complete_todo":
        todo_id = arguments["todo_id"]
        todo = store.complete(todo_id)
        if todo is None:
            return f"未找到 id={todo_id} 的待办事项。"
        return f"已将待办 #{todo.id} 标记为完成：{todo.title}"

    if name == "delete_todo":
        todo_id = arguments["todo_id"]
        deleted = store.delete(todo_id)
        if not deleted:
            return f"未找到 id={todo_id} 的待办事项。"
        return f"已删除待办 #{todo_id}。"

    return f"未知工具：{name}"
