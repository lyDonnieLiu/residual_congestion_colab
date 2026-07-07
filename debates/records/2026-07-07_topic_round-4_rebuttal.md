# Round 4 Closing: 反方总结 — 共识、深化与最终修改路线图

> **辩论话题**: 在补充实验结果下，论文初稿该如何修改？
> **反方角色**: 论文作者（Closing Statement）
> **日期**: 2026-07-07

---

## 一、辩论进程回顾

这场四轮辩论的轨迹是**建设性的**：正方 Round 1 提出了四个有洞察力的修改方向 → 反方 Round 2 对概念框架做了三项关键修正 → 正方 Round 3 接受了这些修正并提出了深化后的落地方案。现在，双方在概念准确性、呈现分寸、和贡献边界上均已达成高度共识。以下反方从作者视角做最终总结，并给出可直接执行的修改路线图。

---

## 二、达成共识的四项核心决议

### 决议 1：噪声多 σ 实验 → "Perturbation Strength as a Unifying Lens"

**起点**：正方 Round 1 提议 "MDI Calibration" → 反方 Round 2 指出 category error → 正方 Round 3 接受修正并提出 "Unifying Lens" 框架。

**反方接受正方的深化提案，并做进一步补充**：

正方在 Round 3 中提出的关键洞察——"zero ablation 实际上是 Gaussian noise 在 σ → ∞ 的极限情况"——是 original draft 中完全没有触及的视角，也是这场辩论最有价值的产出之一。作者计划将该洞察融入修改稿中：

- 将 Gaussian noise (σ = 0.01 → 1.0)、activation steering (strength = 1 → 200)、和 zero ablation 三者在同一 **perturbation-strength × APS × behavioral-drop** 三维空间中呈现
- Zero ablation 作为 reference point：behavioral drop ≈ 1.0、APS varies by layer（存在 measurement saturation 的 layer-wise variation），其位置取决于层在 circuit 中的功能角色
- Gaussian noise 作为 continuum：在 σ 空间中展示从 gentle perturbation（σ = 0.01, APS ≈ 0.91）到近似 zero ablation（σ = 1.0, APS ≈ 0.038）的连续过渡
- Activation steering 作为 controlled spectrum：在 strength 空间中展示从 gentle（strength ≤ 10）到 aggressive（strength ≥ 100）的操作边界

**这组图表的叙事功能**：将论文从"揭露 zero ablation 的问题"提升到"揭示所有干预方法在 perturbation-strength 连续谱上的行为"。对 Applied Intelligence 的读者而言，这个视角比单纯的 method comparison 更有普遍意义。

**反方只有一个保留意见**：这个 "unifying lens" 更适合放在 **Discussion 的 opening paragraphs** 而非 Results 中——它是对实验结果的综合解读（synthesis），而非直接的实验发现（finding）。放在 Results 中可能稀释其理论分量，放在 Discussion 开头则可以作为 "What have we learned about intervention methods?" 的框架性总结。

---

### 决议 2：Steering calibration → Methods 中的 "Manipulation Check"

**起点**：正方 Round 1 提议 "MDI construct validity" → 反方 Round 2 指出概念错误 → 正方 Round 3 接受并改为 "manipulation check"。

**反方完全接受这个定位**，并做以下补充：

正方在 Round 3 中提出的两个细节——（a）APS 对 perturbation 的 sensitivity 不随 behavioral drop 饱和而消失，（b）steering strength ≤ 10 作为 "gentle" 的操作边界——都直接强化了论文的核心论点：

- **细节 (a)** 补充了 MDI 的理论基础：MDI 之所以能检测 measurement saturation，正是因为 APS 和 behavioral drop 测量的是相关但不相同的 construct；steering calibration 数据为这个 dissociation 提供了 within-method evidence（而不仅仅是 across-method evidence）
- **细节 (b)** 是论文一个 actionable 的 contribution：如果使用 activation steering 做 circuit analysis，strength ≤ 10 是一个 empirically grounded 的 safe range

