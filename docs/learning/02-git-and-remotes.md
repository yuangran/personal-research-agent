# 学习记录：本地仓库，远程仓库

日期：2026-07-27

## 这次要解决什么

连接本地仓库与 GitHub、Gitee 远程仓库，理解提交、推送、认证和上游分支，并完成 M0 的远端同步。

## 我原来的理解

1. 本地仓库和远端仓库有什么区别？

   > 本地仓库是在本地电脑上存储项目内容的仓库，远程仓库的内容是本地仓库上传后产生的，用于多人协作项目，或者公开项目作为求职履历

2. `commit` 和 `push` 分别做什么？

   > `commit` 用于将暂存区文件提交到本地仓库，`push` 用于将本地仓库的内容推送到远程仓库

3. 为什么 `main` 只跟踪 `origin/main`？

   > 因为本地分支默认只有一个上游分支，GitHub是主仓库，所以 `main` 只跟踪 `origin/main`（origin是GitHub远端的别名）

4. `noreply` 邮箱和 Token 分别解决什么问题？

   > `noreply` 邮箱隐藏了开发者的真实邮箱，保护了开发者的隐私，token用于授权GitHub通过git和本地仓库进行连接

5. 本阶段哪个概念最容易混淆？

   > GitHub CLI 连接原理

6. 如果重新操作一次，你会怎样验证同步成功？

   > 查看提交编号

当时我仍不理解：

- GitHub CLI 的连接原理还有点模糊
- 不太清楚编号 33ad431 是什么，以及如何查看编号
- 不太理解 `git status -sb` 命令

## 我实际做了什么

- 配置公开提交身份与 GitHub `noreply` 邮箱。
- 使用 GitHub CLI 登录 GitHub，并将访问凭证保存在 macOS Keychain。
- 创建 GitHub 主仓库并把它配置为 `origin`。
- 配置 Gitee 镜像远端 `gitee`。
- 将本地 `main` 设置为跟踪 `origin/main`。
- 完成本地提交、GitHub 推送、GitHub PR 和 Gitee 镜像同步。
- 使用提交哈希检查本地、GitHub 与 Gitee 的 `main` 是否指向同一个提交。
- 在 `docs/m0-retrospective` 功能分支完成 M0 学习复盘并推送到 GitHub。
- 创建 Draft PR #1，检查 base、head、提交、文件、描述、可合并性和检查结果。
- 将 PR 从 Draft 转为 Ready，对比 Merge、Squash 和 Rebase 后选择 Squash。
- 在 GitHub 合并 PR 后，获取新的 `origin/main`，快进本地 `main`，再将同一个提交推送到 Gitee。
- 比较本地、GitHub 和 Gitee 的 `main` 哈希，确认三端一致后清理功能分支。

关键检查包括：

```bash
git log --oneline
git rev-parse --short HEAD
git rev-parse HEAD
git status -sb
git remote -v
git rev-parse main origin/main gitee/main
```

## 遇到的问题

### 1. 把远端仓库理解成只能由本地上传产生

远端仓库也可以先在平台创建，再被克隆到本地；也可以先有本地历史，再创建空远端并推送。它除了协作和作品展示，也可以用于备份、发布、代码审查和 CI/CD。

### 2. 混淆 GitHub CLI、Token、Git 和 macOS 的职责

我最初写的是：

> gh auth login 相当于签发 Token 让 macOS 能够访问 GitHub，gh repo create 让 macOS 用 Token 调用 GitHub API 创建远程仓库，并规定本地仓库和对应的远端，让git能够识别连接

后来修正为：

> GitHub 给 macOS 签发了 Token（访问凭证），需要时读取便 Token 可访问 GitHub

最终需要保留的术语边界是：GitHub 授权的是 GitHub CLI 的登录会话，不是 macOS 本身。macOS Keychain 只负责安全保存 Token；GitHub CLI 使用 Token 调用 GitHub API，Git 则根据远端 URL 传输提交和更新分支引用。

### 3. 只说“查看提交编号”不足以验证同步

需要分别取得本地 `main`、GitHub `origin/main` 和 Gitee `gitee/main` 的提交哈希，并确认三者相同。提交哈希比观察网页中的文件列表更适合证明三端指向同一个提交。

### 4. 没有完整解释简短状态的两列

我最初只写了：

> `??` 代表未追踪，`A` 表示被暂存，`M` 表示被修改

后来理解到简短状态使用 `XY` 两列：第一列表示暂存区相对 `HEAD` 的变化，第二列表示工作区相对暂存区的变化。因此 `M `、` M` 和 `MM` 的含义不同。

