# Agent Work Ledger

[英文](README.md) | 简体中文

> 让 Agent 不再黑盒工作。

**Agent Work Ledger** 是一套受 GTD 启发的轻量级 AI Agent 工作循环。它让编码 Agent 和研究 Agent 自动把开发类提示词捕获为 inbox 任务，持续维护结果定义、下一步动作、阻塞项、证据、决策和人类确认点，并把这些状态投影到 org-agenda、Web dashboard、GitHub/GitLab 评论或 Markdown 日报。

这个项目**不是**面向人类的 GTD 应用，也不是 Emacs org-mode、Todoist、Jira、GitHub Issues 或 GitLab Issues 的替代品。

它定义的是一套让 Agent 工作过程透明可审计的协议：

```text
Human prompt
        ↓
Agent Work Ledger inbox capture
        ↓
events.jsonl
        ↓
State projector
        ↓
agent-agenda.org / dashboard.html / issue comment / daily report
```

`events.jsonl` 是事实来源。其他文件都是可以重新生成的 projection。人类只旁观这些投影，GTD 文件由 Agent 自己维护。

## 为什么需要

现代 coding agent 已经可以分析、写代码、重构和 review，但它们的工作过程经常是黑盒：

- Agent 现在在做什么？
- 下一步具体动作是什么？
- 卡在哪里？
- 已经产出了什么证据或文件？
- 哪些地方需要人类确认？
- Agent 为什么停止？

Agent Work Ledger 让这些状态变得可见。

## 默认 Agent 工作循环

Agent Work Ledger 应该在开发类任务中自动启用。除了简单问答之外，Agent 遇到代码修改、调试、review、重构、文档、调研、验证、commit、PR/MR、部署或远程排查时，都应该默认接入这个工作循环。

Agent 应该自动完成：

- 把人类提示词捕获为 inbox 输入
- 判断任务类型和优先级
- 始终维护一个当前下一步动作
- 随任务推进更新 `RUNNING`、`WAITING`、`REVIEW`、`DONE` 等状态
- 为文件、命令、日志、提交、报告、链接记录证据
- 遇到高风险或需要人类判断的动作时创建确认点
- 重新生成 agenda、dashboard、report 供人类旁观

## 核心概念

每个非平凡 Agent 任务都应该维护：

| 字段 | 含义 |
|---|---|
| Outcome | 什么状态算完成 |
| State | 当前状态，例如 `RUNNING`、`WAITING` 或 `REVIEW` |
| Next Action | 下一步可执行动作 |
| Waiting For | 正在等待的人、系统、CI、API 或外部依赖 |
| Evidence | 文件、报告、提交、日志、链接或其他工作证据 |
| Human Checkpoints | 需要人类判断或批准的点 |
| Progress Log | 按时间记录的进展 |
| Decision Log | 重要决策和原因 |

## 事件类型

```text
task_created
state_changed
next_action_set
progress_logged
evidence_added
waiting_for_set
human_checkpoint
checkpoint_approved
checkpoint_rejected
checkpoint_needs_more_info
checkpoint_delegated
decision_logged
task_done
task_cancelled
```

## 状态

```text
INBOX       新目标，尚未澄清
CLARIFYING  正在理解和拆解目标
NEXT        已有明确的下一步动作
RUNNING     正在执行
WAITING     等待人类、系统或外部依赖
REVIEW      等待人类检查或批准
DONE        已完成并具备证据
CANCELLED   已取消或不再相关
```

## 最小示例

`events.jsonl`:

```jsonl
{"ts":"2026-05-11T10:00:00+09:00","task_id":"ai-governance-001","event":"task_created","title":"Draft AI coding tool risk list","source":"chat"}
{"ts":"2026-05-11T10:01:00+09:00","task_id":"ai-governance-001","event":"state_changed","from":"INBOX","to":"RUNNING"}
{"ts":"2026-05-11T10:08:00+09:00","task_id":"ai-governance-001","event":"progress_logged","message":"Identified risks: code leakage, over-broad permissions, missing audit logs, CI pollution, vendor compliance."}
{"ts":"2026-05-11T10:12:00+09:00","task_id":"ai-governance-001","event":"evidence_added","file":"reports/ai-risk-list-v0.1.md"}
{"ts":"2026-05-11T10:15:00+09:00","task_id":"ai-governance-001","event":"human_checkpoint","message":"Confirm whether external SaaS models may access repository code."}
{"ts":"2026-05-11T10:16:00+09:00","task_id":"ai-governance-001","event":"state_changed","from":"RUNNING","to":"REVIEW"}
```

生成的 `agent-agenda.org` 示例：

```org
* REVIEW [#B] Agent: Draft AI coding tool risk list :agent:ai-governance:
:PROPERTIES:
:TASK_ID: ai-governance-001
:STATUS: REVIEW
:NEXT_ACTION: Confirm whether external SaaS models may access repository code.
:EVIDENCE: file:reports/ai-risk-list-v0.1.md
:END:
```

## 仓库结构

```text
skills/                 面向 Agent 的工作协议提示
ledger/                 事件和状态 JSON Schema
scripts/                轻量级渲染器和工具
examples/               Codex、Claude Code、org-mode、GitLab/GitHub 示例
docs/                   协议、自主级别、审计和路线图文档
.agent-work-ledger/     消费项目里的运行时 ledger 文件
```

## 快速开始

在消费项目中，安装或复制项目内 skill，并忽略运行时 ledger 目录：

```text
.codex/project-skills.json
skills/agent-work-ledger/SKILL.md
.agent-work-ledger/
```

开发类任务中，Agent 应该把事件追加到：

```text
.agent-work-ledger/events.jsonl
```

然后渲染：

```bash
python scripts/render-org-agenda.py .agent-work-ledger/events.jsonl .agent-work-ledger/agent-agenda.org
```

可选 projection：

```bash
python scripts/render-dashboard.py .agent-work-ledger/events.jsonl .agent-work-ledger/dashboard.html
python scripts/render-daily-report.py .agent-work-ledger/events.jsonl .agent-work-ledger/daily-report.md
```

把生成的文件加入 Emacs org-agenda：

```elisp
(add-to-list 'org-agenda-files "/path/to/project/.agent-work-ledger/agent-agenda.org")
```

## 自主策略

Agent 可以自主执行低风险工作：

- 只读分析
- 代码扫描
- 总结
- 草稿生成
- 报告生成
- 本地进度记录

Agent 必须在以下动作前请求人类批准：

- 修改生产代码
- 创建、合并或关闭 pull request
- 发送外部消息
- 修改基础设施
- 修改权限
- 删除数据
- 发布公开内容

## 支持的 Agent

第一版优先支持 Codex 和 Claude Code。协议本身尽量保持运行时无关，因此其他 coding agent 和 research agent 也可以追加同样的事件记录。

## 状态

早期原型。第一个里程碑是最小协议、JSONL 事件日志、org-agenda 渲染器，以及 Codex / Claude Code 这类 coding agent 的示例。

## 路线图

- v0.1：协议、事件 schema、org-agenda 渲染器、coding agent 示例
- v0.2：dashboard 和日报渲染器
- v0.3：MCP server 和 Human Checkpoint API
- v0.4：多 Agent 支持和更强的审计模型
- v1.0：稳定协议和企业级 projection
