# TODO — 项目开发任务清单

## 项目目标

把当前仓库逐步开发成一个 **Todo Agent Demo**，这是我学习 Coding Agent 的第一个项目。

核心学习目标：**LLM + Tool Calling + Todo CRUD**

- 掌握工具调用（Tool Calling / Function Calling）的完整闭环：定义工具 → 模型决策 → 执行 → 结果回传
- 通过自然语言驱动待办事项的增删改查（CRUD）
- 用最少的依赖搭建一个可直接上手演示的最小交互界面（CLI 或 Web）

## 当前进度

- [x] 初始化 Git 仓库，完成首次 `init` 提交
- [x] 创建 `README.md`，补充项目说明并完成 commit / push
- [x] 创建 `TODO.md`（本文件）
- [ ] 确定技术栈与依赖管理方案
- [ ] 搭建工程骨架
- [ ] 实现纯内存的 Todo 核心逻辑（CRUD）
- [ ] 将 Todo 操作封装为可供模型调用的工具
- [ ] 接入 LLM，完成「自然语言 → 工具调用」的编排
- [ ] 添加最小交互层（CLI / Web）

## 下一步任务

1. **确定技术栈**：选择 Python 或 Node/TypeScript，使用官方 SDK（如 OpenAI SDK）直接调用 LLM，不引入额外框架；建立虚拟环境和依赖清单。
2. **搭建工程骨架**：初始化项目结构、依赖管理与运行脚本。
3. **实现 Todo 核心**：先做不依赖 LLM 的纯内存待办增删改查，保证领域逻辑可独立测试。
4. **封装 Agent 工具**：把 `add_todo` / `list_todos` / `complete_todo` / `delete_todo` 定义成可被模型调用的工具。
5. **接入 LLM 编排**：让自然语言输入能自动映射到对应的工具调用。
6. **添加交互层**：命令行 REPL 或简单 Web 页面，便于现场演示。
7. **补全 README**：写清项目定位、架构与运行方式。
