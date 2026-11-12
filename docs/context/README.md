# 会话恢复点

本目录存放跨会话的恢复摘要（`docs/context/`），命名 `YYYY-MM-DD-<slug>.md`，从 [../templates/context.md](../templates/context.md) 起草。

用法约定：

- 字段与全局 ai-work-config 的 `templates/context.md` 一致，以全局协议为准；
- 只记恢复任务所需长度；历史验证不代表当前状态，恢复后先用即时命令复核 revision 与工作区；
- 新会话可调用 `.claude/skills/restore-context` 自动读取最新恢复点；
- 任务完结且无后续价值时清理过期摘要，避免堆积成第二个知识库。
