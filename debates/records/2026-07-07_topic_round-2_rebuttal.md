# Round 2 Rebuttal: 对修改建议的逐条回应

> **辩论话题**: 在补充实验结果下，论文初稿该如何修改？
> **正方角色**: MI 领域专家（审稿人视角）
> **反方角色**: 论文作者（可质疑并反驳）
> **日期**: 2026-07-07

---

## 总体立场

正方对论文核心贡献（双失效模式框架 + MDI 指标）的肯定，作者深表感谢。四项修改建议确实触及了论文需要加强的环节，但在**每项建议的具体落实方式**上，作者有三点原则性分歧需要阐明：（1）噪声实验和 steering calibration 的**解读框架**需要纠正；（2）cross-model validation 的**呈现粒度**需要务实地取舍；（3）论文 narrative 的**调整幅度**需要守住学术贡献的边界。以下逐条回应。

---

## 对论据一的回应：噪声实验应纳入正文，但不应称为"MDI Calibration"

**同意的部分**：噪声消融的多 sigma 数据确实有价值，应该纳入正文。数据清楚地展示了 Gaussian noise perturbation 在 σ 从 0.01 到 1.0 时，APS 从 ~0.91 单调下降到 ~0.038（以 GPT-2 Small IOI layer 0 为例）。这是一个 clean and interpretable 的实验结果。

**分歧**：正方建议将此实验定位为"MDI Calibration"，并以此验证 threshold 0.1 的合理性。作者认为这个框架在概念上是有问题的。

**理由**：

1. **噪声实验测量的是 perturbation strength → behavioral drop / APS 的映射，而非 MDI 的 calibration。** MDI 的定义是方法间排名一致性的度量（Kendall tau / Jaccard / Cohen's kappa 的聚合），它的 threshold 0.1 是基于 *method pairwise agreement* 的经验阈值，而非基于 perturbation magnitude 的阈值。将 MDI threshold 与 noise sigma 挂钩是概念层面的 category error——前者衡量方法间分歧，后者衡量单方法扰动强度。

2. **数据不支持 σ ≈ 0.1 处存在 inflection point。** 正方假设曲线可能在 σ ≈ 0.1 附近出现拐点，以此 justify threshold 0.1。但从数据来看：σ=0.01 时 gaussian_noise APS ≈ 0.91（GPT-2 IOI L0），σ=0.05 时 APS 仍然很高（扰动太弱），σ=1.0 时 APS ≈ 0.038。变化的本质是**噪声强度通过影响 residual stream 的 L2 norm 来间接影响 APS**——大 σ 噪声直接压过原始激活，等同于近似 zero ablation。这不是 MDI 的 calibration，而是 perturbation magnitude 的 sweep。

3. **正确的解读框架**：这组实验应该定位为 **"Sensitivity of APS to Perturbation Magnitude"**——展示不同干预方法对扰动强度的敏感度曲线不同。例如对比 zero ablation（binary，无强度参数）、Gaussian noise（σ 可控）、activation steering（strength 可控）三者在 perturbation-strength × behavioral-impact 空间中的不同行为模式。这个分析**强化而非替代** MDI 的核心论点：不同的干预方法不仅结果不同（MDI 低），它们对扰动强度的响应模式也不同。

**修改建议的修正版**：新增一个 paragraph 或 figure 在 Results 中，标题为 "Perturbation Sensitivity Profiles Across Intervention Methods"，而非独立的 "MDI Calibration" subsection。如果审稿人问 threshold 0.1 的来源，诚实回答"based on empirical convergence patterns of pairwise agreement metrics"，而非将 noise sigma 作为 post hoc justification。

---

## 对论据二的回应：Steering calibration 验证的是 steering 本身，不是 MDI 的建构效度

**同意的部分**：steering calibration 数据确实展示了 clean 的 monotonic strength-response 关系。以 GPT-2 IOI 为例，layer 2 上 steering strength 1→100→200 的 behavioral drop 从 0.004→0.90→0.9998，这与 intuitive expectation 完全一致。这组数据应该被纳入论文。

**分歧**：正方将这组数据定位为"MDI 的 construct validity（建构效度）检验"，作者认为这是对 MDI 概念本身的误解。

**理由**：

