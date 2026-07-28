# 学习记录：本地仓库，远程仓库

日期：2026-07-27

## 这次要解决什么

连接本地仓库和GitHub/Gitee远程仓库，并正常推送

## 我对知识点的理解

1. 本地仓库和远端仓库有什么区别？

    本地仓库是在本地电脑上存储项目内容的仓库，远程仓库的内容是本地仓库上传后产生的，用于多人协作项目，或者公开项目作为求职履历

2. `commit` 和 `push` 分别做什么？

    `commit` 用于将暂存区文件提交到本地仓库，`push` 用于将本地仓库的内容推送到远程仓库

3. 为什么 `main` 只跟踪 `origin/main`？

    因为本地分支默认只有一个上游分支，GitHub是主仓库，所以 `main` 只跟踪 `origin/main`（origin是GitHub远端的别名）

4. `noreply` 邮箱和 Token 分别解决什么问题？

    `noreply` 邮箱隐藏了开发者的真实邮箱，保护了开发者的隐私，token用于授权GitHub通过git和本地仓库进行连接

5. 本阶段哪个概念最容易混淆？

    GitHub CLI 连接原理

6. 如果重新操作一次，你会怎样验证同步成功？

    查看提交编号

## 仍然不懂或想继续验证

- GitHub CLI 的连接原理还有点模糊
- 不太清楚编号 33ad431 是什么，以及如何查看编号
- 不太理解 `git status -sb` 命令

## 导师反馈

检查日期：2026-07-27

### 已经理解正确的部分

- `commit` 把暂存快照写入本地提交历史，`push` 再把本地提交和分支引用发送到远端。
- 一个本地分支通常设置一个上游；本项目把 GitHub 作为主仓库，所以 `main` 跟踪 `origin/main`。
- `noreply` 邮箱用于避免真实邮箱出现在公开提交记录中。
- 当前工作确实位于 `docs/m0-retrospective` 分支，没有直接修改 `main`。

### 需要修正或补充

1. 远端仓库不一定是“本地仓库上传后产生的”。它可以先在平台独立创建，再被本地克隆；也可以像本项目一样先有本地历史，再创建空远端并推送。远端常用于协作、备份、发布、代码审查和 CI/CD。
2. `push` 更准确地说是传输本地缺少于远端的 Git 对象，并更新远端分支引用，不是简单复制整个文件夹。
3. `origin` 和 `gitee` 都只是本地为远端 URL 取的别名，不是 Git 强制规定的平台名称。它们理论上可以改成其他名字，只是 `origin` 是第一个远端的常见默认名。
4. Token 是 GitHub 签发的授权凭证。GitHub CLI 使用它调用 GitHub API，并可为 HTTPS Git 操作提供认证；真正传输提交的仍然是 Git。
5. 只“查看提交编号”不足以验证三端同步。需要分别取得本地 `HEAD`、GitHub `main` 和 Gitee `main` 的提交哈希，并确认三者相同。

### 需要亲手补充的验证

请在本文件后面新增“验证后的理解”一节，用自己的话记录：

- `33ad431` 是什么，以及短哈希和完整哈希的关系。
- `git log --oneline`、`git rev-parse --short HEAD` 和 `git rev-parse HEAD` 分别显示什么。
- `git status -sb` 中 `-s`、`-b` 各自代表什么。
- `## main...origin/main`、`??`、`A`、`M` 分别可能表示什么。
- GitHub CLI、Token、Git 和 GitHub 之间的调用关系。

另外，本文件目前还是 `untracked`。普通 `git diff -- <文件>`不会显示一个尚未被 Git 跟踪的新文件，这也是本次练习中值得记录的现象。

## 验证后的理解

gh auth login 相当于签发token让macOS能够访问GitHub，gh repo create 让macOS用token调用 GitHub API 创建远程仓库，并规定本地仓库和对应的远端，让git能够识别连接

33ad431是短哈希，是提交的“身份证”，每个提交都有自己的哈希值，短哈希是完整哈希的缩写

-s指short，-b指branch，表示由简短的形式显示当前分支和额外的远程分支的关系

`??` 代表未追踪，`A` 表示被暂存，`M` 表示被修改

### 第二次复查

已正确：

- 能把哈希理解为提交的标识，并知道短哈希是完整哈希的缩写。
- 知道 `-s` 是 short、`-b` 是 branch。
- 知道 `??`、`A`、`M` 的基本含义。

仍需修正：

1. Token 不是笼统地“让 macOS 访问 GitHub”，而是 GitHub 签发给已授权客户端的访问凭证。本项目中，GitHub CLI 将 Token 保存在 macOS Keychain，需要时读取它。
2. `gh repo create` 使用 Token 调用 GitHub API 创建仓库；使用 `--source` 和 `--remote` 时还会把远端 URL 写入本地 `.git/config`。Git 通过这个 URL 知道向哪里传输，而不是通过 Token 识别“哪个本地仓库对应哪个远端”。
3. 尚未说明 `git log --oneline`、`git rev-parse --short HEAD`、`git rev-parse HEAD` 分别显示什么。
4. 尚未说明 `## main...origin/main` 的含义。
5. Git 的简短状态是两列 `XY`：第一列表示暂存区相对 `HEAD` 的变化，第二列表示工作区相对暂存区的变化。因此 `M ` 与 ` M` 含义不同，不能只说 `M` 是“被修改”。

请在下面新增“复查修正”小节，用自己的话补齐以上五点。完成后本阶段即可进入提交检查。

## 复查修正

1. GitHub 给 macOS 签发了 token（访问凭证），需要时读取便 token 可访问 GitHub
2. `gh repo create` 在创建远程仓库时将远程仓库的 URL 写入 `.git/config`，以此让 Git 知道向哪里传输
3. `git log --oneline` 用于显示提交记录，`git rev-parse --short HEAD` 用于显示 HEAD 最近一次提交的短哈希，`git rev-parse HEAD` 用于显示 HEAD 最近一次提交的完整哈希
4. 本地 main 分支跟踪远程 origin/main 分支，且两者现在指向同一个提交
5. 第一个 X 表示暂存区相对于最近一次提交的变化，第二个 Y 表示工作区相对于暂存区的变化，例如 MM 就表示相对于最近一次提交暂存了一次修改后没有提交，又在工作区进行了一次修改没有暂存

### 最终验收

检查日期：2026-07-28

结果：通过。

- 已能解释提交哈希、`HEAD`、上游分支和三端同步的验证方法。
- 已能区分简短状态的暂存区列与工作区列。
- 已能区分 GitHub CLI 的平台操作与 Git 的版本传输职责。

保留一项术语修正：GitHub 授权的是 GitHub CLI 的登录会话，不是 macOS 本身。macOS Keychain 只负责安全保存 Token；拥有有效 Token 的客户端才能在其权限范围内访问 GitHub。
