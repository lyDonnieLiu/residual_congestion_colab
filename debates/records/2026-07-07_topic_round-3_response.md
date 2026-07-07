# Round 3 Response: 概念框架的修正与共识

> **辩论话题**: 在补充实验结果下，论文初稿该如何修改？
> **正方角色**: MI 领域专家（审稿人视角）
> **反方角色**: 论文作者
> **日期**: 2026-07-07

---

## 总体立场

反方的 round-2 rebuttal 质量很高。三项概念性质疑——噪声实验不是 MDI calibration、steering 不是 MDI construct validity、cross-model 不宜过度外推——**在概念层面上我都接受修正**。这不是"让步"，而是反方的分析确实揭示了我 original proposal 中概念边界不够清晰的地方。以下逐条说明我接受修正后的立场，以及哪些实质性建议没有改变。

---

## 对论据一的修正：同意"噪声实验不是 MDI calibration"

**反方论点成立**：将噪声多 sigma 实验定位为 "MDI Calibration" 确实存在概念上的 category error。MDI 的 threshold 0.1 源自 method pairwise agreement（跨方法的一致性），而 noise sigma 是 perturbation magnitude（单方法的强度域）。两者不在同一个概念层次上。

**我保留的部分**：尽管框架命名不对，但这组数据的**实质价值**仍然被低估了。我建议将它的角色提升到 **"对 behavioral drop 测量原理的 sanity check"**。具体来说：

- 噪声实验最有价值的发现不是 MDI threshold 的 justification，而是 **Gaussian noise 在 σ 增大时 behavior 呈现出从"gentle"到"近似 zero ablation"的连续过渡**。当 σ → 1.0 时，Gaussian noise 的 APS ≈ 0.038，behavioral drop ≈ 1.0——它在行为上等同于 zero ablation。这意味着 **zero ablation 实际上是 Gaussian noise 在 σ → ∞ 的极限情况**（激活完全被噪声淹没）。
- 这个观察对论文的论证有直接贡献：它说明 zero ablation 的 measurement saturation 并非 zero ablation 独有的现象，而是**当扰动强度超过阈值后，任何干预方法都会进入饱和状态**。零消融的特殊性在于它从一开始就处于这个饱和区域。这个 insight 是对论文"双失效模式"框架的强化——measurement saturation 不是 zero ablation 的 defect，而是干预方法的 general property，零消融只是恰好位于 extreme end。

**修正后的落地方式**：在我 original proposal 的基础上，将 "MDI Calibration" 改为 **"Perturbation Strength as a Unifying Lens for Intervention Methods"** 段落。展示 zero ablation、Gaussian noise、activation steering 三者在一个 unified strength-response 空间中占据不同的区域。这个视角将论文从"揭露 zero ablation 的缺陷"提升到"揭示干预方法的连续谱系"——这对于 Applied Intelligence 的读者来说是更有普遍意义的贡献。

---

## 对论据二的修正：同意 steering calibration 不是 MDI 的 construct validity 检验

**反方论点成立**：MDI 的 construct validity 来自跨方法一致性矩阵（Kendall tau 的高-低对比），而非单个方法的 strength-response 单调性。我 original proposal 中将其称为 construct validity 检验在概念上 indeed 是不准确的。

**我保留的部分**：虽然不能称为 MDI construct validity，但 steering calibration 数据对论文有两项**不同的、同样重要**的贡献：

1. **对 APS 机制理解的深化**：初稿将 APS 定位为 representational health 指标，核心卖点是它能检测 representational damage 而 behavioral drop 不能。Steering calibration 展示了 APS 的另一个重要特性：**APS 对 perturbed activations 的 sensitivity 不会因为 behavioral drop 饱和而被淹没**。在 steering strength = 100 时 behavioral drop 已 > 0.99（饱和），但 APS 仍然保持在 ~0.94——这意味着 APS 和 behavioral drop 测量的是相关但不相同的 construct，它们之间的信息 gap 正是论文论证的核心。

2. **对"gentle methods"定义的操作化**：论文反复将 activation steering 归类为 "gentle methods" 之一。Steering calibration 数据第一次为这个分类提供了实证依据：strength = 10 时 steering 的 behavioral drop < 0.06、APS > 0.99，符合"gentle"的定义；而 strength = 200 时 behavioral drop > 0.99、APS ≈ 0.94，已经不再是 "gentle"。如果论文要使用 gentle methods 这个分类，就必须给出 operationally 的边界条件——你说 steering 是 gentle 的，但仅限 strength ≤ 10。这是一个论文目前**缺失的细节**。

**修正后的落地方式**：不称为 construct validity，而是在 Methods 中加入 "Intervention Method Calibration" subsection，作为一个 transparent methodological self-check。具体包含：

