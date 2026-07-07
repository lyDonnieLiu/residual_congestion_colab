# Round 1 Opening Statement: 新实验数据下的论文修改方向

> **辩论话题**: 在补充实验结果下，论文初稿该如何修改？
> **正方角色**: MI 领域专家（审稿人视角）
> **反方角色**: 论文作者（可质疑并反驳）
> **日期**: 2026-07-07

---

## 核心立场

论文初稿的核心论点——"zero ablation 存在两种失效模式，测量饱和（measurement saturation）是 APS 不可见且更根本的问题"——是**有洞察力且值得发表的**。但补充实验数据揭示了初稿论证中的四个关键缺口，需要在正式投稿前填补。以下逐一阐述，按影响论文核心论断的严重程度排序。

---

## 论据一：噪声强度消融实验必须融入正文，以支撑 MDI 的 empirical grounding

**问题**：初稿提出 MDI threshold < 0.1，但完全基于单组数据经验确定。审稿人会问："0.1 从哪来的？换个电路是否一样？"

**新数据**：补充实验包含了 GPT-2 Small 上 Gaussian noise 在五个 sigma 水平（0.01, 0.05, 0.1, 0.5, 1.0）的逐层结果。这是一个**自然的 MDI calibration 实验**——噪声强度由弱到强，MDI 应由低到高变化。如果画出 σ vs. MDI 的曲线，可以清晰展示 MDI 的**单调性**和**临界区间**。

**修改建议**：

- 新增一个 subsection（"MDI Calibration via Controlled Perturbation"）或一个 figure，展示 noise sigma = 0.01, 0.05, 0.1, 0.5, 1.0 时，Gaussian noise 的 MDI 在 IOI/Greater-Than/Docstring 三个电路上的变化
- 如果曲线在 σ ≈ 0.1 附近出现 inflection point（MDI 从 < 0.05 跳变到 > 0.2），这能为 threshold 0.1 提供独立的 empirical justification
- 反之，如果曲线是平滑线性变化，则说明 threshold 是纯经验性的——需要在 Limitations 中诚实说明

**核心收益**：这组实验是审稿人最可能提出的实证挑战的**现成答案**。不利用它太可惜。

---

## 论据二：Steering calibration 数据应被用来验证 MDI 的建构效度（construct validity）

**问题**：MDI 作为一个新提出的指标，论文需要证明它"测量的确实是你认为它在测量的东西"——即建构效度。初稿通过 method pairwise comparison 做了部分验证（high-MDI 方法之间高一致），但缺少直接的**操纵检验**（manipulation check）。

**新数据**：steer_calib_pythia_str*.json 记录了 activation steering 在 strength = 1, 5, 10, 50, 100, 200 上的逐层 behavioral drop 和 APS。Steering strength 增加时，MDI 应单调递增——这是一个完美的建构效度检验。

**修改建议**：

- 新增一个 figure 或 table：steering strength vs. MDI（分 circuit/层组展示）
- 预期结果：strength = 1→10 时 MDI 低（扰动太小，测不出差异），strength = 50→100 时 MDI 升高，strength = 200 时可能因过度扰动而下降（非线性效应）
- 如果这个模式成立，MDI 的建构效度得到直接支持；如果不成立（比如 MDI 单调递增到饱和），则需要讨论 MDI 的上界特性

**核心收益**：这是对"MDI 是一个有效指标"这一核心主张最强有力的支持证据。审稿人对新指标的第一个问题就是"你怎么证明它有效？"

---

## 论据三：跨模型验证不应只做"preliminary"，应结构化地呈现在 Appendix 中

**问题**：初稿声称 "Preliminary cross-model validation on GPT-2 Small confirms the same qualitative patterns"，但正文中几乎没有展示 GPT-2 的具体数据。

**新数据**：esults_gpt2-small.json（51K chars）和 nalysis_gpt2-small.json 包含了与 Pythia-1.4B 完全相同的实验矩阵——6 methods × 3 circuits × 12 layers。这是可以直接做到的。

**修改建议**：

- 在 Appendix 中新增 **Appendix A: Cross-Model Validation**，包含：
  - GPT-2 Small 的 MDI 表格（与 Pythia-1.4B 并排对比）
  - GPT-2 Small 的 method pairwise Kendall tau 矩阵
  - 关键的 qualitative 一致性陈述（如 "zero ablation MDI < 0.003 across both models"）
- 如果存在跨模型不一致之处（如 GPT-2 更浅，measurement saturation 的影响模式是否不同？），应诚实地报告

**核心收益**：跨模型泛化性是审稿人的核心关切之一。"在 1.4B 模型上发现的模式在 124M 模型上是否成立？"的回答不能只是一句话带过。你有完整数据，放 Appendix 几乎零成本。

---

## 论据四：论文的 narrative 需要从"批判"转向"构建性方法论指导"

**问题**：初稿目前的叙事基调是**揭露问题**——"Zero ablation has two failure modes, MDI reveals them"。这在学术上没问题，但对 Applied Intelligence 这类应用型期刊来说，审稿人可能会问："So what? What should I do differently tomorrow?"

**修改建议**：

初稿已有 "Recommendations for Practitioners" 小节，但可以做得更强。建议将论文的 contribution framing 从：

> "We identify two failure modes of zero ablation"

调整为：

> "We provide a practical framework for selecting intervention methods based on discrimination diagnostics"

具体改动：

1. **Abstract 的最后一句**从强调 "community should adopt routine MDI reporting" 扩展为 "we provide a concrete decision framework..."
2. **Discussion 末尾**加入一个 **decision flowchart**（文字描述即可，不一定要真正的图）：MDI > 0.1 → 方法可用于排序；MDI 0.05–0.1 → 需辅助验证；MDI < 0.05 → 换方法
3. 在 Recommendations 中增加一条：**当 zero ablation 和 mean/resample ablation 不收敛时，优先信任 high-MDI 方法的结果**——这是你数据直接支持的 actionable insight

---

## 总结：修改优先级

| 优先级 | 修改项 | 关键支持数据 | 预期工作量 |
|:---:|:---|:---|:---:|
| P0 | 噪声强度实验 → MDI calibration | 
oise_scale_gpt2_sigma*.json | 半天 |
| P0 | Steering calibration → MDI construct validity | steer_calib_pythia_str*.json | 半天 |
| P1 | GPT-2 跨模型验证 → Appendix | nalysis_gpt2-small.json | 半天 |
| P2 | Narrative 从"批判"转向"建设性框架" | 现有正文修改 | 半天 |

四个改动加起来约 1.5–2 天工作量，但对论文的 rigor、completeness、和 reviewer readiness 的提升非常显著。论文的核心贡献（双失效模式框架 + MDI 指标）是成立的，这些修改的作用是将它从"有趣的初步发现"推向"方法论层面的成熟贡献"。

---

*期待反方（作者）的回应与质疑。*
