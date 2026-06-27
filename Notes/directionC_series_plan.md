# Sparse Intervention Toolkit（方向C）系列研究总体规划

> **Material Passport**
> - Origin Skill: experiment-agent (plan mode)
> - Origin Date: 2026-06-18
> - Verification Status: UNVERIFIED
> - Version Label: sparse_intervention_series_v1
> - Scope: 方向C Sparse Intervention Toolkit 系列研究全周期规划

---

## 一、问题背景与核心理念

### 1.1 为什么需要系列而非单篇论文？

方向C源自12篇LLM可解释性论文的交叉局限性分析，核心理念是：
当前Mech Interp社区对干预的理解极度单一——ablation几乎是一切的默认操作。

Ablation只是干预连续空间中的一个极端边界点。四篇论文独立证明了这个问题的严重性：

- Paper 20: Refusal方向causal necessary但causal insufficient, 0/1 ablation无法捕捉多组件协同
- Paper 22: Wrecking-ball ablation破坏了太多结构, 需要更精细的干预粒度
- Paper 24: Final MLP只是放大确认已有表示, 不同功能角色需要不同干预策略
- Paper 21: Full ablation sweep计算成本极高, 需要principled的选择方法

把ablation从唯一工具变成分类学中的一个点, 涉及四个层次的问题:

1. 理论构建: 什么是干预空间?
2. 实证验证: 不同干预方法是否真的不同?
3. 方法创新: 新干预工具如何设计?
4. 工具工程: 如何让社区用起来?

这四个问题各自是一篇论文的体量。

### 1.2 系列设计原则

1. 每篇可独立发表——不依赖前一篇文章被接受才能投稿
2. 渐进式风险控制——从0 GPU的理论论文到高实验量的方法论文
3. 判定节点驱动——前一篇的实验结果决定后一篇的形式(长/短/博文/工具包)
4. 开源优先——所有代码和实验数据从Paper 2开始就公开

---

## 二、总体架构：四层递进Diamond模型

阶段划分:

| 阶段 | 包含论文 | 核心目标 | 风险等级 |
|------|---------|---------|---------|
| 阶段一 (Week 0-8) | Paper 1 | 确立研究话语权 | 最低 |
| 阶段二 (Week 6-18) | Paper 2 | 建立实证基础 | 低 |
| 阶段三 (Week 14-26) | Paper 3, 4, 5 | 产出方法论论文 | 中 |
| 阶段四 (Week 24-32) | Paper 6 | 工具落地 + 社区整合 | 低 |

---

## 三、逐篇详细设计

### Paper 1: Beyond Ablation

定位: 立场论文 + 分类学提案

核心论点: Mech Interp社区存在ablation偏见。需要干预空间分类学来指导方法选择。

核心贡献:
1. 三维干预流形的形式化定义:
   - 维度1 信息保留程度: 完全移除(ablation) 到 完全不干预
   - 维度2 因果粒度: neuron级 到 circuit级
   - 维度3 时空范围: 单个token 到 全层
2. 现有方法的分类学映射
3. 每个维度的理论动机(从12篇论文的局限模式提取)

形式判定:
- 理论框架完整且有深度 -> 长论文 (NeurIPS 2027 Position / TMLR)
- 框架够新但有争议 -> 短文 (ICML Blue Sky / ICLR)
- 主要是呼吁 -> 博客文章 (Distill / arXiv blog)

GPU: 0 | 时间线: 6-8周 | 前置条件: 无

---

### Paper 2: Intervention Landscapes

定位: 实证基准论文

实验设计:
- 模型: Pythia-1.4B, Gemma-2 2B
- 电路: IOI, Greater-Than, Indirect Object ID, Docstring
- 干预: Ablation, Mean-ablation, Resample-ablation, Gaussian Noise, Activation Steering, Patching
- 度量: 因果效应量, 方向一致性, 组件排序(Kendall tau), 计算成本

核心产出: 干预方法一致性排行榜 + 最少足够干预配方