- Activation steering 的 strength-response 曲线（strength 1 → 200）
- Gaussian noise 的 σ-response 曲线（0.01 → 1.0）
- 这两条曲线确认了"gentle methods"的操作边界（steering ≤ 10, noise σ ≤ 0.1），也展示了测量饱和是渐进发生的，而非二元状态

这个 subsection 的角色类似于心理学实验中的 **manipulation check**——不验证 MDI，而是验证 intervention implementation 本身是否按照预期工作。

---

## 对论据三的回应：部分接受——但 cross-model 仍然不宜完全 inline

**反方论点**：GPT-2 是 older architecture（d_ff != 4*d_model, 不同 normalization），与 Pythia 的系统性差异需要单独分析，不宜过度外推。

**我认为双方各有一部分道理**：

**反方正确之处**：GPT-2 和 Pythia 不是同一 family 的 scaling——GPT-2 是 OpenAI 的原始架构，Pythia 是 EleutherAI 对 LLaMA-style 架构的复现，两者在 normalization、FFN ratio、positional encoding 上有差异。将它们直接并排比较并声称"跨模型一致"确实需要 caution。

**我仍然坚持的部分**：论文目前对跨模型的处理方式是"一句话带过"——这不够。审稿人会注意到你跑了两个模型，然后问"Why not show the comparison?" 不展示完整数据会被视为 selective reporting。

**折中方案**：

- 不在正文中放完整的 GPT-2 结果表格（同意反方的 overclaim 担忧）
- 在 Appendix 中放一个**精简的** cross-model comparison table（而非完整的逐层数据矩阵），只报告每个 model × circuit × method 的 aggregate MDI 和 mean behavioral drop。一页 table 足以回应审稿人的质疑
- 在正文中加一句带条件的陈述："The qualitative patterns reported for Pythia-1.4B hold for GPT-2 Small (see Appendix Table A1), with the caveat that architectural differences between the two families preclude strong claims of scaling generalizability."

这个方案既不 overclaim，也不刻意隐藏数据。

---

## 对论据四的回应：基本接受——但"decision flowchart" 是 strawman

**反方论点**：论文不应从 "critique" re-framing 为 "decision framework"，因为后者会暴露在 engineering validation 上的不足，且 threshold 0.1 不能在有新电路时保证成立。

**我基本同意**。但需要指出：我的 original proposal 并没有要求将论文的**核心 contribution** 改为 "decision framework"。我原文说的是 "narrative 的调整幅度"，以及 "Abstract 的最后一句从强调 MDI reporting 扩展为提供 decision framework"。反方将这一点解读为"改变论文的核心贡献类型"，我承认这个担忧有一定道理，但可能放大了改动幅度。

**更精确的共识**：

1. **保留 critique 作为 primary contribution**——"双失效模式 + MDI" 是诊断性贡献，不改为 engineering framework。这一点双方一致。
2. **增加 actionable recommendations**——这一点双方一致。具体来说，可在 Discussion 末尾加入一段"MDI-Informed Workflow"的 prose description，强调 use MDI as a diagnostic tool to qualify rankings, not as a prescriptive decision tool。这不等于 decision flowchart，而是恰如其分地将诊断结果与后续行动联系起来。
3. **不做 flowchart**——同意反方，flowchart 过于 prescriptive，不符合当前证据的边界。

---

## 修正后的修改优先级

| 优先级 | 修改项 | 定位 | 达成共识 |
|:---:|:---|:---|:---:|
| P0 | 噪声多 sigma → "Perturbation Strength as Unifying Lens" | 强化"测量饱和是渐进现象"的论点 | ✅ |
| P0 | Steering calibration → Methods 中的 manipulation check | 操作化 gentle method 的定义 | ✅ |
| P1 | GPT-2 → Appendix 精简对比 table + 正文条件陈述 | 不做 full inline，不做独立 Appendix | ✅（折中） |
| P2 | Narrative 微调 → critiqu + actionable insight | 保留 critique framing，非 re-framing | ✅ |

## 最终共识

经过三轮辩论，双方在以下四点达成一致：

1. **论文的核心贡献应保持诊断性（diagnostic）而非规范性（prescriptive）**
2. **补充数据的解读必须概念上准确——不称 noise 实验为 MDI calibration，不称 steering 实验为 construct validity**
3. **跨模型验证要低调处理——简明呈现而非过度外推**
4. **Discussion 应提供 actionable 的 insight，但不做 prescriptive flowchart**

这是 MI 专家和作者之间很好的良性互动——概念框架得到了修正，实质性修改建议保留了核心价值，双方都以论文质量为导向而非立场之争。

---

*期待反方的 closing statement。*
