# 学习记录：Python 解释器、虚拟环境与最小项目

日期：2026-07-31

## 这次要解决什么

检查本机 Python 开发环境，理解 Python 解释器、虚拟环境和项目配置文件分别解决什么问题，并确定最小 Python 项目的工具方案与验收标准。

在理解和确认这些概念后，亲手建立一个能够运行、测试和重建的最小 Python 项目。

## 我原来的理解

我最初的理解是：

1. Python 解释器是读取 `.py` 文件的程序，它决定程序的语法等。
2. 虚拟环境以一个现有解释器为基础创建一个入口，这样安装的包不会污染其他环境。
3. `pyproject.toml` 是一套规则，用于规范项目的各个配置。
4. 激活虚拟环境不会改变已经安装的 Python，主要会让 `python`、`pip` 优先指向虚拟环境文件夹。
5. `pyproject.toml` 只是声明配置，不会自己产生虚拟环境。

我最初把项目版本理解成“当前项目的推进进度”，后来认识到它实际表示软件包或应用的发布版本。项目进度应由路线图和项目状态文档记录。

我也曾认为项目环境可以根据 `.env.example` 重建。后来认识到，`.env.example` 用于说明环境变量名称和示例，不负责 Python 解释器与依赖的重建。

## 我实际做了什么

### 1. 检查并选择 Python 与环境管理工具

- 确认本机是 Apple Silicon，并同时安装了多个 Python。
- 确认终端中的全局 `python3` 仍指向 Python 3.14.0。
- 使用 Homebrew 安装 uv 0.12.0，但不让 uv 改写全局默认 Python。
- 使用 uv 安装 CPython 3.13.14。
- 使用 `uv python find 3.13` 确认 uv 管理的解释器位置。
- 选择 Python 3.13 作为项目版本，并把项目允许范围声明为 `>=3.13,<3.14`。

### 2. 建立项目配置与虚拟环境

- 使用 `uv python pin 3.13` 创建 `.python-version`。
- 创建 `pyproject.toml`，声明项目名称、版本、Python 范围和依赖。
- 使用 `uv lock` 创建 `uv.lock`。
- 使用 `uv sync` 创建项目的 `.venv`。
- 确认 `.venv/bin/python3` 使用 uv 管理的 CPython 3.13.14。
- 确认项目依赖安装在 `.venv/lib/python3.13/site-packages`，且 `.venv` 被 Git 忽略。

### 3. 编写并运行最小程序

我亲手编写了 `main.py`：

```python
def main() -> None:
    print("Hello from personal-research-agent")


if __name__ == "__main__":
    main()
```

我分别验证了：

- 直接运行文件会输出 `Hello from personal-research-agent`。
- 只执行 `import main` 不会产生输出。
- 导入后显式调用 `main.main()` 会产生输出。

### 4. 添加开发依赖与自动测试

- 选择 pytest 作为测试工具，因为后续测试仍会使用它。
- 使用 `uv add --dev pytest` 将 pytest 声明为直接开发依赖。
- 理解 pytest 的 `iniconfig`、`packaging`、`pluggy` 和 `pygments` 是传递依赖。
- 理解锁文件中的 `colorama` 带有 Windows 平台条件，因此不会安装到当前 macOS 环境。
- 使用 pytest 的 `capsys` 捕获标准输出和标准错误。
- 编写测试，精确断言标准输出包含结尾换行，标准错误为空。

### 5. 进行失败实验与环境重建

- 故意把预期输出改为 `Wrong message\n`，观察到断言失败和退出码 `1`。
- 恢复正确断言后，测试通过且退出码为 `0`。
- 记录 `.python-version`、`pyproject.toml` 和 `uv.lock` 的哈希。
- 删除 `.venv`，再执行 `uv sync --locked`。
- 确认解释器、pytest、程序和测试都能恢复。
- 确认重建前后三个配置文件的哈希完全一致。

## 遇到的问题

### 1. 测试文件的第一版存在语法和调用问题

我最初写了 `import main.py`、重复调用 `capsys.readouterr()`，并把 Python 的断言写成了 `affirm`。

修正后的理解是：

