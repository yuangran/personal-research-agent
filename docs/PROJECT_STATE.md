# 项目当前状态

## 状态元数据

- 最后验证日期：2026-07-31
- 最近已验证基线提交：`3204e67`

## 当前里程碑

- M0 已完成，M1 正在进行
- M1 的第一个最小任务“Python 开发环境与最小项目”已通过本地验收
- M1 的重点是理解一次请求从输入到模型响应经历了什么，而不是先制作聊天界面

## 已合并并验证完成

- 已定义项目目标和第一个真实场景（证据：`README.md`）
- 已建立项目及学习文档骨架（证据：提交 `33ad431`）
- 已建立本地 Git 仓库（证据：`git log --oneline`）
- 已配置 GitHub 主仓库和 Gitee 镜像，且本地、GitHub 和 Gitee 的 `main` 已同步到 `3204e67`
- 已完成 M0 学习复盘（证据：`docs/learning/02-git-and-remotes.md`、提交 `c8b4507`）
- 已通过 [GitHub PR #1](https://github.com/yuangran/personal-research-agent/pull/1) 合并 M0
- 已通过 GitHub PR #2 和 PR #3 补充持久化项目上下文与仓库工作流约定
- 已记录“先直接调用模型，再使用 Agent 框架”的决策（证据：`docs/decisions/0001-learn-direct-model-calls-before-agent-frameworks.md`）

## M1 已验证完成

- 已选择 uv 管理项目解释器、虚拟环境和依赖，不替换本机全局 Python
- 已选择 CPython 3.13，并通过 `.python-version` 请求 3.13，通过 `requires-python = ">=3.13,<3.14"` 声明项目范围
- 已建立 `pyproject.toml`、`uv.lock` 和被 Git 忽略的 `.venv`
- 已实现最小程序，输出 `Hello from personal-research-agent`
- 已将 pytest 作为直接开发依赖，并编写一条精确断言标准输出和标准错误的测试
- 已区分 pytest 的测试收集失败与断言失败，并完成受控失败实验
- 已删除 `.venv` 后使用 `uv sync --locked` 成功重建环境，重建前后项目配置文件哈希一致
- 已完成本任务学习记录（证据：`docs/learning/03-python-environment-and-minimal-project.md`）

## 当前正在做

- 完成 M1 Python 基础任务的版本记录与远端同步
- 准备进入第一次模型调用前的 SDK、模型、Token 和费用方案选择

## 已采用的重要决策

- [ADR 0001：先学习直接模型调用，再使用 Agent 框架](decisions/0001-learn-direct-model-calls-before-agent-frameworks.md)
- M1 使用 uv 管理项目环境，项目 Python 版本选择 3.13；本机原有 Python 保持不变
- pytest 属于开发依赖，使用标准化的 `[dependency-groups].dev` 声明
- 当前扁平项目通过 `uv run python -m pytest` 运行测试，后续形成正式包结构时重新评估导入方式

## 下一步最小任务

- 选择第一次模型调用使用的官方 SDK、模型以及 Token 和费用控制方案

## 待解决问题

- 第一次模型调用使用的模型尚未选择，需要确定 Token 和费用控制方式
- 当前项目还是根目录 `main.py` 的扁平结构；进入正式包结构时需要学习 `src` 布局、构建系统和可编辑安装

## 验证证据

- 相关文件：`.python-version`、`pyproject.toml`、`uv.lock`、`main.py`、`tests/test_main.py`、`docs/learning/03-python-environment-and-minimal-project.md`
- 环境检查：`uv run python --version`、解释器路径、pytest 版本与安装位置
- 运行检查：`uv run python main.py`
- 测试检查：`uv run python -m pytest -q`，结果 `1 passed`，退出码 `0`
- 重建检查：删除 `.venv` 后执行 `uv sync --locked`，再次通过运行和测试
- 基线提交：`33ad431`、`c8b4507`、`519a148`、`3204e67`
- M0 PR：[GitHub PR #1](https://github.com/yuangran/personal-research-agent/pull/1)

## 已发现的文档偏差

- 暂无已知文档偏差
