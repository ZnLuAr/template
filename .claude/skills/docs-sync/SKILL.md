---
name: docs-sync
description: 改动代码或结构后，对照同步契约表检查并更新文档、登记总索引
---

# 文档同步检查

1. 读 `docs/standards/general.md` 的「文档同步契约表」。
2. 对照本次改动逐项判断需要同步的文档（layout / standards / reference / system-map / CHANGELOG / 新 ADR）。
3. 新增文档必须登记 `docs/index.md`；头部补 `> status: … · owner: … · updated: …` 行。
4. 运行验证：

   ```bash
   python scripts/check_docs.py
   ```

**Done when**：契约表每一行都有明确判定——同步了什么，或为什么不需要（有理由，不是漏判）。

报告时分两栏：已同步；判定不需要更新（附理由）。
