# Hermes Telegram Group Communication

这是一个可复用的 Hermes skill，用来规范多个 agent bot 在同一个 Telegram 群组 / topic 中进行**可见、低噪音、可审计**的沟通与协作。

这个仓库已经专门整理成：**仓库根目录本身就是一个可直接加载的 Hermes skill 目录**。

也就是说，最简单的使用方式不是 build，不是安装脚本，而是：

- 直接 clone 到 Hermes skills 目录
- 改几个本地化占位文件
- 开一个新的 Hermes session
- 直接加载使用

---

## 最简使用方式（推荐）

直接 clone 到 Hermes 的 skills 目录：

```bash
git clone https://github.com/xiaohei-info/hermes-telegram-group-communication.git   ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication
```

然后只需要重点改这两个文件：

- `references/live-bot-roster.md`
- `references/profile-capability-routing.md`

如果你想维护一份结构化配置，也可以再看：

- `templates/skill-config.example.json`

改完之后，**开启一个新的 Hermes session**，再加载：

```text
skill_view(name='hermes-telegram-group-communication')
```

---

## 为什么现在可以直接 clone 后加载

因为仓库根目录已经是标准 Hermes skill 结构：

```text
hermes-telegram-group-communication/
├── SKILL.md
├── references/
├── templates/
└── scripts/
```

所以如果你把它 clone 到：

```text
~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication
```

Hermes 就能直接把它当作 skill 目录识别。

---

## 最少需要改哪些东西

如果你希望步骤尽量少，可以忽略大部分文件，只改：

### 1）`references/live-bot-roster.md`
把里面的占位内容换成你自己的：
- role/profile key
- bot 用户名
- 可选 bot ID
- 是否支持 topics/thread

### 2）`references/profile-capability-routing.md`
把里面的路由说明改成你自己的：
- 哪类任务应该 @ 哪个角色
- 你的系统里如何做 escalation
- 本地 role 文档在什么路径

对很多使用场景来说，这两处改完就够用了。

---

## 标准使用流程

```bash
# 1) clone 到 Hermes skills 目录
git clone https://github.com/xiaohei-info/hermes-telegram-group-communication.git   ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication

# 2) 编辑本地化文件
$EDITOR ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication/references/live-bot-roster.md
$EDITOR ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication/references/profile-capability-routing.md

# 3) 开一个新的 Hermes session，然后加载 skill
```

在 Hermes 里加载：

```text
skill_view(name='hermes-telegram-group-communication')
```

---

## 如果你更喜欢用结构化配置

你也可以复制模板 JSON：

```bash
cp templates/skill-config.example.json templates/skill-config.local.json
```

然后填写自己的配置，再用脚本生成参考文件：

```bash
python3 scripts/render_skill.py   --config templates/skill-config.local.json   --output /tmp/hermes-telegram-group-communication-rendered
```

但这不是必须步骤。

**大多数人直接手改 `references/` 下面两个文件就够了。**

---

## 这个 skill 解决什么问题

当多个 agent 共用一个 Telegram 群组 / topic 时，常见问题包括：

- 随手写了一个 handle，结果唤醒了错误的 bot
- 真正该干活的 bot 没被明确唤醒
- 多个 bot 同时回答，群里变得很吵
- 消息链路断裂，只剩“同 topic 发了一条”，但没有任务 lineage
- 没人知道现在谁是 owner，谁负责最后汇报

这个 skill 统一了：

- 显式 `@mention` 唤醒
- 原生 quote-reply / topic-post / `reply-fallback` 的区别
- 可见 `[ACK]` ownership
- handoff 结构
- reporter 指定
- 群内低噪音协作纪律

---

## 仓库结构

```text
.
├── SKILL.md
├── references/
├── templates/
├── scripts/
├── README.md
├── README.zh-CN.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

---

## 开源前审计（如果你 fork 后再定制）

如果你要把你**自己改过的版本**再开源，建议先跑一遍敏感信息审计：

```bash
python3 scripts/audit_sensitive_strings.py   --path .   --deny your_company_name   --deny your_project_codename   --deny your_primary_bot_handle   --deny /home/your-user/.hermes
```

如果是审计你已经安装到本地 skills 目录里的版本：

```bash
python3 scripts/audit_sensitive_strings.py   --path ~/.hermes/skills/autonomous-ai-agents/hermes-telegram-group-communication   --deny your_real_company_name   --deny your_real_bot_prefix   --deny /home/your-user
```

---

## FAQ

### 一定要跑 render script 吗？

不用。

最简单的路径就是：
- clone 到 skill 目录
- 改 `references/live-bot-roster.md`
- 改 `references/profile-capability-routing.md`
- 开一个新 session
- 加载 skill

### 一定要填 bot ID 吗？

不用，bot ID 是可选的。

### role key 能不能改成自己的？

可以，完全可以按你自己的 agent fleet 来改。

---

## License

MIT