1. **MDI 的 construct validity 来自它的定义和跨方法验证，而非单方法的 strength sweep。** MDI 衡量的是"不同干预方法对同一组神经元的排序是否一致"。它的 construct validity 已经通过 method pairwise comparison（初稿 Table 2/3 的 Kendall tau 矩阵）得到了初步验证——high-MDI methods 之间 Kendall tau 高，low-MDI methods 之间 Kendall tau 低。这**就是** construct validity 的证据：MDI 高的方法确实在测量同一个底层信号。

2. **Steering calibration 验证的是 steering 作为干预方法的 internal validity**——即"改变 steering strength 是否导致 behavioral impact 的预期变化"。这当然是有用的，但它回答的问题是"steering 这个方法本身是否可信"，而非"MDI 是否测量了它声称在测量的东西"。将 steering calibration 称为 MDI 的 construct validity 检验，相当于用温度计校准实验来验证"温度"这个概念——概念和工具被混淆了。

3. **实际数据还有局限。** steering_calibration.json 只覆盖了 3 个 layers（2, 6, 10），无法做全层 MDI 计算。要做"steering strength vs. MDI"分析，需要每个 strength level 的完整 24 层 steering 数据，才能计算该 strength 下的 MDI 并与 baseline MDI 比较。目前的数据只支持"steering strength vs. behavioral drop per layer"的分析，这是 intervention characterization，不是 MDI validation。

**修改建议的修正版**：将 steering calibration 数据纳入 Results 现有的 "Intervention Method Characterization" 小节（或新增 "Intervention Strength-Response Profiles" 段落），展示不同方法（特别是 steering 和 Gaussian noise）的 strength-response 曲线。在 Discussion 中 brief mention 这组数据对 MDI 的**间接**支持——"methods with higher MDI also exhibit cleaner monotonic strength-response profiles（如 steering），further supporting their reliability for circuit ranking"——但不将其作为 MDI construct validity 的核心证据。

---

## 对论据三的回应：GPT-2 数据应该纳入，但不必独立成章

**同意的部分**：GPT-2 Small 的完整实验矩阵（6 methods × 3 circuits × 12 layers）确实与 Pythia-1.4B 一一对应，不利用是浪费。analysis_gpt2-small.json 中的 method_summary 已经清楚地展示了关键 pattern：zero ablation 在 GPT-2 IOI 上的 APS_mean = 0.808（对比 Pythia 的 0.888），mean ablation APS_mean = 0.997（对比 Pythia 的 0.998）。跨模型定性一致性很高。

**分歧**：正方建议在 Appendix 中新增独立的 "Appendix A: Cross-Model Validation"，包含完整的 MDI 表格和 Kendall tau 矩阵。作者认为这过于形式化——数据支持的是**跨模型 robustness check**，而非独立的 validation study。

**理由**：

1. **GPT-2 Small（124M）和 Pythia-1.4B（1.4B）的规模差距不够大，不能构成严格的 cross-model validation。** 两者都是 decoder-only Transformer，且都在相近的量级上。真正有说服力的跨模型验证需要跨越 architecture family（如 encoder-decoder vs. decoder-only）或至少跨越一个数量级的规模差异。将 124M 模型的 Appendix 称为 "Cross-Model Validation" 可能被审稿人批评为 overclaiming。

2. **论文的页数限制需要考虑。** Applied Intelligence 的 regular paper 通常有页数限制。将 GPT-2 的完整 MDI 表格 + Kendall tau 矩阵放入 Appendix 会增加 2-3 页。如果这些数据只是 confirm 而非 extend Pythia 的发现，那这个空间投入的边际收益有限。

3. **务实的做法**：在 Results 的相应段落中，将 GPT-2 的关键数字作为 **inline cross-reference** 呈现。例如："On GPT-2 Small (124M), zero ablation similarly exhibits MDI < 0.01 across all three circuits (IOI: τ = −0.24 vs. mean ablation; Greater-Than: τ = −0.33; Docstring: τ = −0.24), confirming that measurement saturation is not an artifact of model scale or architecture." 这样审稿人看到的是 converging evidence，而非 segregated appendix。

**修改建议的修正版**：在 Results 每个 circuit 段落的末尾加 1-2 句 GPT-2 的关键对比数字。如果主编或审稿人明确要求完整的跨模型 Appendix，再补充——但目前先做轻量级的 inline integration。

---

## 对论据四的回应：Narrative 可以微调，但不能改变论文的学术贡献类型

