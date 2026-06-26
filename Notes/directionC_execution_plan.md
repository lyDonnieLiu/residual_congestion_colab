# Direction C 系列：下一步执行计划

> 基于 `all_results.json` 实验数据生成的阶段执行方案
> 依赖文件：`Notes/directionC_series_plan.md`（总体规划）

---

## 一、当前状态

Paper 1 (Beyond Ablation): **投稿准备阶段**
- main.tex 全部 7 章节完成（441行）
- 引用已验证零虚假（32条目）
- Position paper 重定位 + CBA→APS 重命名已完成
- 实验数据：6 methods × 3 circuits × 24 layers × 3 seeds，包含在 `all_results.json`（6632行）
- Figure：intervention_comparison.pdf（3×2 子图，300DPI）

---

## 二、实验结果关键发现

### 干预方法两极聚类

| 阵营 | 方法 | 内部一致性 (tau) | APS | 行为drop特征 |
|------|------|:---:|:---:|:---:|
| **Gentle 🟢** | mean ablation, patching, steering | 0.93–1.0 | >0.99 | 层间差异大(0~1) |
| **Destructive 🔴** | zero ablation, resample | -0.5 vs Gentle | 0.86–0.98 | 几乎全层drop=1 |
| **Noise ⚠️** | Gaussian noise | -0.9~-1.2 vs Gentle | 0.85–0.94 | behavioral drop < 0.15 |

### 跨电路一致性

| 电路 | mean tau | 模式 |
|------|:---:|------|
| IOI | -0.164 | 两极聚类清晰 |
| Greater-Than | -0.187 | 两极聚类清晰 |
| Docstring | 0.036 | 弱相关，需要进一步检查 |

### 关键数值

- **zero vs mean ablation tau** = -0.508（IOI）→ zero ablation 给出的重要性排序与 mean 相反
- **mean ablation vs patching tau = 1.0** → 两种方法在所有层上排序完全一致
- **overkill ratio = 0.0** → 没有方法在所有层上都比另一个更温和
- **silent damage**：Gaussian 噪声在 L1 的 behavioral drop = 0.018，但 APS = 0.854

---

## 三、决策分析（判定节点 1）

来自总体规划的决策树：

| 路径 | 条件 | 评估 |
|:---|:---|:---:|
| **Path B ✅** | 方法间严重不一致(>30%) | mean tau = -0.16~-0.19，两极聚类显著 |
| Path A ❌ | Ablation 是 over-kill | overkill ratio = 0.0 不支持 |
| Path C ❌ | 结论弱 | 两极聚类是 novel pattern，结论强 |

**推荐：Path B** → Paper 3 (APS 理论验证) 作为系列第二篇。

---

## 四、阶段 A：Paper 1 投稿 + 实验扩展（≈2-3 周）

### A1. Paper 1 投稿前准备（无 GPU）

```
[ ] pdflatex + bibtex + pdflatex × 2 → 0 errors
[ ] elsarticle 模板格式检查
[ ] Neurocomputing 页数限制确认
[ ] 投稿包：main.tex + references.bib + figures/*.pdf + main.pdf
[ ] Abstract + Highlights 二次校对
```

### A2. 跨模型验证（~10-15 A100-hours）

```
模型:  Gemma-2 2B（替代 Pythia-1.4B）
电路:  IOI（最具鉴别力的电路）
方法:  zero ablation, mean ablation, Gaussian noise, activation steering（4种，覆盖两极）
种子:  42, 123, 456（3 seeds）
└─ 成功标准: tau方向一致 + 跨模型tau相关性 > 0.7
```

### A3. 方法聚类形式化分析（无GPU）

```
输入:  6×6 Kendall tau相似性矩阵（每电路一个）
输出:  方法家族树 dendrogram
用途:  Paper 1 supplementary materials / Paper 3 前置结果
```

---

## 五、阶段 B：系列第二篇论文（Paper 1 投稿后启动）

### 选项 I（推荐 ⭐⭐）：Paper 3 — APS 理论验证

**定位**：方法论论文，将 APS 从"启发式度量"提升为"有理论保证的干预质量指标"

**差异化策略**（相对于 Paper 1）：
- Paper 1 使用 APS 作为实证工具
- Paper 3 对 APS 本身做形式化验证

**核心问题**：
1. K=100 分箱是否最优？APS 对 K 的敏感度？
2. 是否存在 APS 阈值，低于该阈值行为退化必然发生？
3. APS 能否预测性地判断干预方法的适用性？

**实验量**：~200 A100-hours
**目标**：ICLR 2027 / TMLR
**风险**：中等（需要与 Paper 1 重复 APS 内容做区分）

### 选项 II（备选）：跨模型 Replication 报告

- 内容：Pythia-1.4B → Gemma-2 2B 扩展，确认聚类模式
- 目标：TMLR Replication Track / arXiv 技术报告
- 时间：2-3 周（Phase A 完成后快速产出）
- 风险：最低

### 选项 III（长期）：Paper 4 — Activation Steering 方法论

- 动机：steering ≈ mean ablation（tau=0.94）且 APS > 0.99
- 仅在 Paper 3 被拒或需要补充实验时启动

---

## 六、不执行事项

1. 不启动 Paper 2 (Intervention Landscapes) —— 已被 Paper 1 实验吸收
2. 不启动 Paper 5 (Intervention Through Noise) —— 噪声实验已部分覆盖
3. 不启动 Paper 6 (Toolkit) —— Paper 1 未被接收前无发表基础
4. 不新增 GPU 密集实验（除 A2 最小跨模型验证外）

---

## 七、验证标准

| 检查项 | 方法 | 标准 |
|--------|------|------|
| Paper 1 编译 | pdflatex + bibtex × 3 | 0 errors, 0 warnings |
| 跨模型稳定性 | Pythia vs Gemma tau 比较 | 相关性 > 0.7 |
| 聚类图输出 | hierarchical clustering | dendrogram 清晰显示两极 |

---

## 八、关键文件索引

| 文件路径 | 用途 |
|----------|------|
| `Papers/sparse_intervention/paper/main.tex` | Paper 1 正文 |
| `Papers/sparse_intervention/paper/references.bib` | 参考文献 |
| `experiments/sparse_intervention/code/__init__.py` | InterventionGrid 引擎 |
| `experiments/sparse_intervention/code/metrics.py` | APS 等度量 |
| `experiments/sparse_intervention/code/analysis.py` | InterventionAnalyzer |
| `experiments/sparse_intervention/results/all_results.json` | 完整实验数据 |
| `experiments/sparse_intervention/results/analysis_for_paper.json` | 论文用汇总 |
| `Notes/directionC_series_plan.md` | 系列总体规划（父文档） |