形式判定:
- Ablation在>=80%是over-kill -> 长论文 (NeurIPS D&B)
- 方法不一致率>30% -> 短文 (Workshop)
- 主要是复现 -> 工具论文+博客 (JOSS)

时间线: 14周 | GPU: ~150 A100-hours

---

### Paper 3: Codebook Agreement as Quality Metric

定位: 方法论论文

核心假设: Codebook Agreement (A) 的下降可以作为干预侵入性的代理指标。

形式判定:
- A验证好+理论深 -> 长论文 (ICLR 2027)
- 验证好但理论不够 -> 短文 (Workshop)
- A表现一般 -> 合并到Paper 6

时间线: 12周 | GPU: ~200 A100-hours

---

### Paper 4: Activation Steering as Minimal Intervention
核心问题: 多强的steering vector是足够的? 存在通用黄金比例吗?
时间线: 10周 | GPU: ~50 A100-hours

### Paper 5: Intervention Through Noise
核心问题: 噪声注入能否替代ablation?
时间线: 10周 | GPU: ~50 A100-hours

### Paper 6: SparseIntervention Toolkit (Capstone)
三大API: InterventionGrid, InterventionQuality, CrossValidator
目标: JOSS / NeurIPS Demo Track
时间线: 10周(与P3-P5并行)

---

## 四、总决策树

阶段一: Paper 1 (分类学) -> arXiv发布
  |
阶段二: Paper 2 (实证基准)
  |
  +-- 判定节点1: Paper 2核心发现
       |
       +-- [A] Ablation是over-kill -> 全力Paper 4+5
       +-- [B] 方法间严重不一致(>30%) -> Paper 3的A成为裁判
       +-- [C] 结论弱 -> 降级workshop,合并
  |
阶段三: Paper 3 + Paper 4 + Paper 5 (并行)
  +-- 判定节点2: Paper 3的A度量效果
  +-- 判定节点3: Paper 4和5的质量
  |
阶段四: Paper 6 (Capstone Toolkit)

---

## 五、时间线与资源

资源汇总:
- 总时间: 32周 (8个月), ~200个深度工作天
- 总GPU: ~450 A100-hours (~,000-2,000云成本)
- 总代码量: ~8,000行Python (核心库3,000 + 脚本5,000)
- 主要依赖: PyTorch, TransformerLens, SAELens (全开源)

---

## 六、当下可立即推进的方案

### 本周内 (无需GPU)

1. 写Paper 1初稿框架 (2-3天)
   - 路径: F:/codex/LiM/papers/sparse_intervention/paper1_beyond_ablation.md
   - 定义三维干预流形 + 映射6种干预方法

2. 搭建实验基础设施 (2天)
   - 安装TransformerLens (pip install transformer-lens)
   - 写 intervention_grid.py 统一接口
   - 路径: F:/codex/LiM/experiments/sparse_intervention/
   - 跑通最小原型: 1 circuit x 4 methods

3. 实现Codebook Agreement函数 (1天)
   - 基于Paper 25的Proposition 4

4. 建立文献笔记: 干预方法参考基准

### 启动检查清单

[ ] 创建实验代码目录
[ ] 安装TransformerLens + SAELens
[ ] intervention_grid.py 完成
[ ] Paper 1初稿框架完成
[ ] 第一次小实验跑通 (1 circuit, 4 methods)
[ ] Codebook Agreement实现完成
[ ] 决定本系列第一篇投稿目标

---

## 七、风险矩阵

| 风险 | 概率 | 影响 | 缓解 |
|------|------|------|------|
| 不同干预方法结论高度一致 | 中 | 低-中 | 仍是好论文: ablation是over-kill |
| 方法间完全不一致 | 中 | 中 | 故事更强: 方法冲突 |
| Codebook Agreement对干预不敏感 | 低-中 | 高 | 降级到Paper 6章节 |
| SAE训练不稳定 | 中 | 中 | 用预训练SAE |
| 计算时间低估 | 中 | 中 | 先小模型再scale |

---

*本计划由 academic-research-suite / experiment-agent (plan mode) 辅助生成*
*创建日期: 2026-06-18*