### 5. 未跟踪文件不会出现在普通 `git diff` 中

当学习记录还是 `untracked` 时，普通的 `git diff -- <文件>` 不会显示它的内容。需要通过 `git status` 发现未跟踪文件，或先暂存后再检查暂存差异。

### 6. Squash 合并后功能分支不再是 `main` 的祖先

PR #1 的功能分支原来包含两个提交，Squash 把它们的最终内容组合成一个新的 `main` 提交。文件内容已经进入 `main`，但原来的两个提交在祖先关系上没有进入 `main`，因此普通的 `git branch -d` 可能拒绝删除。

删除前需要比较功能分支与 `main` 的最终文件内容，确认没有内容丢失；验证后才能删除本地和 GitHub 功能分支。

## 现在的理解

### 本地与远端

1. 本地仓库保存本机工作区、暂存区、提交对象和分支引用。
2. 远端仓库是独立仓库，可以先于或晚于本地仓库创建。
3. `origin` 和 `gitee` 只是本地为远端 URL 设置的别名，不是 Git 强制规定的平台名称。
4. 本项目以 GitHub `origin` 为主仓库，Gitee 是单向镜像，不在 Gitee 单独开发或合并。

### Commit、push 与上游分支

1. `commit` 根据暂存区快照在本地创建提交。
2. `push` 传输远端缺少的 Git 对象，并更新远端分支引用，不是复制整个项目文件夹。
3. 一个本地分支通常设置一个上游；本项目的 `main` 跟踪 `origin/main`。
4. `## main...origin/main` 表示当前本地分支及其上游关系；没有 ahead/behind 数字时，两者在已知状态下没有提交差异。

### 哈希与状态检查

1. `33ad431` 是提交完整哈希的短写，可以作为这次提交的标识。
2. `git log --oneline` 显示简化的提交历史。
3. `git rev-parse --short HEAD` 显示 `HEAD` 当前提交的短哈希。
4. `git rev-parse HEAD` 显示 `HEAD` 当前提交的完整哈希。
5. `git status -sb` 中 `-s` 表示 short，`-b` 表示同时显示分支信息。
6. 简短状态的第一列表示暂存区相对 `HEAD` 的变化，第二列表示工作区相对暂存区的变化。

### GitHub CLI、Token 与 Git

1. GitHub 签发 Token 作为授权凭证，GitHub CLI 的登录会话使用它访问 GitHub。
2. macOS Keychain 负责安全保存凭证，不是被 GitHub 授权的主体。
3. `gh repo create` 使用 GitHub API 创建仓库；指定本地来源和远端名称时，也可以把远端 URL 写入 `.git/config`。
4. Git 根据远端 URL 知道向哪里传输，并在 HTTPS 操作需要时使用相应凭证。
5. `noreply` 邮箱用于避免真实邮箱出现在公开提交记录中。

### Pull Request 的作用

Pull Request 是“请求把一个来源分支的改动合并到目标分支”，不是新的 Git 提交，也不会在创建后自动合并：

```text
head：功能分支（改动来源）
            ↓ 请求审查并合并
base：main（目标分支）
```

Draft 表示改动还在准备中；Ready for review 表示已经准备接受正式审查，但仍不会自动合并。`MERGEABLE` 表示 GitHub 当前判断分支可以合并，不等于代码和文档一定正确。

PR 审查至少应检查：

1. base 和 head 是否正确。
2. 标题与描述是否准确。
3. 提交和文件是否都在预期范围。
4. 是否混入密钥、私人数据或无关文件。
5. 本地测试和格式检查是否通过。
6. GitHub 的 checks、review 和 mergeable 状态。

### 三种合并方式

| 方式 | `main` 中的结果 | 特点 |
|---|---|---|
| Merge | 保留功能分支原提交，再新增一个合并提交 | 完整保留分支结构，但主分支历史较繁 |
| Squash | 把 PR 中多个提交组合成一个新的提交 | 主分支简洁，原提交过程仍可在 PR 中查看 |
| Rebase | 把功能分支提交重新应用到 `main` | 历史保持线性，但提交哈希会改变 |

M0 的 PR #1 选择 Squash，因为两个提交共同完成一项文档任务，其中一个只是审查时补充的忽略规则，没有必要让 `main` 长期保留两个细碎提交。

### 从提交到三端同步的完整流程