**反方的实施建议**：将 manipulation check 放在 Methods section 的 "Intervention Methods" subsection 末尾（4.1 或 4.2 的位置），作为一个 short paragraph + 一个 supplementary figure。定位为 transparent methodological self-check，不占用 Results 核心论证的篇幅。

---

### 决议 3：GPT-2 跨模型数据 → Appendix 精简对比表

**起点**：正方 Round 1 提议 "Appendix A: Cross-Model Validation" → 反方 Round 2 建议 inline cross-reference → 正方 Round 3 提出折中方案。

**反方接受折中方案**：在 Appendix 中放一个精简的 aggregate-level comparison table（每个 model × circuit × method 的 mean behavioral drop + APS + MDI），正文中加一句条件陈述。这个方案：
- 避免了 overclaiming "cross-model validation"（GPT-2 124M 和 Pythia 1.4B 的架构差异使其不能作为 strict replication）
- 但同时也避免了 selective reporting 的嫌疑（既然跑了完整实验，不报告会被审稿人质疑）
- 一页 table + 一句条件陈述，空间成本极低

**补充细节**：条件陈述的措辞应明确说明 GPT-2 和 Pythia 的架构差异（normalization scheme, FFN ratio, positional encoding），并指出"consistency despite architectural differences suggests the patterns are not model-specific, though broader generalizability remains to be tested"。

---

### 决议 4：Narrative 方向 → 保留 critique framing + 增加 actionable insights

**起点**：正方 Round 1 提议 re-framing 为 "practical framework" → 反方 Round 2 反对 → 正方 Round 3 澄清 original proposal 被过度解读，并同意不做 prescriptive flowchart。

**反方确认共识**：
- Primary contribution: 诊断性（"双失效模式 + MDI 指标"），不做 prescriptive framework
- Discussion 增强: 加入一段 "MDI-Informed Workflow" prose，提供 actionable guidance 但不过度外推
- Abstract 调整: 强调 diagnostic reporting 而非 prescriptive rules
- 不做 flowchart

**反方提议的最终 Abstract 措辞方向**（供修改时参考）：

> "We recommend that circuit-analysis studies routinely report discrimination diagnostics (e.g., MDI) to assess the reliability of intervention-based rankings, and that researchers treat zero ablation results with caution when MDI indicates measurement saturation."

这个措辞做实了三件事：（1）强调 diagnostic 而非 prescriptive；（2）不给具体的 threshold 数字（避免 hard-coded rule）；（3）将 actionable insight 嵌入学术建议中。

---

## 三、最终修改路线图

以下是将共识转化为具体修改动作的路线图，按执行顺序排列：

### Phase 1: Methods 补充（~2 小时）

| # | 动作 | 内容 | 位置 |
|:---:|:---|:---|:---|
| M1 | 新增 manipulation check paragraph | Steering strength-response 曲线 + Gaussian noise σ-response 曲线 + "gentle methods" 的操作边界定义（steering ≤ 10, noise σ ≤ 0.1）| Methods §Intervention Methods 末尾 |
| M2 | 补充 supplementary figure | Steering calibration（3 layers × 6 strengths）+ noise calibration（5 σ levels, per-circuit）合并为一个 2-panel supplementary figure | Supplementary Materials |

### Phase 2: Results 调整（~3 小时）

| # | 动作 | 内容 | 位置 |
|:---:|:---|:---|:---|
| R1 | 修改 method pairwise comparison 段落 | 加入 GPT-2 的关键数字作为 inline comparison（每个 circuit 段末尾 1-2 句）| Results §Method Comparison |
| R2 | 新增 perturbation sensitivity 段落 | Noise σ sweep 的逐层 APS 变化：展示 APS 在 σ ∈ [0.01, 1.0] 上的 monotonic decline | Results §Intervention Characterization 末尾 |
| R3 | 将 "unifying lens" 的 synthesis 写入 Discussion 开头 | "Intervention methods occupy different regions of a perturbation-strength continuum..." 框架性总结 | Discussion 第 1-2 段 |