- 导入模块时不写 `.py`，可以使用 `from main import main`。
- `capsys.readouterr()` 读取后会清空当前捕获内容，因此应只读取一次并保存结果。
- Python 使用 `assert` 编写断言。
- 断言必须位于测试函数内部。

### 2. pytest 收集测试时无法导入 `main`

执行下面的命令时：

```bash
uv run pytest -q
```

pytest 在收集 `tests/test_main.py` 时出现：

```text
ModuleNotFoundError: No module named 'main'
```

这属于测试收集失败，测试函数和断言都还没有执行。

当前项目尚未作为 Python 包安装，使用下面的命令后测试通过：

```bash
uv run python -m pytest -q
```

原因是 `python -m pytest` 会把当前工作目录加入 `sys.path`。命令从项目根目录执行时，Python 可以找到根目录中的 `main.py`。这不是递归搜索文件，pytest 显示的 `rootdir` 也不等于自动修改模块搜索路径。

### 3. 混淆了虚拟环境激活与 `uv run`

我曾认为项目使用 Python 3.13.14 是因为虚拟环境激活后改变了当前终端的 `PATH`。

实际实验中并没有执行 `source .venv/bin/activate`。`uv run python` 会直接使用项目的 `.venv/bin/python` 运行子命令，而不会永久改变当前终端的全局 `python3`。因此全局 `python3` 仍然是 3.14.0。

### 4. 混淆了直接依赖、间接依赖和开发依赖

我最初把“只在测试中使用的依赖”理解成间接依赖。

后来理解到这是两个不同维度：

- 项目是否主动使用：直接依赖或间接依赖。
- 依赖用于什么阶段：运行依赖或开发依赖。

如果测试代码直接使用 `freezegun`，它是直接开发依赖，应写入 `[dependency-groups].dev`；pytest 自己需要但项目不直接使用的 `pluggy` 才是间接依赖。

## 现在的理解

### Python 解释器、虚拟环境和项目配置

1. Python 解释器用于读取和运行代码，并决定支持的 Python 语法与执行行为。
2. `.venv` 是建立在基础解释器上的项目虚拟环境，提供项目自己的命令入口和依赖安装目录，与其他项目隔离。
3. `pyproject.toml` 声明项目元数据、接受的 Python 版本范围、直接运行依赖和开发依赖，但它本身不会执行安装或创建虚拟环境。

### 项目文件与 uv 的分工

1. `.python-version` 请求 uv 优先选择 Python 3.13 创建项目环境。
2. `pyproject.toml` 声明项目接受 `>=3.13,<3.14`，并记录直接依赖。
3. `uv lock` 根据项目声明解析依赖，并创建或更新 `uv.lock`。
4. `uv.lock` 是解析结果，记录精确版本、依赖关系和平台条件；它不会主动解析其他文件，也不应手工编辑。
5. `.venv` 是根据这些声明在本机创建的真实环境，不应提交到 Git。

### 常用 uv 命令

1. `uv add --dev pytest`：把 pytest 加入直接开发依赖，同时更新锁文件并同步项目环境。
2. `uv lock`：创建或更新锁文件，但不创建 `.venv`。
3. `uv sync --locked`：根据现有项目声明和锁文件创建或同步 `.venv`；如果锁文件已经过期则报错，而不是修改锁文件。
4. `uv run python ...`：使用项目虚拟环境中的 Python 运行命令，不要求先激活虚拟环境。

### 直接依赖与间接依赖

1. 项目代码直接使用的包应声明为直接依赖。
2. 正式程序直接使用的包放入 `[project].dependencies`。
3. 测试或开发工具直接使用的包放入 `[dependency-groups].dev`。
4. 直接依赖自身需要的包是间接依赖，通常不手工写入 `pyproject.toml`，由 uv 解析并记录在 `uv.lock` 中。
5. 如果项目后来开始直接导入一个原本的间接依赖，就应把它提升为直接依赖，不能依赖它被其他包“碰巧安装”。

### 测试失败的阶段

1. 测试收集失败发生在 pytest 导入测试模块或被测模块时，此时测试函数尚未执行。
2. 断言失败说明测试已经成功收集并运行，但实际值和预期值不一致。
3. 测试通过并显示退出码 `0`，才能说明这次测试命令正常完成。

