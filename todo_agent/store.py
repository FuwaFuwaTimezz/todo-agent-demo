"""内存中的 Todo 存储与 CRUD 实现。"""

from .models import Todo


class TodoStore:
    """用字典 + 自增 id 在内存中保存待办事项。"""

    def __init__(self) -> None:
        self._todos: dict[int, Todo] = {}
        self._next_id: int = 1

    def add(self, title: str) -> Todo:
        """新增一条待办并返回它。"""
        todo = Todo(id=self._next_id, title=title)
        self._todos[todo.id] = todo
        self._next_id += 1
        return todo

    def list(self) -> list[Todo]:
        """按 id 升序返回所有待办。"""
        return [self._todos[tid] for tid in sorted(self._todos)]

    def get(self, todo_id: int) -> Todo | None:
        """按 id 查找，不存在返回 None。"""
        return self._todos.get(todo_id)

    def complete(self, todo_id: int) -> Todo | None:
        """将指定待办标记为完成，不存在返回 None。"""
        todo = self._todos.get(todo_id)
        if todo is None:
            return None
        todo.done = True
        return todo

    def delete(self, todo_id: int) -> bool:
        """删除指定待办，成功返回 True，不存在返回 False。"""
        if todo_id not in self._todos:
            return False
        del self._todos[todo_id]
        return True
