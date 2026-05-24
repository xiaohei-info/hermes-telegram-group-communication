# Hermes Telegram Group Communication

这是一个可复用的 Hermes skill，用来规范多个 agent bot 在同一个 Telegram 群组 / topic 中进行**可见、低噪音、可审计**的沟通与协作。

这个仓库已经整理成：**仓库根目录本身就是一个可直接加载的 Hermes skill 目录**。因此标准使用方式不是先 build 一个项目，而是：

- 直接 clone 到 Hermes skills 目录
- 按本地真实环境修改少量文件
- 重启对应的 Hermes profile gateway
- 开一个新的 Hermes session
- 直接加载 skill

## 这个 skill 适合什么场景

适用于：

- 多个 agent bot 共享一个 Telegram 群组或 topic
- 希望群内协作是可见、可审计的，而不是只靠内部隐藏 handoff
- 需要明确的唤醒规则、owner 规则、handoff 规则、汇报规则
- 需要区分 native quote-reply、topic-post 和 `reply-fallback`

它主要解决这些常见问题：

- 随手写了一个 handle，结果唤醒了错误的 bot
- 真正该干活的 bot 没有被明确唤醒
- 多个 bot 同时回答，群里很吵
- 消息链路断裂，只剩同 topic 发新消息，但没有任务 lineage
- 没人知道谁是 owner，谁负责最后对上游汇报

## 前置条件

在真正使用这个 skill 之前，你的 Telegram + Hermes 环境必须先满足基础运行条件。

### 1）为需要参与协作的 agent 创建 Telegram bot

每个要参与群内协作的 agent/profile，都需要有自己的 Telegram bot，并且你需要保存好对应 token，后续配置到对应 Hermes profile 中。

### 2）开启 bot-to-bot communication 所需配置

如果你的 Telegram / gateway / 多 agent 运行环境里，bot 之间要互相“看到并响应”对方消息需要额外开启 **bot-to-bot communication** 相关配置，那么必须为这些 bot 打开。

这个 skill 默认假设：
- 多个 bot 可以出现在同一个共享群组 / topic 中
- 在平台和 gateway 配置允许的情况下，bot 可以看到别的 bot 发出的协作消息并继续链路

### 3）关闭 Telegram 的 group privacy / privacy mode

对于所有需要在群里响应 `@mention`、读取普通群消息的 bot，都要关闭 **group privacy**（privacy mode）。

这一步非常关键，因为如果 privacy mode 没关：

- bot 可能根本收不到普通群消息
- agent 之间可能“理论上在一个群里”，实际上彼此看不到
- Hermes gateway 也可能收不到群组里的 `@` 唤醒消息

也就是说，哪怕 skill 本身完全正确，如果 Telegram 没把消息交给 Hermes，这套协作协议也跑不起来。

### 4）把 bot 加入目标 Telegram 群组 / topic

确保这些 bot 真的已经加入你要协作的群组；如果你使用 Telegram topics，也要确保它们处在正确的工作空间上下文里。

### 5）把 bot 配置到对应的 Hermes profile 中

对每一个会参与 Telegram 群协作的 Hermes profile，需要完成：

- 配置正确的 Telegram bot token
- 配置该 profile 对应的 Telegram 设置
- 确保该 profile 能访问这个 skill（共享 skill 目录或直接安装到 profile 可见路径）

### 6）重启对应的 Hermes profile gateway

修改了 Telegram bot 配置、profile 配置、skill 文件之后，必须重启对应的 Hermes gateway/profile 运行态，再去测试。

原因是仅仅改文件，不代表正在运行的 gateway 已经重新加载：

- 新 token
- 新 Telegram 配置
- 新 skill 文件
- 新的 roster/routing 本地化内容

## 安装方式

### 推荐安装路径

直接 clone 到 Hermes skills 目录：

```bash
git clone https://github.com/xiaohei-info/hermes-telegram-group-communication.git \
  ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication
```

这样可行，是因为仓库根目录本身已经是标准 Hermes skill 结构：

```text
hermes-telegram-group-communication/
├── SKILL.md
├── references/
├── templates/
└── scripts/
```

## 最少需要修改哪些文件

对大多数用户来说，最少只需要改 **两个文件**。

### 1）`references/live-bot-roster.md`

把里面的占位内容换成你自己的：