## 最小项目验收标准

1. 项目使用选定的 Python 3.13，执行路径位于 `.venv/bin/python`。
2. 第三方依赖安装在 `.venv`，不污染全局环境。
3. 程序正常退出并精确输出 `Hello from personal-research-agent`。
4. 自动测试精确断言标准输出和标准错误，并以退出码 `0` 通过。
5. 删除 `.venv` 后，能够根据 `.python-version`、`pyproject.toml` 和 `uv.lock` 重建环境，并再次通过全部检查。

## 验证证据

- 解释器：`uv run python --version` 显示 Python 3.13.14，`sys.executable` 位于项目 `.venv/bin/python3`。
- 依赖：pytest 9.1.1 位于 `.venv/lib/python3.13/site-packages`。
- 程序：`uv run python main.py` 输出 `Hello from personal-research-agent`。
- 测试：`uv run python -m pytest -q` 显示 `1 passed`，退出码为 `0`。
- 失败实验：错误预期值产生 `AssertionError`，退出码为 `1`；恢复后重新通过。
- 重建：删除 `.venv` 后，`uv sync --locked` 成功重新创建环境并安装开发依赖。
- 一致性：重建前后 `.python-version`、`pyproject.toml` 和 `uv.lock` 的哈希完全一致。

## 仍然不懂或想继续验证

- 直接依赖、间接依赖、运行依赖和开发依赖的区别已经通过 pytest、pluggy 和 freezegun 的例子澄清。后续增加模型 SDK 时，继续根据项目是否直接调用其公共接口来验证依赖分类。
- 当前项目使用根目录中的 `main.py`，因此测试命令采用 `python -m pytest`。项目开始形成正式包结构时，需要继续学习 `src` 布局、构建系统和可编辑安装之间的关系。

## 导师反馈

检查日期：2026-07-31

### 已经理解正确的部分

- 能区分解释器负责执行代码、虚拟环境负责隔离项目依赖、项目配置负责声明需求。
- 能解释全局 Python 3.14.0 与项目 Python 3.13.14 可以同时存在，并知道 `uv run` 不等于激活虚拟环境。
- 能说明 `.python-version`、`pyproject.toml`、`uv.lock` 和 `.venv` 的不同职责。
- 能区分直接依赖与间接依赖，也能把运行或开发用途作为另一个分类维度。
- 能区分 pytest 的收集失败与断言失败，并通过受控实验验证退出码。
- 能删除并重建 `.venv`，用解释器路径、依赖位置、程序输出、测试结果和文件哈希证明环境可复现。

### 需要继续保持的边界

1. `pyproject.toml` 和 `uv.lock` 是声明与解析结果，不是虚拟环境本身。
2. `uv.lock` 不会主动执行依赖解析；执行解析的是 uv 命令。
3. 虚拟环境激活只是临时调整当前终端命令查找顺序，使用 `uv run` 时不必先激活。
4. 不要因为某个间接依赖已经出现在 `.venv` 中，就在项目代码里直接使用它；如果项目直接使用，应明确声明。
5. 当前用 `python -m pytest` 解决的是未安装的扁平项目导入问题。后续采用正式包结构时应重新评估测试和导入方式，而不是长期依赖临时的路径修改。

### 本次验收

知识点验收结果：通过。

已经能够解释核心概念、亲手完成最小实现、通过测试和重建实验提供证据，并对收集失败和断言失败进行区分与排查。本次知识点验收时改动尚未提交，随后仍需更新项目状态文档并完成提交前检查。

## 参考资料

- [Python 官方文档：`venv`](https://docs.python.org/3/library/venv.html)
- [Python Packaging User Guide：`pyproject.toml` 规范](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
- [uv 官方文档：项目结构与文件](https://docs.astral.sh/uv/concepts/projects/layout/)
- [uv 官方文档：锁定与同步](https://docs.astral.sh/uv/concepts/projects/sync/)
- [pytest 官方文档：调用 pytest](https://docs.pytest.org/en/stable/how-to/usage.html)