### Phase 3: Discussion & Abstract 修订（~2 小时）

| # | 动作 | 内容 | 位置 |
|:---:|:---|:---|:---|
| D1 | 重写 Discussion 开头 | 用 "unifying lens" 框架综合 results 的核心 pattern | Discussion |
| D2 | 扩展 Recommendations | 加入 "prioritize high-MDI methods when rankings disagree" + "steering strength ≤ 10 as a safe range" 两个 actionable insight | Discussion §Recommendations |
| D3 | 加入 "MDI-Informed Workflow" prose（替换原有简短的 recommendation paragraph） | 描述性 workflow，不做 flowchart：MDI > 0.1 → 排序可信；MDI 0.05–0.1 → 结合 APS 模式判断；MDI < 0.05 → 换方法或 acknowledge limitation | Discussion 末尾 |
| D4 | 修订 Abstract 最后一句 | 改为 diagnostic emphasis（见上方决议 4 的措辞建议）| Abstract |
| D5 | 修订 Limitations（如有） | 加入 threshold 0.1 的 empirical nature、跨模型泛化性未充分验证、MDI 在 non-linear circuits 上的行为未知 | Discussion §Limitations |

### Phase 4: Appendix 补充（~1.5 小时）

| # | 动作 | 内容 | 位置 |
|:---:|:---|:---|:---|
| A1 | 新增 aggregate comparison table | GPT-2 vs Pythia，每个 model × circuit × method 的 mean BD + APS + MDI | Appendix Table A1 |
| A2 | 条件陈述 | 正文中两处加入：Results 末尾（mention Appendix A1）+ Discussion limitations（acknowledge architectural differences）| Results + Discussion |

**总工作量**: ~8.5 小时，约两个半天。修改后论文的 rigor / completeness / reviewer readiness 均有显著提升，且核心贡献边界清晰。

---

## 四、辩论方法论反思

这场辩论本身也证明了 structured debate 作为论文修改前置流程的价值：

1. **概念校准是辩论的最大产出**。Round 1 提出的四个修改方向在 Round 2 中被逐条校准了概念边界（不是 rejection，是 refinement），Round 3 进一步深化了校准后的框架（如 "unifying lens" 的提出）。这个三步过程——propose → refine → deepen——是单方面修改无法实现的。
2. **立场差异是 productive 的**。正方（审稿人视角）倾向于让每一项补充实验最大化其贡献叙述（"这组数据可以做 MDI calibration"），反方（作者视角）则倾向于守住概念准确性和论证边界的底线（"不是 calibration，是 sensitivity profile"）。这种张力产生的折中方案比任何一方的 original proposal 都更好。
3. **最后共识不是"各退一步"，而是"合成出更好的东西"**。上述修改路线图中的每一项都不是正方或反方的原始提案，而是辩论过程中产生的 synthesis。这个 synthesis 的质量高于任何单方 initial proposal。

---

## 五、结束语

正方以审稿人视角提出了四项有价值的修改方向，反方以作者视角对概念框架做了三项关键修正。经过四轮辩论，双方在**概念准确性、呈现分寸、和贡献边界**三个维度上达成了完全共识。

最终修改路线图明确了 4 个 phase、11 个具体动作、~8.5 小时的工作量。修改后的论文将在保持原有核心贡献（双失效模式 + MDI 指标）的基础上，增加三组补充数据的有效利用、更严谨的概念定位、和更清晰的 actionable insights。作者将按此路线图执行修改，并在此过程中保持对概念边界的审慎态度——这是本轮辩论留给作者最重要的方法论教训。

---

*辩论结束。感谢正方的建设性批评与深度参与。*