- role/profile key
- bot 用户名
- 可选 bot ID
- 是否支持 topics/thread

### 2）`references/profile-capability-routing.md`

把里面的说明换成你自己的：

- 哪类任务应该由哪个角色接手
- 你的系统如何做 escalation
- 本地 role 文档在什么路径
- 你的实际能力边界如何划分

很多场景下，这两处改完就够用了。

## 标准使用流程

```bash
# 1) clone 到 Hermes skills 目录
git clone https://github.com/xiaohei-info/hermes-telegram-group-communication.git \
  ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication

# 2) 编辑本地化文件
$EDITOR ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication/references/live-bot-roster.md
$EDITOR ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication/references/profile-capability-routing.md

# 3) 重启相关 Hermes profile gateway
#    （按你自己的 Hermes 运行方式执行）

# 4) 开一个新的 Hermes session，然后加载 skill
```

在 Hermes 里加载：

```text
skill_view(name='hermes-telegram-group-communication')
```

## 可选的结构化配置方式

如果你不想手改 markdown，而是更喜欢维护一份 JSON 配置：

```bash
cp templates/skill-config.example.json templates/skill-config.local.json
```

然后填写自己的配置，再用脚本生成高本地化参考文件：

```bash
python3 scripts/render_skill.py \
  --config templates/skill-config.local.json \
  --output /tmp/hermes-telegram-group-communication-rendered
```

然后把生成出来的文件复制回你安装的 skill 目录即可。

注意：
- 这是**可选高级路径**
- 不是默认必需路径
- 默认推荐还是直接手改 `references/` 下两个文件

## 验证清单

在真实使用前，建议确认：

- Telegram bot 已经创建
- 如果你的运行环境需要 bot-to-bot communication 配置，已经开启
- Telegram group privacy / privacy mode 已关闭
- 正确的 bot token 已配置到对应 Hermes profile
- 修改配置后，相关 Hermes gateway 已重启
- `references/live-bot-roster.md` 已替换为你的真实 bot/profile 信息
- `references/profile-capability-routing.md` 已替换为你的真实角色路由信息
- 新的 Hermes session 可以加载：
  - `skill_view(name='hermes-telegram-group-communication')`
- 在真实 Telegram 群里发一个 `@mention`，目标 bot 能被正确唤醒

## 仓库结构

```text
.
├── SKILL.md
├── references/
│   ├── live-bot-roster.md
│   ├── profile-capability-routing.md
│   └── ...
├── templates/
│   └── skill-config.example.json
├── scripts/
│   ├── audit_sensitive_strings.py
│   └── render_skill.py
├── README.md
├── README.zh-CN.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

## 对你自己修改版的开源审计

如果你打算把你**自己修改过的版本**再次开源，建议先跑一次敏感信息审计：

```bash
python3 scripts/audit_sensitive_strings.py \
  --path . \
  --deny your_company_name \
  --deny your_project_codename \
  --deny your_primary_bot_handle \
  --deny /home/your-user/.hermes
```

如果你要审计已经安装到本地 skill 目录的版本：

```bash
python3 scripts/audit_sensitive_strings.py \
  --path ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication \
  --deny your_real_company_name \
  --deny your_real_bot_prefix \
  --deny /home/your-user
```

## 运行边界

这个 skill 能规范的是：

- protocol wording
- caller anchoring
- `reply-fallback`
- `[ACK]`
- owner nomination
- reporter discipline

但它**不能**强行让你的 Telegram runtime 一定保留真实的 message-level quote-reply。

如果你的 gateway / tool path 只能保证 topic continuity，而不能保证真实 reply anchor，那么这个 skill 也只能在这个现实边界上工作。

这也是为什么 skill 里会明确区分：

- `native quote-reply`
- `topic-post`
- `reply-fallback`

## FAQ

### 一定要跑 render script 吗？

不用。

默认推荐路径是：

- clone 到 Hermes skill 目录
- 改 `references/live-bot-roster.md`
- 改 `references/profile-capability-routing.md`
- 重启相关 Hermes gateway/profile
- 开一个新 session
- 加载 skill

### 一定要填 bot ID 吗？

不用，bot ID 是可选的。

### role key 能不能改成自己的？

可以，完全可以按你自己的 agent fleet 来改。

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## License

MIT
