# 辩论总结: 新实验数据下的论文修改方向

> **话题**: 论文初稿修改方案辩论
> **正方角色**: MI 领域专家（审稿人视角）
> **反方角色**: 论文作者
> **日期**: 2026-07-07
> **话题文件**: debates/topics/2026-07-07_zero-ablation-debate.md

## 辩论流程

| 轮次 | 角色 | 文件 | 核心动作 |
|:---:|:---|:---|:---|
| Round 1 | 正方开场（MI 专家） | ound-1_opening.md | 提出四项修改建议：噪声实验做 MDI calibration、steering 验证 construct validity、GPT-2 独立 Appendix、narrative 转向建设性框架 |
| Round 2 | 反方反驳（作者） | ound-2_rebuttal.md | 接受精神但提出三项概念性质疑：噪声不是 MDI calibration、steering 不是 construct validity、跨模型不宜过度外推 |
| Round 3 | 正方回应（MI 专家） | ound-3_response.md | 接受三项概念修正，但深化了"unifying lens"框架和 manipulation check 定位 |
| Round 4 | 反方总结（作者） | ound-4_rebuttal.md | 共识确认，给出 4-phase、11-action、~8.5h 的最终修改路线图 |

## 双方核心论点演变

### Round 1 → 2: 概念框架的校准（propose → refine）

| 原提案（Round 1） | 反方校准（Round 2） | 最终方案（Round 3-4） |
|:---|:---|:---|
| 噪声多 σ → "MDI Calibration" | category error：MDI 衡量 method agreement，σ 衡量 perturbation magnitude | "Perturbation Strength as a Unifying Lens"——展示干预方法在 strength-response 连续谱上的行为 |
| Steering calibration → "MDI construct validity" | construct validity 已由 pairwise 矩阵提供，steering 验证的是 steering 本身 | Methods 中的 manipulation check——操作化 "gentle method" 的边界条件 |
| GPT-2 → 独立 Appendix | 架构差异（GPT-2 ≠ Pythia）使 overclaim 风险高 | Appendix 精简对比表 + 正文条件陈述 |
| Narrative → decision framework | 改变核心贡献类型，且暴露 engineering validation 不足 | 保留 critique framing + 增强 actionable insights，不做 flowchart |

### Round 2 → 4: 共识的深化（refine → synthesize）

辩论过程中产生的、双方 initial proposal 均未包含的合成性发现：

1. **"Zero ablation = Gaussian noise in σ → ∞ limit"**（Round 3 正方提出）：测量饱和不是 zero ablation 独有的 defect，而是当扰动强度超过 threshold 后任何干预方法的 general property。这个 insight 将论文从"揭露 zero ablation 的问题"提升到"揭示干预方法的连续谱系"。

2. **"Manipulation check 的操作化价值"**（Round 3 正方提出）：Steering strength ≤ 10、noise σ ≤ 0.1 作为 "gentle method" 的 empirical boundary——这原本是论文中缺失的操作细节。

3. **"APS 不随 behavioral drop 饱和而丧失 sensitivity"**（Round 3 正方提出）：Steering calibration 数据为 APS 和 behavioral drop 测量不同 construct 提供了 within-method evidence。

## 共识与分歧

### 完全共识

| 共识项 | 说明 |
|:---|:---|
| 论文核心贡献保持诊断性（diagnostic）而非规范性（prescriptive） | 不改为 decision framework |
| 补充数据必须概念准确 | 噪声 ≠ MDI calibration，steering ≠ construct validity |
| 跨模型验证不 overclaim | Appendix 精简 + 条件陈述 |
| Discussion 提供 actionable insights，不做 flowchart | 改为 prose description of MDI-informed workflow |
| "Unifying lens" 放在 Discussion 开头而非 Results | 合成性框架，不作独立实验发现 |

### 已解决的分歧

| 原分歧 | 解决方式 |
|:---|:---|
| 噪声实验是独立 subsection 还是 paragraph | Methods 中 manipulation check paragraph + Discussion 中 unifying lens synthesis |
| GPT-2 数据 inline 还是独立 Appendix | Appendix 精简对比表 + 正文条件陈述（折中） |
| Diversity of datasets 作为 limitation | 加入 Limitations 段落 |
| 四项或五项贡献 | 维持原始四项，加入"methodological transparency"作为 cross-cutting theme |

## 最终修改路线图摘要

| Phase | 内容 | 工作量 |
|:---:|:---|:---:|
| Phase 1: Methods 补充 | manipulation check paragraph + supplementary figure | ~2h |
| Phase 2: Results 调整 | GPT-2 inline comparison + perturbation sensitivity 段落 | ~3h |
| Phase 3: Discussion & Abstract | unifying lens 合成 + recommendations + MDI-informed workflow + limitations | ~2h |
| Phase 4: Appendix 补充 | aggregate comparison table + 条件陈述 | ~1.5h |
| **总计** | **11 个具体动作** | **~8.5h** |

## 辩论方法论反思

这场辩论的产出质量高于双方任何一方的 initial proposal，关键机制是三步循环：**propose → refine → synthesize**。Round 1 的四个方向在 Round 2 中被校准概念边界，Round 3 中进一步深化为更精密的框架（如 "unifying lens"）。最终路线图中每一行都是辩论过程中产生的 synthesis——这正是 structured debate 作为论文修改前置流程的价值所在。

---

*辩论结束。双方在概念准确性、呈现分寸、和贡献边界三个维度上达成完全共识。*
