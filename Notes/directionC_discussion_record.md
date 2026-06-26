# 方向C系列：与反方的讨论全过程记录

> 日期：2026-06-25
> 参与者：用户（正方）、反方（资深MI领域专家）、Claude（记录）
> 主题：Paper 1 之后的下一篇论文方向

---

## 背景

Paper 1 (Beyond Ablation) 已完成投稿准备。核心发现：6种干预方法在3个电路上的排序高度不一致（mean Kendall tau = -0.10）。Paper 1 提出了 APS（Activation Preservation Score）作为表征健康度量来辅助仲裁。

Open question：既然方法结论不同且 APS 有变化，那么——谁是正确的？

---

## 第一轮：反方对"三角验证"方案的批评

### 反方论点

"谁是正确的"这个问题本身有问题——它隐含了存在 ground truth 的假设。但在真实模型中不存在 ground truth。重要性是 intervention-dependent 的。

**核心批评**：
- Zero ablation 问"去掉这个组件还能工作吗"（必要性问题）
- Mean ablation 问"替换为平均值还能工作吗"（稳健性问题）
- Activation steering 问"在这个方向上扰动行为变化多大"（连续性问题）
- 这三个问题不同，答案不同是正常的。APS 解决不了这个。

### 反方建议（第一版）

在合成电路（synthetic transformers with known circuits）上做方法校准——在已知 ground truth 的设置下，看哪个方法恢复了正确的电路结构。

### 正方回应

操作复杂度被低估了。Elhage 2022 的框架是数学描述不是可运行代码。要在 Pythia 规模的模型上嵌入已知电路结构，工程工作量相当于半年以上的项目。

---

## 第二轮：正方提出"Impossibility of Ground Truth"方案

### 正方建议

论文标题："The Impossibility of Ground Truth: Why Disagreeing Intervention Methods Are All Correct"

核心论点：每种方法回答不同因果问题，没有仲裁。揭露一个被社区忽视的方法论事实。

### 反方评估

- 论点太哲学，审稿人会问"so what? 那我们怎么做实验？"
- 论文必须给出可操作的指导，不能只破不立

---

## 第三轮：反方提出"APS 加权修正"方案

### 反方方案

Observation → Diagnosis → Correction → Validation 四步结构：
1. 量化 zero ablation 的测量偏差
2. 基于 APS 构建校正项
3. 验证修正后的排序与 gentle methods 收敛
4. 在 hold-out 设置下验证排序预测力

### 正方回应

反方的前提是 gentle methods 更正确——但证据是什么？APS 高不代表更可信，只是代表破坏得少。

**正方的最终评价**：这个方向比之前所有方案都好，但需要加一个独立可验证的步骤（hold-out validation）。

---

## 第四轮：正方提出 Option A vs Option B

### 方案分析

Option A（冒险）：直接做完整四步，如果修正验证通过投 TMLR

Option B（稳健）：只做 Observation + Diagnosis 两步，投 TMLR Replication

### 正方倾向

Option B 风险更低，但可能 novelty 不够。

### 反方反驳

Option B 的核心发现已经在 Paper 1 里了。而且没有 Correction 环节，无法区分"不同问题"和"测量偏差"。

---

## 第五轮：反方提出 Option C（多结局设计）

### 方案

预设四种可能的结论，每一种都能成文：
- 结局 1：修正有效 → TMLR 长文
- 结局 2：部分有效 → TMLR 短文
- 结局 3：完全无效 → 负结果论文
- 结局 4：APS 本身更能预测 → APS 方法论论文

### 正方反问

基于已有数据，最可能的结局是哪个？需要先看数据再决定论文结构。

---

## 第六轮（转折）：反方检查数据发现核心错误

### 数据检查结果

反方实际查看了 `all_results.json` 的每层数据，发现了关键的"度量饱和"模式。

**核心发现**：

| 电路 | Zero unique drop 值 | Gentle 方法动态范围 |
|:---|:---:|:---:|
| IOI | 3/24 | 0.0–0.97 |
| GT | 2/24 | 0.0–0.99 |
| Docstring | 18/24 | 0.0–0.96 |

**关键证据 -- IOI L11**：
- zero_aps = 0.996（极高）
- zero_behavioral_drop = 1.0（完全饱和）
- mean_behavioral_drop = 0.826（circuit 开始的地方）

这意味着 zero ablation 在 IOI 和 GT 上根本没有排名能力——这不是"问不同问题"，而是"退化为一个无辨别力的度量"。

### 诊断

Zero ablation 有两个不同的失败模式：
1. **模式一：表征损伤**（L0-L4，APS 可见）
2. **模式二：度量饱和**（L5-L23，APS 不可见）

这两个模式共同决定了基于 APS 的修正方案在原则上不可行。

---

## 第七轮：最终方案定型

### 论文结构

1. **Observation** — 发现 zero ablation 的两个不同失效模式
2. **Diagnosis** — 为什么 APS 不能修正（L11 证据）
3. **MDT (Measurement Discrimination Test)** — 工具输出
4. **Impact Demonstration** — 展示 MDT 低的方法如何误导结论

### 时间线

- 第 1-2 天：运行分析，生成图表
- 第 3-7 天：写初稿
- 第 8-10 天：修改定稿
- 第 11-14 天：arXiv + TMLR

### 目标

- arXiv（第 2 周发布建优先级）
- TMLR 短文（后续提交）

### 不做的事项

- 不做合成电路实验
- 不做跨模型新 GPU 实验
- 不做 LOOCV（n=3 统计力不足）
- 不做文献的全面 MDT 回顾（数据不可得）

---

## 关键决策记录

| 序号 | 决策 | 理由 | 做出者 |
|:---|:---|:---|:---:|
| 1 | 不追求"谁是正确"的仲裁 | 不存在 ground truth | 双方同意 |
| 2 | 不建设合成电路 | 工程量过大 | 正方提出，反方撤回 |
| 3 | 不做 LOOCV | n=3 统计力不足 | 正方提出，反方同意 |
| 4 | 不将修正方案作为论文核心 | 数据证明其基础假设失效 | 反方数据发现 |
| 5 | 转向诊断+MDT 方向 | 数据驱动的方向转变 | 双方同意 |
| 6 | MDT 替代 DRC | DRC 是巧合，MDT 是标准必要 | 反方提议，正方同意 |
| 7 | 2 周出 arXiv | 建优先级 | 双方同意 |

---

## 参与方角色说明

- **正方（用户）**：论文实际作者，研究方向为 MI 可解释性。提出原始问题和实验方案，对反方建议做实践可行性评估，最终控制决策。
- **反方（资深 MI 领域专家）**：扮演 adversarial reviewer 角色，负责指出方案的逻辑缺陷、数据矛盾和发表风险。核心贡献在于通过实际检查数据发现了度量饱和模式，从而改变了论文方向。
- **Claude**：讨论和记录辅助。技术方案的分析和结构化呈现。

---

*本记录由 Claude 在讨论过程中整理，经参与者确认后存档。*