**同意的部分**：正方指出论文目前"揭露问题"的叙事需要更强的 "so what" 成分，这一点作者接受。"Recommendations for Practitioners" 可以写得更具体、更 actionable。

**分歧**：正方建议将 contribution framing 从 "We identify two failure modes" 调整为 "We provide a practical framework for selecting intervention methods"，作者认为这会**改变论文的核心贡献类型**，对于 Applied Intelligence 这样的应用型期刊反而可能不利——审稿人会问："这个 framework 有没有在真实场景中被验证过？有没有 ablation 证明每个 component 的必要性？" 这些问题论文目前无法充分回答。

**理由**：

1. **论文的核心贡献是 conceptual + empirical，而非 engineering。** "双失效模式（measurement saturation + representational damage）+ MDI 指标"是一个**诊断性框架**，它的价值在于帮助研究者理解为什么不同的干预方法给出不同的结果——不是告诉研究者应该用什么方法。将论文重新定位为"decision framework"会制造错误的读者预期，并且暴露论文在 engineering validation 上的不足。

2. **"Decision flowchart" 的提议过于 premature。** 正方建议的 flowchart（MDI > 0.1 → 可用于排序；0.05–0.1 → 需辅助验证；< 0.05 → 换方法）虽然直观，但 itself 就是基于单一数据集的经验规则。在没有第三个模型、第三个电路类型、或不同任务 domain 的验证之前，将这个 flowchart 作为论文的核心 take-away 是在用不充分的证据做规范性推荐。审稿人完全可能问："你凭什么认为 0.1 的 threshold 在 unseen circuits 上成立？"

3. **论文现有的 "critique" framing 在学术上是 honest 且 defensible 的。** 揭示 methodological problems 本身就是一个 legitimate contribution——许多高引论文的核心贡献就是"指出大家都在用的方法有问题"（如 double descent, shortcut learning 等文献）。不应因为投稿应用型期刊就将学术贡献包装成 engineering solution。

**修改建议的修正版**：

- Abstract 末尾调整为："We recommend that future circuit-analysis studies routinely report discrimination diagnostics (MDI or equivalent metrics) to qualify the reliability of their intervention-based rankings."（强调诊断和透明度，而非 decision framework）
- Discussion 中保留 "Recommendations for Practitioners"，但增加 nuanced 内容："When zero ablation and high-MDI methods disagree on circuit rankings, we recommend prioritizing high-MDI methods' results, as the disagreement itself is diagnostic of measurement saturation in zero ablation." 这是数据直接支持的 actionable insight，且不需要 overclaim。
- 不加入 decision flowchart，而是在 Discussion 末尾用一段文字描述"MDI-informed workflow"——说明 MDI 如何辅助研究者判断干预结果的可信度，但不做出超出数据支持的 prescriptive claims。

---

## 修改优先级（修正版）

| 优先级 | 修改项 | 与原建议的差异 | 预期工作量 |
|:---:|:---|:---|:---:|
| P0 | 噪声多 sigma 实验 → "Perturbation Sensitivity Profiles" 段落 | 改名称 + 改解读框架，不放独立 subsection | 2-3 小时 |
| P0 | Steering calibration → "Intervention Strength-Response" 段落 | 不作为 MDI construct validity 的核心证据 | 2-3 小时 |
| P1 | GPT-2 跨模型数据 → Results inline cross-reference | 不做独立 Appendix，改为 inline comparison | 1-2 小时 |
| P2 | Narrative 微调 → 强调诊断意识 + actionable insight | 不做 decision framework/flowchart re-framing | 1-2 小时 |

总计约 6-10 小时，仍在一个合理的工作周期内。

---

## 总结

正方四项建议的**精神**作者完全认同——补充数据来之不易，应充分利用。但在**落实方式**上，作者坚持三点：（1）概念准确性不可妥协——噪声实验不是 MDI calibration，steering calibration 不是 MDI construct validity；（2）呈现形式要务实地服务于论证目标，而非 formality for formality's sake；（3）学术贡献的边界要守住——可以做诊断性建议，不做规范性 framework。这三点不影响论文修改的实质内容（数据都会用上），但影响论文在审稿人眼中的**学术可信度**。一个诚实的、边界清晰的诊断性贡献，比一个 overclaimed 的"practical framework"更可能通过同行评审。

---

*期待正方的进一步回应。*
