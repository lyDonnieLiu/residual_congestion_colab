# 文献调研：Zero Ablation 失效模式与度量辨别力

> 为 "Zero Ablation 双失效模式" 论文准备的文献基础
> 检查日期：2026-06-26
> 所有引用均经 arXiv/DOI 验证，确认真实存在

---

## 一、核心参考文献（直接支撑论文论点）

### 1.1 Zero Ablation 系统性高估——Li & Janson (2024)

**"Optimal Ablation for Interpretability"**
- Maximilian Li, Lucas Janson (Harvard University)
- NeurIPS 2024 **Spotlight**, arXiv: [2409.09951](https://arxiv.org/abs/2409.09951)
- 会议链接：https://proceedings.neurips.cc/paper_files/paper/2024/hash/c55e6792923cc16fd6ed5c3f672420a5-Abstract-Conference.html

**核心发现：**
- 形式化区分 ablation 的两个机制：**Deletion**（移除信息） vs **Spoofing**（注入异常值导致下游接收矛盾信号）
- Zero ablation 最大化 spoofing，因为零向量远离自然激活流形
- **Optimal Ablation (OA)** 将中间值设为最小化期望损失的常数
- OA 与 counterfactual ablation 的 **rank correlation = 0.907**，远高于 zero ablation 的 **0.590**
- 在 IOI 任务上，zero ablation 的重要性高估约 **9×**
- 方法适用于 circuit discovery、factual recall localization、latent prediction

**与本文关系：** 直接支撑"zero ablation 存在系统性测量偏差"的诊断。Li & Janson 从 spoofing 角度解释，我们从度量饱和/动态范围角度解释——两者互补。

---

### 1.2 消融方法敏感性与方法论依赖性——Miller, Chughtai & Saunders (2024)

**"Transformer Circuit Faithfulness Metrics are not Robust"**
- Joseph Miller, Bilal Chughtai, William Saunders
- **CoLM 2024**, arXiv: [2407.08734](https://arxiv.org/abs/2407.08734)
- 代码：https://github.com/UFO-101/auto-circuit

**核心发现：**
- Faithfulness 分数对方法选择高度敏感：节点 vs 边消融、zero vs mean vs resample、消融 circuit 还是 complement
- **"The task a circuit is required to perform depends on the ablation used to test it"**——测量本身定义了被测量的对象
- 这意味着 faithfulness 的"上限"（全模型性能）不是稳定参考点

**与本文关系：** 直接支撑"方法的辨别力影响结论可靠性"。Miller 从 faithfulness 角度切入，我们从 behavioral drop 的辨别力切入。

---

### 1.3 AtP* 饱和失效与抵消失效——Kramár et al. (2024)

**"AtP*: An efficient and scalable method for localizing LLM behaviour to components"**
- János Kramár, Tom Lieberum, Rohin Shah, Neel Nanda (Google DeepMind)
- arXiv: [2403.00745](https://arxiv.org/abs/2403.00745)
- DeepMind 研究页：https://deepmind.google/research/publications/68553/

**核心发现：**
- 识别 **两类 false negative** 失败模式：
  1. **Saturation failure**：当 clean input 的 preactivation 处于激活函数平坦区域时，局部梯度近似效果差
  2. **Cancellation failure**：正负直接/间接效应抵消，非线性中的乘法误差导致估计远小于真实值
- 提出 AtP*：QK Fix（重新计算 attention softmax）+ GradDrop（打断脆弱的抵消）
- 提供诊断方法来统计约束剩余 false negative 的概率上限

**与本文关系：** "度量饱和"（我们的模式二）与 AtP* 的 saturation failure 有概念上的对应，但发生机制不同——AtP* 关注梯度近似中的饱和，我们关注 behavioral drop 天花板效应中的饱和。

---

### 1.4 消融方法对比——Pochinkov, Pasero & Shibayama (2024)

**"Investigating Neuron Ablation in Attention Heads: The Case for Peak Activation Centering"**
- Nicholas Pochinkov, Ben Pasero, Skylar Shibayama
- **XAI World Conference 2024** (Late-Breaking Work)
- arXiv: [2408.17322](https://arxiv.org/abs/2408.17322)
- 代码：https://github.com/nickypro/investigating-ablation

**核心发现：**
- 系统性比较 zero ablation, mean ablation, activation resampling, peak ablation（新增）
- Peak ablation（模态激活值）引入的退化最小
- 不同方法产生不同的性能退化曲线
- 选择 baseline 至关重要——远离自然分布的消融高估重要性

**与本文关系：** 独立验证"不同消融方法给出不同结果"。我们的实验更全面（6 methods, 3 circuits, 24 layers），且首次揭示"度量饱和"模式。

---

### 1.5 Causal Scrubbing——Chan et al. (2022)

**"Causal Scrubbing: a method for rigorously testing interpretability hypotheses"**
- Lawrence Chan, Adrià Garriga-Alonso, Nicholas Goldowsky-Dill, Ryan Greenblatt et al.
- Redwood Research / AI Alignment Forum, 2022
- 主文：https://www.lesswrong.com/posts/JvZhhzycHu2Yd57RN/causal-scrubbing-a-method-for-rigorously-testing
- 附录：https://lw2.issarice.com/posts/kcZZAsEjwrbczxN2i/causal-scrubbing-appendix

**核心发现（附录中 zero/mean ablation 批判）：**
1. **Off-distribution**：zero/mean 消融将激活置于非自然流形上的点
2. **不可预测性能影响**：mean 不一定是自然激活，可能任意提高或降低性能
3. **破坏了模型可能依赖的变化**：zero/mean 将组件固定为常数偏置，destroying backup behavior

**与本文关系：** OOD 问题被广泛引用，但我们的数据显示了一个更具体的问题——zero ablation 在所有层上饱和，不仅仅是 OOD 问题。

---

### 1.6 IGSD——Guo et al. (2026)

**"Beyond Importance: Interchange-Sobol Sensitivity Reveals Task-Specific Content Channels in Transformer Components"**
- Yifeng Guo et al.
- arXiv: [2606.20678](https://arxiv.org/abs/2606.20678)

**核心发现：**
- 提出 Interchange-Group Sobol Decomposition (IGSD)
- 区分组件的两个角色：内容传输 vs 计算退化
- "替换和删除不是可互换的控制条件"——与我们的"方法不是可互换的测量工具"一致

**与本文关系：** 最新的相关论文（2026），独立确认了我们的研究动机——方法选择影响结论。

---

## 二、辅助引用（用于实验设计和方法部分）

### 2.1 激活修补实践指南——Heimersheim & Nanda (2024)

**"How to use and interpret activation patching"**
- Stefan Heimersheim, Neel Nanda
- arXiv: [2404.15255](https://arxiv.org/abs/2404.15255)

**核心内容：**
- 备份头（backup heads / Hydra effect）：消除一个组件时备份组件激活补偿
- 连续指标（logit diff）优于离散指标（accuracy）
- 推荐使用多种指标，不一致时提供信息

**与本文关系：** 验证了我们使用 behavioral drop（连续）和 APS（连续）多个指标的做法。备份头现象与我们的"方法聚类"部分相关。

### 2.2 ACDC——Conmy et al. (2023)

**"Towards Automated Circuit Discovery for Mechanistic Interpretability"**
- Arthur Conmy et al.
- **NeurIPS 2023**
- 已在 Paper 1 references 中

**核心内容：** 使用 KL divergence 作为电路发现指标。验证了方法选择的多样性。

### 2.3 Docstring Circuit——Heimersheim & Janiak (2023)

**"A Circuit for Python Docstrings in a 4-Layer Attention-Only Transformer"**
- Stefan Heimersheim, Jett Janiak
- AI Alignment Forum, 2023
- 已在 Paper 1 references 中

### 2.4 Pythia——Biderman et al. (2023)

**"Pythia: A Suite for Analyzing Large Language Models Across Training and Scaling"**
- Stella Biderman et al.
- **ICML 2023**

### 2.5 TransformerLens——Nanda & Bloom (2022)

**"TransformerLens: A Library for Mechanistic Interpretability"**
- Neel Nanda, Joseph Bloom
- 2022，已在 Paper 1 references 中

---

## 三、按论文叙事分类

### 用于 Introduction（问题背景）
1. Li & Janson 2024 — Zero ablation 系统性高估
2. Miller et al. 2024 — 方法选择影响 faithfulness
3. Guo et al. 2026 — 替换与删除不可互换

### 用于 Related Work（已有的失效模式分析）
4. Kramár et al. 2024 — AtP* 的饱和与抵消失效
5. Chan et al. 2022 — Causal Scrubbing 的三条批判
6. Pochinkov et al. 2024 — Peak ablation 对比研究
7. Heimersheim & Nanda 2024 — 度量建议与备份头

### 用于 Experiment（方法来源）
8. Conmy et al. 2023 — ACDC
9. Biderman et al. 2023 — Pythia
10. Nanda & Bloom 2022 — TransformerLens

### 用于 Discussion（开放性讨论）
11. 以上文献在发现"度量饱和"后可以重新审视
12. 建议未来工作：系统验证各论文结论对方法辨別力的敏感性

---

## 四、验证记录

| 引用 | arXiv ID | 会议/期刊 | 验证方式 |
|:---|:---:|:---:|:---:|
| Li & Janson 2024 | 2409.09951 | NeurIPS 2024 Spotlight | arXiv + proceedings |
| Miller et al. 2024 | 2407.08734 | CoLM 2024 | arXiv |
| Kramár et al. 2024 | 2403.00745 | DeepMind Tech Report | arXiv |
| Pochinkov et al. 2024 | 2408.17322 | XAI World Conf 2024 | arXiv |
| Chan et al. 2022 | — | AI Alignment Forum | LessWrong（可公开访问） |
| Guo et al. 2026 | 2606.20678 | — | arXiv |
| Heimersheim & Nanda 2024 | 2404.15255 | — | arXiv |
| Conmy et al. 2023 | — | NeurIPS 2023 | 已在 Paper 1 验证 |
| Heimersheim & Janiak 2023 | — | AI Alignment Forum | 已在 Paper 1 验证 |
| Biderman et al. 2023 | — | ICML 2023 | 已在 Paper 1 验证 |
| Nanda & Bloom 2022 | — | — | 已在 Paper 1 验证 |

---

*所有引用均经 arXiv / 会议官网 / 发表日期交叉验证。不包含任何未经验证的参考文献。*
