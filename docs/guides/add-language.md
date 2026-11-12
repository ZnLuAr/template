# 指南：新增一种语言脚手架

> status: stable · owner: ZnLuAr · updated: 2026-11-12

按清单执行，全部完成前不算加完：

1. **建目录** `scaffold/<lang>/`，分层变体落地遵守 ADR-0002：`variants/cls/`（entry/logic/model/infra）与 `variants/hex/`（entry/service/domain/infra）两套都要，按该语言惯例映射目录名；
2. **工具链配置**（放语言根，两变体共享）：构建 + 测试 + lint/format 三件套的最小可用配置（零第三方运行时依赖优先，Greeter 示例用标准库实现）；
3. **同构示例**：两变体各移植 Greeter 示例（规则层纯策略 + Clock、业务层编排、infra 实现、entry 组装），与其他语言同变体者同构（都注入 + fake）；
4. **测试镜像**：unit 覆盖规则与业务层（cls：model/logic；hex：domain/service，均含 fake Clock），integration 覆盖 entry；
5. **语言规则段**：`scaffold/<lang>/variants/<arch>/CLAUDE.md` 各写薄段（布局、常用命令、该变体铁律、指向 standards），实例化时由 init.py 按所选变体合并进项目根 CLAUDE.md；
6. **规范**：`docs/standards/<lang>.md`（布局按变体区分、命令、命名、禁忌）；
7. **生成器**：`scripts/init.py` 的 `LANGS` 与 `LANG_STANDARD` 映射登记新语言；
8. **冒烟**：`scripts/tests/test_init.py` 加用例（两变体各实例化 → 关键文件存在 → 无占位符残留 → check_docs 通过）；
9. **登记**：本文件不改；更新 `docs/index.md`（standards 列表）、模板根 `README.md` 支持语言列表、`CHANGELOG.md`；
10. **验证**：`python scripts/check_docs.py` + `python -m unittest discover -s scripts/tests` 全绿。

若新语言的惯例与变体语义有实质冲突（无法同构），先写 ADR 说明偏差，再动工。
