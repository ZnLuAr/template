---
name: restore-context
description: 恢复上次会话上下文：读取 docs/context/ 最新恢复摘要并复核现状
---

# 恢复会话上下文

1. 列出 `docs/context/` 下的 `YYYY-MM-DD-*.md`，取日期最新的一篇。
2. 按摘要字段恢复：目标/不做、已完成与验证、未知/阻塞、下一步入口。
3. **复核优先**：摘要只是定位线索；用即时命令核对 revision、工作区状态与关键事实，历史验证不代表当前状态。
4. 若无恢复点：说明情况，询问是否从 `docs/templates/context.md` 新建一份。
5. 恢复完成后如用户继续任务，按全局 workflow 推进；本 skill 不改变任务边界。

**Done when**：能一句话复述目标、当前状态与下一步入口，且关键事实（revision、工作区）已经过即时命令复核而非只凭摘要。
