# 学习记录：认识本地 Git 仓库

日期：2026-07-27

## 这次要解决什么

亲手把当前项目文件夹变成 Git 仓库，并理解初始化前后发生了什么。

同时开始用自己的话补全项目 README 中的目标、场景和判断标准。

## 我原来的理解

在初始化前执行 `git status` 失败时，我的判断是：

> 因为此时这个目录还不是仓库，无法使用git命令

我对几个概念的第一版回答是：

1. `pwd` 输出的是什么？

   > 当前目录的绝对路径

2. `git init` 新增了什么？能否通过 `ls -la` 观察到？

   > 新增了 .git 文件，能观察到

3. `main` 是文件夹、版本，还是分支？

   > 分支

4. `git status` 中的 `untracked files` 是什么意思？

   > 暂未提交的更改，所以未被追踪

5. 为什么 `.git` 目录不应该手动随便修改？

   > 不知道

## 我实际做了什么

先进入项目目录并观察初始化前的状态：

```bash
cd "/Users/yuangran/个人项目/personal-research-agent"
pwd
ls -la
git status
```

确认目录还不是 Git 仓库后，执行：

```bash
git init
git branch -M main
git status
```

随后再次使用 `ls -la` 和 `git status` 观察 `.git` 与未跟踪文件，并补充 README 中的项目目标和第一个真实场景。

在建立项目骨架时，我还第一次接触了 ADR，并阅读了 `docs/decisions/0001-learn-direct-model-calls-before-agent-frameworks.md`，了解项目为什么决定先直接调用模型、再手写工具循环，最后才评估 Agent 框架。

## 遇到的问题

### 1. 初始化前的 `git status` 失败

当时我把它概括成“无法使用 Git 命令”。更准确的情况是：`git status` 需要读取具体仓库状态，但当前目录及其父目录中还没有 `.git`。

不依赖具体仓库的命令，例如 `git --version` 和 `git help`，仍然可以执行。

### 2. 把 `.git` 误认为普通文件

`git init` 创建的是 `.git` 目录，不是普通文件。`ls -la` 输出中以 `d` 开头可以帮助判断它是目录。

### 3. 把 `untracked` 理解成所有未提交修改

`untracked` 只表示 Git 从未开始跟踪的路径。一个已经提交过的文件再次修改时会显示为 `modified`，不会重新变成 `untracked`。

## 现在的理解

1. `pwd` 显示当前工作目录的绝对路径，帮助确认命令会作用在哪个目录。
2. `git init` 在当前目录创建 `.git`，从而让这个普通文件夹成为 Git 仓库。
3. `main` 是分支名，不是文件夹或软件版本。
4. `.git` 保存提交对象、分支引用、暂存区状态和仓库配置。
5. 手工删除或错误修改 `.git` 中的内容，可能损坏提交历史、分支或暂存状态；现阶段应通过 Git 命令操作它。
6. `untracked`、`staged`、`committed` 和 `modified` 表示不同状态，不能都概括成“尚未提交”。

### ADR 的作用

ADR 是 Architecture Decision Record，即架构决策记录。它不是用来记录每天的项目进度，而是保存一个重要技术决策的：

1. 背景：为什么需要做决定。
2. 决策：最终选择了什么。
3. 结果：这个选择带来的优点和代价。
4. 重新评估条件：出现什么情况时需要重新考虑。

项目进度写入 `docs/PROJECT_STATE.md`，长期路线写入 `ROADMAP.md`，学习过程写入 `docs/learning/`，影响长期技术路线的选择才写入 `docs/decisions/`。

## 验证证据

- 工作目录：`pwd`
- 隐藏目录：`ls -la`
- 初始化前后状态：`git status`
- 仓库初始化：`git init`
- 默认分支：`git branch -M main`
- 观察结果：初始化后出现 `.git` 目录，`git status` 能读取仓库状态并显示未跟踪文件
- 第一条 ADR：`docs/decisions/0001-learn-direct-model-calls-before-agent-frameworks.md`

## 仍然不懂或想继续验证

- 当时还需要在下一次任务中继续区分工作区、暂存区和本地提交历史。
- 当时还没有实践第一次 `git add` 和 `git commit`。
- 后续遇到新的长期技术路线选择时，还需要继续练习判断它是否值得新增 ADR。

## 导师反馈

检查日期：2026-07-27

### 已经理解正确的部分

- 能根据 `git status` 的失败判断当前目录尚未初始化为仓库。
- 能解释 `pwd` 显示当前目录的绝对路径。
- 能识别 `main` 是分支。
- 能按照停止点只完成初始化，没有提前执行提交或推送。
- 能区分 ADR、项目状态、路线图和学习记录的基本用途。

### 需要修正或补充

1. `git init` 创建的是 `.git` 目录，不是普通文件。
2. `untracked files` 不是所有“暂未提交的更改”，而是 Git 从未开始跟踪的路径。
3. `.git` 是仓库内部数据目录，错误修改可能损坏提交、分支、暂存区或配置。
4. “当前目录还不是仓库”只会阻止依赖仓库状态的命令，不代表所有 Git 命令都无法执行。

### 本次验收

结果：通过。

已经能够完成仓库初始化并解释最基础的目录、分支和未跟踪状态。下一篇学习记录继续验证 `untracked`、`staged` 与 `committed` 的区别。