1. 在功能分支检查并暂存明确范围的文件。
2. 使用 `git diff --cached` 检查快照，再创建本地提交。
3. 使用 `git push -u origin <branch>` 将功能分支推送到 GitHub。
4. 创建以功能分支为 head、`main` 为 base 的 Draft PR。
5. 检查 PR 的标题、描述、提交、文件、检查结果和可合并状态。
6. 确认准备完成后，把 Draft 转为 Ready。
7. 根据任务历史需求选择 Merge、Squash 或 Rebase；M0 使用 Squash。
8. GitHub 合并后执行 `git fetch origin --prune`，只更新远端跟踪引用。
9. 切换到本地 `main`，使用 `git merge --ff-only origin/main` 安全快进，不制造额外合并提交。
10. 确认本地 `main` 与 `origin/main` 一致后，明确执行 `git push gitee main`。
11. 比较本地 `main`、`origin/main` 和 `gitee/main` 的完整哈希。
12. Squash 场景下先比较功能分支与 `main` 的文件内容，再删除 GitHub 和本地功能分支。

Gitee 只是镜像，不单独创建 PR 或合并；开发和审查都发生在 GitHub，GitHub `main` 合并成功后才把同一个提交同步到 Gitee。

## 验证证据

- 提交历史：`git log --oneline`
- 当前提交：`git rev-parse --short HEAD` 与 `git rev-parse HEAD`
- 分支和上游：`git status -sb`
- 远端别名与 URL：`git remote -v`
- 三端同步：`git rev-parse main origin/main gitee/main`
- M0 学习复盘提交：`c8b4507`
- M0 合并记录：[GitHub PR #1](https://github.com/yuangran/personal-research-agent/pull/1)
- PR #1 验证：base 为 `main`，head 为 `docs/m0-retrospective`，最终状态为 `MERGED`
- 合并方式：Squash，功能分支两个提交组合为 `c8b4507`
- 同步结果：当时本地 `HEAD`、`origin/main` 和 `gitee/main` 最终指向同一提交

## 仍然不懂或想继续验证

- 当时最容易混淆的是 GitHub CLI、Token、Git 与 macOS Keychain 的职责；经过两次复查已经能够区分。
- 后续仍需在每次 PR 和镜像同步中重复验证上游关系与三端提交哈希，避免只凭网页或文件内容判断同步成功。
- 后续需要继续根据每个 PR 的提交结构判断应该使用 Merge、Squash 还是 Rebase，而不是固定选择一种方式。

## 导师反馈

- 首次检查日期：2026-07-27
- 最终检查日期：2026-07-28

### 已经理解正确的部分

- `commit` 把暂存快照写入本地提交历史，`push` 再传输对象并更新远端分支引用。
- 一个本地分支通常设置一个上游；本项目将 GitHub 作为主仓库，因此 `main` 跟踪 `origin/main`。
- `noreply` 邮箱用于避免真实邮箱出现在公开提交记录中。
- 能把提交哈希理解为提交标识，并知道短哈希是完整哈希的缩写。
- 能解释 `git log`、`git rev-parse` 和 `git status -sb` 的基本作用。
- 能区分简短状态的暂存区列与工作区列。
- 能解释 PR 的 base/head、Draft/Ready 和可合并状态。
- 能比较 Merge、Squash、Rebase 三种方式，并说明 M0 为什么选择 Squash。
- 能描述 GitHub 合并后更新本地 `main`、同步 Gitee、验证三端哈希和清理分支的顺序。

### 需要修正或补充

1. 远端仓库不一定由本地仓库上传后产生。
2. `origin` 和 `gitee` 是可自定义的远端别名。
3. Token 是 GitHub 签发给已授权客户端使用的凭证，不是笼统地“让 macOS 访问 GitHub”。
4. GitHub CLI 负责平台 API 操作，Git 负责版本对象和分支引用的传输。
5. 只查看一个提交编号不足以验证同步，需要比较本地、GitHub 和 Gitee 分支的哈希。
6. `M` 必须结合简短状态的两列位置解释。
7. PR 可合并不代表已经完成内容审查；仍要核对文件、提交、描述和检查结果。
8. Squash 合并后不能只依赖提交祖先关系判断内容是否进入 `main`，删除分支前还要比较文件内容。

### 本次验收

结果：通过。

已经能够解释提交哈希、`HEAD`、上游分支、PR、三种合并方式和三端同步方法，并能区分 GitHub CLI 的平台操作与 Git 的版本传输职责。

保留一项术语边界：GitHub 授权的是客户端登录会话，不是 macOS 本身；Keychain 只负责安全保存 Token。
